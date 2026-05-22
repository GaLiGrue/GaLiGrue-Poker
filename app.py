from functools import wraps
import random
import string

from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from poker_engine import (
    all_in_player,
    bot_strength,
    deal_cards,
    determine_winner_ids,
    draw_cards,
    evaluate_hand,
    fold_player,
    hand_label,
    make_deck,
    place_bet,
    public_card,
)

app = Flask(__name__)

app.secret_key = "supersecretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

games = {}


# USER DATENBANK
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/")
        return view(*args, **kwargs)
    return wrapped_view


def room_code():
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if code not in games:
            return code


def create_player(player_id, name, bot=False):
    return {
        "id": str(player_id),
        "name": name,
        "bot": bot,
        "chips": 1000,
        "bet": 0,
        "folded": False,
        "acted": False,
        "all_in": False,
        "eliminated": False,
        "cards": [],
    }


def create_game(user_id, username, mode):
    code = f"S{user_id}" if mode == "singleplayer" else room_code()
    game = {
        "id": code,
        "mode": mode,
        "host_id": str(user_id),
        "deck": [],
        "players": [create_player(user_id, username)],
        "community": [],
        "pot": 0,
        "current_bet": 0,
        "stage": "lobby",
        "turn_index": 0,
        "message": "Warte auf Spieler.",
        "winner": None,
        "last_action": None,
        "started": False,
    }

    if mode == "singleplayer":
        game["players"].extend([
            create_player("bot-1", "Ada", True),
            create_player("bot-2", "Ben", True),
            create_player("bot-3", "Mia", True),
        ])
        start_hand(game)

    games[code] = game
    return game


def get_user_game():
    room_id = session.get("room_id")
    return games.get(room_id)


def current_player(game):
    if not game["players"]:
        return None
    return game["players"][game["turn_index"] % len(game["players"])]


def find_player(game, player_id):
    player_id = str(player_id)
    return next((player for player in game["players"] if player["id"] == player_id), None)


def leave_current_room():
    room_id = session.get("room_id")
    game = games.get(room_id)
    if not game:
        session.pop("room_id", None)
        return

    user_id = str(session["user_id"])
    leaving_player = find_player(game, user_id)
    if leaving_player:
        was_current = current_player(game) == leaving_player if game["players"] else False
        game["players"] = [player for player in game["players"] if player["id"] != user_id]
        game["message"] = f"{leaving_player['name']} hat den Tisch verlassen."
        if game["host_id"] == user_id and game["players"]:
            game["host_id"] = game["players"][0]["id"]
        if game["started"] and was_current and game["players"] and not game["winner"]:
            game["turn_index"] = game["turn_index"] % len(game["players"])
            advance_turn(game)

    if not game["players"]:
        games.pop(room_id, None)
    elif game["started"] and len([player for player in game["players"] if not player.get("eliminated")]) <= 1:
        finish_round(game)

    session.pop("room_id", None)


def start_hand(game):
    game["players"] = [player for player in game["players"] if player["chips"] > 0]
    game["deck"] = make_deck()
    game["community"] = []
    game["pot"] = 0
    game["current_bet"] = 0
    game["stage"] = "preflop"
    game["turn_index"] = 0
    game["winner"] = None
    game["last_action"] = None
    game["started"] = True
    for player in game["players"]:
        player["bet"] = 0
        player["folded"] = False
        player["acted"] = False
        player["all_in"] = False
        player["eliminated"] = player["chips"] <= 0
        player["cards"] = []

    game["deck"] = deal_cards(game["players"], 2, game["deck"])

    game["message"] = f"{current_player(game)['name']} ist dran."


def next_stage(game):
    for player in game["players"]:
        player["bet"] = 0
        player["acted"] = False
    game["current_bet"] = 0

    if game["stage"] == "preflop":
        game["community"].extend(draw_cards(game["deck"], 3))
        game["stage"] = "flop"
        game["message"] = "Der Flop liegt auf dem Tisch."
    elif game["stage"] == "flop":
        game["community"].extend(draw_cards(game["deck"], 1))
        game["stage"] = "turn"
        game["message"] = "Der Turn wurde aufgedeckt."
    elif game["stage"] == "turn":
        game["community"].extend(draw_cards(game["deck"], 1))
        game["stage"] = "river"
        game["message"] = "Der River wurde aufgedeckt."
    else:
        finish_round(game)
        return

    game["turn_index"] = next_active_index(game, 0)
    if current_player(game):
        game["message"] += f" {current_player(game)['name']} ist dran."


def active_players(game):
    return [player for player in game["players"] if not player["folded"] and player["chips"] >= 0 and not player.get("eliminated")]


