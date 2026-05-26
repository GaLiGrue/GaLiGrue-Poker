"""
Module für die Kartenverwaltung im Poker-Spiel.
"""

from classes import Karte
from Spielablauf import WERT_NAMEN, FARBEN

def karten_geben(AlleSpieler, Anzahl, Deck):
    """Teilt jedem Spieler Anzahl Karten aus."""
    for Spieler in AlleSpieler:
        for _ in range(Anzahl):
            KarteObjekt = Deck.get_Card()
            Spieler.add_Karten([KarteObjekt])
    return AlleSpieler, Deck


def karten_austeilen(Ziele, Anzahl, Deck):
    """Teilt jedem Ziel eine bestimmte Anzahl Karten aus und speichert deren Namen."""
    for Ziel in Ziele:
        for _ in range(Anzahl):
            KarteObjekt = Deck.get_Card()
            if hasattr(Ziel, "add_Karten"):
                Ziel.add_Karten([KarteObjekt])
            else:
                Ziel["cards"].append(KarteObjekt.get_Name())
    return Deck


def karten_wert(KarteCode):
    """Liest den Zahlenwert aus einem Kartencode wie k14."""
    return int(KarteCode[1:])


def karten_farbe(KarteCode):
    """Liest die Farbe aus einem Kartencode wie k14."""
    return KarteCode[0]


def karten_bild(KarteCode):
    """Gibt den Bildpfad fuer einen Kartencode zurueck."""
    return Karte(KarteCode).get_image_path()


def oeffentliche_karte(KarteCode):
    """Bereitet eine Karte fuer die Anzeige im Template auf."""
    Wert = karten_wert(KarteCode)
    Beschriftung = WERT_NAMEN.get(Wert, str(Wert)).capitalize()
    return {
        "code": KarteCode,
        "label": f"{Beschriftung} {FARBEN[karten_farbe(KarteCode)]['symbol']}",
        "image": karten_bild(KarteCode),
    }