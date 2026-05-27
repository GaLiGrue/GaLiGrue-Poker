"""
Funktionen zur Erstellung von Player- und Spiel-Objekten, Verwaltung von Spielern, Prüfung und Durchführung von Spieleraktionen
"""

from classes import Player, Spiel
from Spiel_Helfer import aktueller_spieler, aktive_spieler, spieler_finden
from Spielablauf import zug_weitergeben, runde_beenden

# ============================================================================
# SPIELER-Erstellung und Spiel-Erstellung
# ============================================================================

def spieler_erstellen(SpielerId, Name):
    """Erstellt ein Player-Objekt mit Startchips und Web-Zusatzstatus."""
    Spieler = Player(1000, Name, str(SpielerId))
    Spieler.set_IstDrin(True)
    Spieler.set_AllIn(False)
    Spieler.set_ChipsGesetzt(0)
    Spieler.set_Gehandelt(False)
    Spieler.set_Eliminiert(False)
    return Spieler


def spiel_erstellen(SpielId, BenutzerId, Benutzername, Modus):
    """Erstellt ein neues Spiel-Objekt mit dem angemeldeten Spieler als Host."""
    return Spiel(SpielId, Modus, BenutzerId, [spieler_erstellen(BenutzerId, Benutzername)])

# ============================================================================
# SPIELER-VERWALTUNG
# ============================================================================

def spieler_hinzufuegen(Spiel, SpielerId, Benutzername):
    """Fuegt einen Spieler zum Spiel hinzu, falls er noch nicht am Tisch sitzt."""
    VorhandenerSpieler = spieler_finden(Spiel, SpielerId)
    if VorhandenerSpieler:
        return VorhandenerSpieler

    Spieler = spieler_erstellen(SpielerId, Benutzername)
    Spiel.get_Spieler().append(Spieler)
    Spiel.set_Nachricht(f"{Benutzername} ist dem Tisch beigetreten.")
    return Spieler


def spieler_verlassen(Spiel, SpielerId):
    """Entfernt einen Spieler vom Tisch und aktualisiert Host, Zugfolge und Rundenzustand."""
    SpielerId = str(SpielerId)
    GehenderSpieler = spieler_finden(Spiel, SpielerId)
    if not GehenderSpieler:
        return

    WarAktuell = aktueller_spieler(Spiel) == GehenderSpieler if Spiel.get_Spieler() else False
    Spiel.set_Spieler([Spieler for Spieler in Spiel.get_Spieler() if Spieler.get_ClientName() != SpielerId])
    Spiel.set_Nachricht(f"{GehenderSpieler.get_Name()} hat den Tisch verlassen.")

    if Spiel.get_HostId() == SpielerId and Spiel.get_Spieler():
        Spiel.set_HostId(Spiel.get_Spieler()[0].get_ClientName())

    if Spiel.get_Gestartet() and WarAktuell and Spiel.get_Spieler() and not Spiel.get_Gewinner():
        Spiel.set_ZugIndex(Spiel.get_ZugIndex() % len(Spiel.get_Spieler()))
        zug_weitergeben(Spiel)

    if Spiel.get_Spieler() and Spiel.get_Gestartet() and len([Spieler for Spieler in Spiel.get_Spieler() if not Spieler.get_Eliminiert()]) <= 1:
        runde_beenden(Spiel)

# ============================================================================
# SPIEL- UND SPIELER-ABFRAGEN
# ============================================================================

def kann_spiel_beitreten(Spiel):
    """Prueft, ob ein Multiplayer-Spiel noch nicht gestartet und nicht voll ist."""
    return bool(Spiel and not Spiel.get_Gestartet() and len(Spiel.get_Spieler()) < 6)


def kann_spiel_starten(Spiel, SpielerId):
    """Prueft, ob der Host mit mindestens zwei aktiven Spielern starten darf."""
    return (
        Spiel.get_HostId() == str(SpielerId)
        and len([Spieler for Spieler in Spiel.get_Spieler() if Spieler.get_Chips() > 0]) >= 2
    )
    

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

