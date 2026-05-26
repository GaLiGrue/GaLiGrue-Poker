from functools import wraps
import random
import string

from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



from Spiel_Ansicht import spiel_ansicht_erstellen
from Spieler_Und_Spiel_Verwaltung import spieler_hinzufuegen, spieler_verlassen, spiel_erstellen, spieler_aktion_per_id_ausfuehren, kann_spiel_beitreten, kann_spiel_starten, kann_neue_runde_starten, spieler_ist_raus
from Spielablauf import hand_starten
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


def get_user_game():
    room_id = session.get("room_id")
    return games.get(room_id)


def leave_current_room():
    room_id = session.get("room_id")
    game = games.get(room_id)
    if not game:
        session.pop("room_id", None)
        return

    spieler_verlassen(game, session["user_id"])
    if not game.get_Spieler():
        games.pop(room_id, None)

    session.pop("room_id", None)


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
    code = f"S{session['user_id']}" if mode == "singleplayer" else room_code()
    game = spiel_erstellen(code, session["user_id"], session["username"], mode)
    games[code] = game
    session["room_id"] = game.get_Id()
    return redirect(url_for("game"))


@app.route('/join-room', methods=['POST'])
@login_required
def join_room():
    code = request.form.get("room_code", "").strip().upper()
    game = games.get(code)
    if not kann_spiel_beitreten(game):
        return redirect(url_for("dashboard"))

    spieler_hinzufuegen(game, session["user_id"], session["username"])
    session["room_id"] = code
    return redirect(url_for("game"))


@app.route('/game')
@login_required
def game():
    current_game = get_user_game()
    if not current_game:
        return redirect(url_for("dashboard"))
    return render_template("game.html", game=spiel_ansicht_erstellen(current_game, session["user_id"]), username=session["username"])


@app.route('/game/start', methods=['POST'])
@login_required
def start_game():
    current_game = get_user_game()
    if not current_game:
        return redirect(url_for("dashboard"))
    if kann_spiel_starten(current_game, session["user_id"]):
        hand_starten(current_game)
    return redirect(url_for("game"))


@app.route('/game/action', methods=['POST'])
@login_required
def game_action():
    current_game = get_user_game()
    if not current_game:
        return redirect(url_for("dashboard"))

    action = request.form.get("action")
    raise_amount = int(request.form.get("raise_amount", 50))
    spieler_aktion_per_id_ausfuehren(current_game, session["user_id"], action, raise_amount)
    return redirect(url_for("game"))


@app.route('/game/new-round', methods=['POST'])
@login_required
def new_round():
    current_game = get_user_game()
    if not current_game:
        return redirect(url_for("dashboard"))
    if spieler_ist_raus(current_game, session["user_id"]):
        return redirect(url_for("dashboard"))
    if not kann_neue_runde_starten(current_game, session["user_id"]):
        return redirect(url_for("game"))
    hand_starten(current_game)
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
