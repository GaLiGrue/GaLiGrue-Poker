"""
Hier befinden sich Funktionen, die Informationen über den aktuellen Spiel- und Spielerstatus zurückgeben, z.B. welcher Spieler gerade am Zug ist oder ob ein Spieler noch Chips hat. Diese Funktionen werden von verschiedenen Teilen der App verwendet, um zu entscheiden, welche Aktionen erlaubt sind oder um Informationen an die Benutzeroberfläche weiterzugeben.
"""


def aktueller_spieler(Spiel):
    """Gibt den Spieler zurueck, der laut turn_index gerade am Zug ist."""
    if not Spiel.get_Spieler():
        return None
    return Spiel.get_Spieler()[Spiel.get_ZugIndex() % len(Spiel.get_Spieler())]

def kann_spiel_beitreten(Spiel):
    """Prueft, ob ein Multiplayer-Spiel noch nicht gestartet und nicht voll ist."""
    return bool(Spiel and not Spiel.get_Gestartet() and len(Spiel.get_Spieler()) < 6)


def kann_spiel_starten(Spiel, SpielerId):
    """Prueft, ob der Host mit mindestens zwei aktiven Spielern starten darf."""
    return (
        Spiel.get_HostId() == str(SpielerId)
        and len([Spieler for Spieler in Spiel.get_Spieler() if Spieler.get_Chips() > 0]) >= 2
    )
    

def spieler_finden(Spiel, SpielerId):
    """Sucht einen Spieler im Spiel ueber seine ID."""
    SpielerId = str(SpielerId)
    return next((Spieler for Spieler in Spiel.get_Spieler() if Spieler.get_ClientName() == SpielerId), None)


def kann_spieler_handeln(Spiel, SpielerId):
    """Prueft, ob der angegebene Spieler gerade eine Aktion ausfuehren darf."""
    BenutzerSpieler = spieler_finden(Spiel, SpielerId)
    return (
        BenutzerSpieler is not None
        and not Spiel.get_Gewinner()
        and Spiel.get_Gestartet()
        and aktueller_spieler(Spiel) == BenutzerSpieler
    )


def kann_neue_runde_starten(Spiel, SpielerId):
    """Prueft, ob ein Spieler eine neue Runde starten darf."""
    BenutzerSpieler = spieler_finden(Spiel, SpielerId)
    if BenutzerSpieler and BenutzerSpieler.get_Chips() <= 0:
        return False
    return Spiel.get_Modus() == "singleplayer" or Spiel.get_HostId() == str(SpielerId)


def spieler_ist_raus(Spiel, SpielerId):
    """Prueft, ob ein Spieler keine Chips mehr hat."""
    BenutzerSpieler = spieler_finden(Spiel, SpielerId)
    return bool(BenutzerSpieler and BenutzerSpieler.get_Chips() <= 0)

def aktive_spieler(Spiel):
    """Gibt alle Spieler zurueck, die nicht gefoldet haben und noch im Spiel sind."""
    return [Spieler for Spieler in Spiel.get_Spieler() if Spieler.get_IstDrin() and Spieler.get_Chips() >= 0 and not Spieler.get_Eliminiert()]