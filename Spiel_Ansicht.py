"""
In diesem Modul wird die Funktion definiert, die die Datenstruktur für die Spielansicht erstellt, damit das Template sie rendern kann.
"""

from Spieler_Und_Spiel_Verwaltung import aktueller_spieler, spieler_finden
from Kartenverwaltung import oeffentliche_karte

def spiel_ansicht_erstellen(Spiel, BenutzerId):
    """Erstellt die Datenstruktur, die das Template fuer die Spielansicht braucht."""
    def spieler_ansicht_erstellen(Spieler, BenutzerId, AktuellerSpieler):
        """Wandelt ein Player-Objekt in ein Dict fuer das Template um."""
        return {
            "id": Spieler.get_ClientName(),
            "name": Spieler.get_Name(),
            "chips": Spieler.get_Chips(),
            "bet": Spieler.get_ChipsGesetzt(),
            "folded": not Spieler.get_IstDrin(),
            "acted": Spieler.get_Gehandelt(),
            "all_in": Spieler.get_AllIn(),
            "eliminated": Spieler.get_Eliminiert(),
            "cards": [KarteObjekt.get_Name() for KarteObjekt in Spieler.get_Karten()],
            "is_current": AktuellerSpieler is not None and Spieler.get_ClientName() == AktuellerSpieler.get_ClientName(),
            "is_user": Spieler.get_ClientName() == BenutzerId,
            "visual_cards": [oeffentliche_karte(KarteObjekt.get_Name()) for KarteObjekt in Spieler.get_Karten()],
            "chip_icons": list(range(max(1, min(5, Spieler.get_Chips() // 200 + 1)))),
        }

    AktuellerSpieler = aktueller_spieler(Spiel) if Spiel.get_Gestartet() and not Spiel.get_Gewinner() else None
    BenutzerId = str(BenutzerId)
    BenutzerSpieler = spieler_finden(Spiel, BenutzerId)
    ZuCallen = max(0, Spiel.get_AktuellerEinsatz() - BenutzerSpieler.get_ChipsGesetzt()) if BenutzerSpieler else 0
    BenutzerHatVerloren = bool(BenutzerSpieler and BenutzerSpieler.get_Eliminiert() and Spiel.get_Gewinner())
    SichtbareSpieler = Spiel.get_Spieler()
    if BenutzerSpieler:
        BenutzerIndex = Spiel.get_Spieler().index(BenutzerSpieler)
        SichtbareSpieler = Spiel.get_Spieler()[BenutzerIndex:] + Spiel.get_Spieler()[:BenutzerIndex]

    AktuellerSpielerAnzeige = spieler_ansicht_erstellen(AktuellerSpieler, BenutzerId, AktuellerSpieler) if AktuellerSpieler else None

    return {
        "id": Spiel.get_Id(),
        "mode": Spiel.get_Modus(),
        "host_id": Spiel.get_HostId(),
        "deck": Spiel.get_Deck(),
        "players": Spiel.get_Spieler(),
        "community": Spiel.get_Gemeinschaftskarten(),
        "pot": Spiel.get_Pot(),
        "current_bet": Spiel.get_AktuellerEinsatz(),
        "stage": Spiel.get_Phase(),
        "turn_index": Spiel.get_ZugIndex(),
        "message": Spiel.get_Nachricht(),
        "winner": Spiel.get_Gewinner(),
        "last_action": Spiel.get_LetzteAktion(),
        "started": Spiel.get_Gestartet(),
        "current_player": AktuellerSpielerAnzeige,
        "current_player_id": AktuellerSpieler.get_ClientName() if AktuellerSpieler else None,
        "user_player_id": BenutzerId,
        "is_host": Spiel.get_HostId() == BenutzerId,
        "user_can_act": bool(AktuellerSpieler and AktuellerSpieler.get_ClientName() == BenutzerId and not Spiel.get_Gewinner()),
        "to_call": ZuCallen,
        "user_lost": BenutzerHatVerloren,
        "community_cards": [oeffentliche_karte(KarteCode) for KarteCode in Spiel.get_Gemeinschaftskarten()],
        "event_key": "|".join([
            str(Spiel.get_Id()),
            str(Spiel.get_Phase()),
            str(Spiel.get_Nachricht()),
            str(Spiel.get_LetzteAktion()),
            str(Spiel.get_Gewinner()),
            str(len(Spiel.get_Spieler())),
        ]),
        "players": [
            spieler_ansicht_erstellen(Spieler, BenutzerId, AktuellerSpieler)
            for Spieler in SichtbareSpieler
        ],
    }


