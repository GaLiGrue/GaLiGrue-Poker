"""
Gemeinsame Abfragen fuer Spieler und Spielzustand.
"""


def aktueller_spieler(Spiel):
    """Gibt den Spieler zurueck, der laut ZugIndex gerade am Zug ist."""
    if not Spiel.get_Spieler():
        return None
    return Spiel.get_Spieler()[Spiel.get_ZugIndex() % len(Spiel.get_Spieler())]


def spieler_finden(Spiel, SpielerId):
    """Sucht einen Spieler im Spiel ueber seine ID."""
    SpielerId = str(SpielerId)
    return next((Spieler for Spieler in Spiel.get_Spieler() if Spieler.get_ClientName() == SpielerId), None)


def aktive_spieler(Spiel):
    """Gibt alle Spieler zurueck, die nicht gefoldet haben und noch im Spiel sind."""
    return [
        Spieler
        for Spieler in Spiel.get_Spieler()
        if Spieler.get_IstDrin() and Spieler.get_Chips() >= 0 and not Spieler.get_Eliminiert()
    ]
