from itertools import combinations

from classes import Karte, Kartendeck
from Kartengeben import Kartengeben
from GanzesProgramm import GewinnerAusWebSpielern
from chipSetzen import all_in_web, fold_web, setze_chips_web

SUITS = {
    "k": {"name": "clubs", "symbol": "Kreuz"},
    "h": {"name": "hearts", "symbol": "Herz"},
    "p": {"name": "spades", "symbol": "Pik"},
    "s": {"name": "diamonds", "symbol": "Karo"},
}

VALUE_NAMES = {
    11: "jack",
    12: "queen",
    13: "king",
    14: "ace",
}

RANK_NAMES = {
    8: "Straight Flush",
    7: "Vierling",
    6: "Full House",
    5: "Flush",
    4: "Straight",
    3: "Drilling",
    2: "Zwei Paare",
    1: "Ein Paar",
    0: "High Card",
}


class DealTarget:
    def __init__(self):
        self.cards = []

    def add_Karten(self, cards):
        self.cards.extend(cards)


def make_deck():
    return Kartendeck()


def deal_cards(targets, count, deck):
    deal_targets = [DealTarget() for _ in targets]
    deal_targets, deck = Kartengeben(deal_targets, count, deck)
    for target, dealt in zip(targets, deal_targets):
        target["cards"].extend(card.get_Name() for card in dealt.cards)
    return deck


def draw_cards(deck, count):
    return [deck.get_Card().get_Name() for _ in range(count)]


def card_value(card):
    return int(card[1:])


def card_suit(card):
    return card[0]


def card_image(card):
    return Karte(card).get_image_path()


def public_card(card):
    value = card_value(card)
    label = VALUE_NAMES.get(value, str(value)).capitalize()
    return {
        "code": card,
        "label": f"{label} {SUITS[card_suit(card)]['symbol']}",
        "image": card_image(card),
    }


def straight_high(values):
    unique_values = sorted(set(values), reverse=True)
    if 14 in unique_values:
        unique_values.append(1)
    for group in combinations(unique_values, 5):
        sorted_group = sorted(group, reverse=True)
        if sorted_group[0] - sorted_group[4] == 4 and len(set(sorted_group)) == 5:
            return 5 if sorted_group[0] == 5 else sorted_group[0]
    return None


def evaluate_hand(cards):
    values = sorted((card_value(card) for card in cards), reverse=True)
    suits = [card_suit(card) for card in cards]
    counts = {value: values.count(value) for value in set(values)}
    ordered_counts = sorted(counts.items(), key=lambda item: (item[1], item[0]), reverse=True)

    flush_suit = next((suit for suit in SUITS if suits.count(suit) >= 5), None)
    flush_cards = [card for card in cards if card_suit(card) == flush_suit] if flush_suit else []
    flush_values = sorted((card_value(card) for card in flush_cards), reverse=True)
    straight = straight_high(values)
    straight_flush = straight_high(flush_values) if flush_suit else None

    if straight_flush:
        return (8, [straight_flush])

    four = next((value for value, count in ordered_counts if count == 4), None)
    if four:
        kicker = max(value for value in values if value != four)
        return (7, [four, kicker])

    triples = sorted([value for value, count in counts.items() if count == 3], reverse=True)
    pairs = sorted([value for value, count in counts.items() if count == 2], reverse=True)
    if triples and (pairs or len(triples) > 1):
        full_house_pair = pairs[0] if pairs else triples[1]
        return (6, [triples[0], full_house_pair])

    if flush_suit:
        return (5, flush_values[:5])

    if straight:
        return (4, [straight])

    if triples:
        kickers = [value for value in values if value != triples[0]][:2]
        return (3, [triples[0], *kickers])

    if len(pairs) >= 2:
        kicker = max(value for value in values if value not in pairs[:2])
        return (2, [pairs[0], pairs[1], kicker])

    if pairs:
        kickers = [value for value in values if value != pairs[0]][:3]
        return (1, [pairs[0], *kickers])

    return (0, values[:5])


def hand_label(score):
    return RANK_NAMES[score[0]]


def bot_strength(player_cards, community_cards):
    if community_cards:
        score = evaluate_hand(player_cards + community_cards)
        return min(1.0, (score[0] / 8) + (max(score[1]) / 100))

    first, second = sorted((card_value(card) for card in player_cards), reverse=True)
    suited = card_suit(player_cards[0]) == card_suit(player_cards[1])
    pair_bonus = 0.34 if first == second else 0
    high_bonus = (first + second) / 32
    suited_bonus = 0.08 if suited else 0
    connector_bonus = 0.06 if abs(first - second) <= 2 else 0
    return min(1.0, high_bonus + pair_bonus + suited_bonus + connector_bonus)


def determine_winner_ids(players, community_cards):
    return GewinnerAusWebSpielern(players, community_cards)


def place_bet(player, amount):
    return setze_chips_web(player, amount)


def fold_player(player):
    fold_web(player)


def all_in_player(player):
    return all_in_web(player)