def take_bet(player, amount):
    return place_bet(player, amount)


def next_active_index(game, start_index):
    for offset in range(len(game["players"])):
        index = (start_index + offset) % len(game["players"])
        player = game["players"][index]
        if not player["folded"] and not player.get("eliminated") and (player["chips"] > 0 or player.get("all_in")):
            return index
    return 0


def betting_round_complete(game):
    active = active_players(game)
    if len(active) <= 1:
        return True
    return all(player["acted"] and (player["bet"] == game["current_bet"] or player.get("all_in")) for player in active)


def advance_turn(game):
    if len(active_players(game)) == 1:
        finish_round(game)
        return

    if betting_round_complete(game):
        next_stage(game)
        return

    game["turn_index"] = next_active_index(game, game["turn_index"] + 1)
    if current_player(game):
        game["message"] = f"{current_player(game)['name']} ist dran."


def apply_player_action(game, player, action, raise_amount=50):
    to_call = max(0, game["current_bet"] - player["bet"])

    if action == "fold":
        fold_player(player)
        game["last_action"] = f"{player['name']} foldet."
    elif action == "all_in":
        paid = all_in_player(player)
        game["pot"] += paid
        if player["bet"] > game["current_bet"]:
            game["current_bet"] = player["bet"]
            for other in active_players(game):
                if other["id"] != player["id"] and not other.get("all_in"):
                    other["acted"] = False
        player["acted"] = True
        game["last_action"] = f"{player['name']} geht All-in mit {paid} Chips."
    elif action == "raise":
        total_bet = to_call + max(25, raise_amount)
        paid = take_bet(player, total_bet)
        game["pot"] += paid
        game["current_bet"] = max(game["current_bet"], player["bet"])
        for other in active_players(game):
            if other["id"] != player["id"]:
                other["acted"] = False
        player["acted"] = True
        game["last_action"] = f"{player['name']} raist um {max(25, raise_amount)} Chips."
    else:
        paid = take_bet(player, to_call)
        game["pot"] += paid
        player["acted"] = True
        game["last_action"] = f"{player['name']} callt {paid} Chips." if paid else f"{player['name']} checkt."

    advance_turn(game)


def run_bot_turn(game):
    if game["winner"] or not game["started"]:
        return
    player = current_player(game)
    if not player or not player["bot"]:
        return

    to_call = max(0, game["current_bet"] - player["bet"])
    strength = bot_strength(player["cards"], game["community"])
    pot_odds = to_call / max(1, game["pot"] + to_call)
    can_raise = player["chips"] > to_call + 25

    if to_call > 0 and strength + 0.08 < pot_odds:
        apply_player_action(game, player, "fold")
    elif can_raise and strength > 0.72:
        apply_player_action(game, player, "raise", random.choice([75, 100, 150]))
    elif can_raise and strength > 0.52 and random.random() < 0.45:
        apply_player_action(game, player, "raise", random.choice([25, 50, 75]))
    else:
        apply_player_action(game, player, "call")


def finish_round(game):
    contenders = active_players(game)
    if len(contenders) == 1:
        winner = contenders[0]
        score = None
    else:
        winner_ids = determine_winner_ids(contenders, game["community"])
        winner = next(player for player in contenders if player["id"] in winner_ids)
        score = evaluate_hand(winner["cards"] + game["community"])

    winner["chips"] += game["pot"]
    for player in game["players"]:
        player["eliminated"] = player["chips"] <= 0
    game["winner"] = winner["name"]
    game["stage"] = "showdown"
    game["message"] = f"{winner['name']} gewinnt {game['pot']} Chips" + (f" mit {hand_label(score)}." if score else ".")
    game["pot"] = 0