# ============================================================================
# SPIELER-AKTIONEN
# ============================================================================

def chips_setzen_web(Spieler, Betrag):
    """Setzt Chips fuer ein Player-Objekt und gibt den wirklich gezahlten Betrag zurueck."""
    Betrag = max(0, int(Betrag))
    Gezahlt = min(Betrag, Spieler.get_Chips())
    Spieler.add_Chips(-Gezahlt)
    Spieler.add_ChipsGesetzt(Gezahlt)
    if Spieler.get_Chips() == 0:
        Spieler.set_AllIn(True)
    return Gezahlt


def all_in_setzen_web(Spieler):
    """Setzt alle uebrigen Chips eines Players als Einsatz."""
    Gezahlt = Spieler.get_Chips()
    Spieler.add_Chips(-Gezahlt)
    Spieler.add_ChipsGesetzt(Gezahlt)
    Spieler.set_AllIn(True)
    Spieler.set_Gehandelt(True)
    return Gezahlt


def spieler_aktion_ausfuehren(Spiel, Spieler, Aktion, RaiseBetrag=50):
    """Fuehrt fold, call/check, raise oder all_in fuer einen konkreten Spieler aus."""
    def folden_web(Spieler):
        """Markiert einen Player als gefoldet und als bereits gehandelt."""
        Spieler.set_IstDrin(False)
        Spieler.set_Gehandelt(True)

    ZuCallen = max(0, Spiel.get_AktuellerEinsatz() - Spieler.get_ChipsGesetzt())

    if Aktion == "fold":
        folden_web(Spieler)
        Spiel.set_LetzteAktion(f"{Spieler.get_Name()} foldet.")
    elif Aktion == "all_in":
        Gezahlt = all_in_setzen_web(Spieler)
        Spiel.add_Chips(Gezahlt)
        if Spieler.get_ChipsGesetzt() > Spiel.get_AktuellerEinsatz():
            Spiel.set_AktuellerEinsatz(Spieler.get_ChipsGesetzt())
            for AndererSpieler in aktive_spieler(Spiel):
                if AndererSpieler.get_ClientName() != Spieler.get_ClientName() and not AndererSpieler.get_AllIn():
                    AndererSpieler.set_Gehandelt(False)
        Spieler.set_Gehandelt(True)
        Spiel.set_LetzteAktion(f"{Spieler.get_Name()} geht All-in mit {Gezahlt} Chips.")
    elif Aktion == "raise":
        GesamtEinsatz = ZuCallen + max(25, RaiseBetrag)
        Gezahlt = chips_setzen_web(Spieler, GesamtEinsatz)
        Spiel.add_Chips(Gezahlt)
        Spiel.set_AktuellerEinsatz(max(Spiel.get_AktuellerEinsatz(), Spieler.get_ChipsGesetzt()))
        for AndererSpieler in aktive_spieler(Spiel):
            if AndererSpieler.get_ClientName() != Spieler.get_ClientName():
                AndererSpieler.set_Gehandelt(False)
        Spieler.set_Gehandelt(True)
        Spiel.set_LetzteAktion(f"{Spieler.get_Name()} raist um {max(25, RaiseBetrag)} Chips.")
    else:
        Gezahlt = chips_setzen_web(Spieler, ZuCallen)
        Spiel.add_Chips(Gezahlt)
        Spieler.set_Gehandelt(True)
        Spiel.set_LetzteAktion(f"{Spieler.get_Name()} callt {Gezahlt} Chips." if Gezahlt else f"{Spieler.get_Name()} checkt.")

    zug_weitergeben(Spiel)


def spieler_aktion_per_id_ausfuehren(Spiel, SpielerId, Aktion, RaiseBetrag=50):
    """Fuehrt eine Spieleraktion ueber die Spieler-ID aus, wenn der Spieler am Zug ist."""
    if not kann_spieler_handeln(Spiel, SpielerId):
        return False

    Spieler = spieler_finden(Spiel, SpielerId)
    spieler_aktion_ausfuehren(Spiel, Spieler, Aktion, RaiseBetrag)
    return True