def game_view_model(game):
    current = current_player(game) if game["started"] and not game["winner"] else None
    user_id = str(session["user_id"])
    user_player = find_player(game, user_id)
    to_call = max(0, game["current_bet"] - user_player["bet"]) if user_player else 0
    user_lost = bool(user_player and user_player.get("eliminated") and game["winner"])
    visible_players = game["players"]
    if user_player:
        user_index = game["players"].index(user_player)
        visible_players = game["players"][user_index:] + game["players"][:user_index]

    return {
        **game,
        "current_player": current,
        "current_player_id": current["id"] if current else None,
        "user_player_id": user_id,
        "is_host": game["host_id"] == user_id,
        "user_can_act": bool(current and current["id"] == user_id and not game["winner"]),
        "bot_can_act": bool(current and current["bot"] and game["mode"] == "singleplayer" and not game["winner"]),
        "to_call": to_call,
        "user_lost": user_lost,
        "community_cards": [public_card(card) for card in game["community"]],
        "event_key": "|".join([
            str(game["id"]),
            str(game["stage"]),
            str(game["message"]),
            str(game["last_action"]),
            str(game["winner"]),
            str(len(game["players"])),
        ]),
        "players": [
            {
                **player,
                "is_current": current is not None and player["id"] == current["id"],
                "is_user": player["id"] == user_id,
                "visual_cards": [public_card(card) for card in player["cards"]],
                "chip_icons": list(range(max(1, min(5, player["chips"] // 200 + 1)))),
            }
            for player in visible_players
        ],
    }


@app.route('/', methods=['GET', 'POST'])
def home():

    # LOGIN
    if request.method == 'POST':

        action = request.form.get("action")

        # REGISTER
        if action == "register":

            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                return "User existiert bereits!"

            hashed_password = generate_password_hash(password)

            new_user = User(
                username=username,
                email=email,
                password=hashed_password
            )

            db.session.add(new_user)
            db.session.commit()

            return redirect('/')

        # LOGIN
        elif action == "login":

            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):

                session['user_id'] = user.id
                session['username'] = user.username

                return redirect('/dashboard')

            else:
                return "Falsche Login Daten!"

    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'dashboard.html',
        username=session['username']
    )


@app.route('/join-game', methods=['POST'])
@login_required
def join_game():
    mode = request.form.get("mode", "singleplayer")
    game = create_game(session["user_id"], session["username"], mode)
    session["room_id"] = game["id"]
    return redirect(url_for("game"))


@app.route('/join-room', methods=['POST'])
@login_required
def join_room():
    code = request.form.get("room_code", "").strip().upper()
    game = games.get(code)
    if not game:
        return redirect(url_for("dashboard"))
    if game["started"]:
        return redirect(url_for("dashboard"))
    if len(game["players"]) >= 6:
        return redirect(url_for("dashboard"))

    existing_player = find_player(game, session["user_id"])
    if not existing_player:
        game["players"].append(create_player(session["user_id"], session["username"]))
        game["message"] = f"{session['username']} ist dem Tisch beigetreten."
    session["room_id"] = code
    return redirect(url_for("game"))


@app.route('/game')
@login_required
def game():
    current_game = get_user_game()
    if not current_game:
        return redirect(url_for("dashboard"))
    return render_template("game.html", game=game_view_model(current_game), username=session["username"])


@app.route('/game/start', methods=['POST'])
@login_required
def start_game():
    current_game = get_user_game()
    if not current_game:
        return redirect(url_for("dashboard"))
    if current_game["host_id"] == str(session["user_id"]) and len([player for player in current_game["players"] if player["chips"] > 0]) >= 2:
        start_hand(current_game)
    return redirect(url_for("game"))


@app.route('/game/action', methods=['POST'])
@login_required
def game_action():
    current_game = get_user_game()
    if not current_game:
        return redirect(url_for("dashboard"))
    if current_game["winner"] or not current_game["started"]:
        return redirect(url_for("game"))

    action = request.form.get("action")
    user_player = find_player(current_game, session["user_id"])
    if current_player(current_game) != user_player:
        return redirect(url_for("game"))

    raise_amount = int(request.form.get("raise_amount", 50))
    apply_player_action(current_game, user_player, action, raise_amount)
    return redirect(url_for("game"))


@app.route('/game/bot-step', methods=['POST'])
@login_required
def bot_step():
    current_game = get_user_game()
    if not current_game:
        return redirect(url_for("dashboard"))
    run_bot_turn(current_game)
    return redirect(url_for("game"))


@app.route('/game/new-round', methods=['POST'])
@login_required
def new_round():
    current_game = get_user_game()
    if not current_game:
        return redirect(url_for("dashboard"))
    user_player = find_player(current_game, session["user_id"])
    if user_player and user_player["chips"] <= 0:
        return redirect(url_for("dashboard"))
    if current_game["mode"] == "singleplayer" or current_game["host_id"] == str(session["user_id"]):
        start_hand(current_game)
    return redirect(url_for("game"))


@app.route('/game/leave', methods=['POST'])
@login_required
def leave_game():
    leave_current_room()
    return redirect(url_for("dashboard"))


@app.route('/cards/<path:filename>')
def cards(filename):
    return send_from_directory("cards", filename)


@app.route('/chips/<path:filename>')
def chips(filename):
    return send_from_directory("chips", filename)


@app.route('/table.svg')
def table_asset():
    return send_from_directory(".", "poker_table_bare.svg")


@app.route('/logout')
def logout():
    if "user_id" in session:
        leave_current_room()
    session.clear()
    return redirect('/')


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
