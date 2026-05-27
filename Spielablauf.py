"""
Reine Poker-Spiellogik: Handvergleich, Gewinnerbewertung und Kartenevaluierung.
"""

from classes import Karte, Player, Aktionen
from Spiel_Helfer import aktueller_spieler, aktive_spieler

FARBEN = {
    "k": {"name": "clubs", "symbol": "Kreuz"},
    "h": {"name": "hearts", "symbol": "Herz"},
    "p": {"name": "spades", "symbol": "Pik"},
    "s": {"name": "diamonds", "symbol": "Karo"},
}

WERT_NAMEN = {
    11: "jack",
    12: "queen",
    13: "king",
    14: "ace",
}

HAND_NAMEN = {
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

SMALL_BLIND = 25
BIG_BLIND = 50


# ============================================================================
# GEWINNER-BESTIMMUNG (reine Poker-Logik)
# ============================================================================

def gewinner_bestimmen(AlleSpieler, KartenMitte, Debug=False):
    """
    Alle Spieler vergleichen und den Gewinner bestimmen.
    Das ist die Gewinnerlogik aus GanzesProgramm.py, direkt in der Engine.
    """
    def get_Hand(Karten):
        """
        Gibt die beste Hand ausser Strassen und Flushes zurueck.
        Also Vierlinge, Full House, Drillinge, Zwei Paare, Ein Paar oder High Card.
        """
        def has_Straight(Karten, Zaehler=None):
            if not Zaehler:
                Zaehler = [0 for _ in range(13)]
                for Karte in Karten:
                    Wert = Karte.get_Value()
                    Zaehler[14 - Wert] += 1
            for Index in range(9):
                if Zaehler[Index] >= 1 and Zaehler[Index + 1] >= 1 and Zaehler[Index + 2] >= 1 and Zaehler[Index + 3] >= 1 and Zaehler[Index + 4] >= 1:
                    return True, 14 - Index
            if Zaehler[0] >= 1 and Zaehler[9] >= 1 and Zaehler[10] >= 1 and Zaehler[11] >= 1 and Zaehler[12] >= 1:
                return True, 5
            return False, None

        def wert_aus_index(Index):
            return 14 - Index

        def get_Beikarten(WertZaehler, Anzahl, Ausgeschlossen=None):
            if Ausgeschlossen is None:
                Ausgeschlossen = []
            Beikarten = []
            for Index in range(13):
                if Index not in Ausgeschlossen and WertZaehler[Index] > 0:
                    Beikarten.append(wert_aus_index(Index))
                    if len(Beikarten) == Anzahl:
                        break
            return Beikarten

        WertZaehler = [0 for _ in range(13)]
        for Karte in Karten:
            Wert = Karte.get_Value()
            WertZaehler[14 - Wert] += 1

        FarbZaehler = [[] for _ in range(4)]
        for Karte in Karten:
            match Karte.get_Suit():
                case "k":
                    FarbZaehler[0].append(Karte)
                case "h":
                    FarbZaehler[1].append(Karte)
                case "p":
                    FarbZaehler[2].append(Karte)
                case "s":
                    FarbZaehler[3].append(Karte)

        Strasse, StrassenKarte = has_Straight(Karten, WertZaehler)

        Flush = False
        FlushKarten = []
        for Farbe in FarbZaehler:
            if len(Farbe) >= 5:
                FarbKopie = Farbe.copy()
                FarbKopie.sort(key=lambda Karte: Karte.get_Value(), reverse=True)
                Flush = True
                FlushKarten = FarbKopie[:5]
                break

        if Strasse and Flush:
            StrassenFlush, HoechsteStrassenFlushKarte = has_Straight(FarbKopie)
            if StrassenFlush:
                return [8, HoechsteStrassenFlushKarte]

        if 4 in WertZaehler:
            Beikarten = get_Beikarten(WertZaehler, 1, Ausgeschlossen=[WertZaehler.index(4)])
            return [7, wert_aus_index(WertZaehler.index(4))] + Beikarten

        Drillinge = [Index for Index, Anzahl in enumerate(WertZaehler) if Anzahl == 3]
        Paare = [Index for Index, Anzahl in enumerate(WertZaehler) if Anzahl >= 2]
        if Drillinge and len(Paare) >= 2:
            Drilling = Drillinge[0]
            Paar = next(Index for Index in Paare if Index != Drilling)
            return [6, wert_aus_index(Drilling), wert_aus_index(Paar)]

        if Flush:
            return [5, FlushKarten[0].get_Value(), FlushKarten[1].get_Value(), FlushKarten[2].get_Value(), FlushKarten[3].get_Value(), FlushKarten[4].get_Value()]

        if Strasse:
            return [4, StrassenKarte]

        if 3 in WertZaehler:
            Beikarten = get_Beikarten(WertZaehler, 2, Ausgeschlossen=[WertZaehler.index(3)])
            return [3, wert_aus_index(WertZaehler.index(3))] + Beikarten

        if WertZaehler.count(2) >= 2:
            PaarIndex1 = WertZaehler.index(2)
            PaarIndex2 = WertZaehler.index(2, PaarIndex1 + 1)
            Beikarten = get_Beikarten(WertZaehler, 1, Ausgeschlossen=[PaarIndex1, PaarIndex2])
            return [2, wert_aus_index(PaarIndex1), wert_aus_index(PaarIndex2)] + Beikarten

        if 2 in WertZaehler:
            Beikarten = get_Beikarten(WertZaehler, 3, Ausgeschlossen=[WertZaehler.index(2)])
            return [1, wert_aus_index(WertZaehler.index(2))] + Beikarten

        Beikarten = get_Beikarten(WertZaehler, 5)
        return [0] + Beikarten

    Gewinner = Player(0, "temp", "temp")
    Gewinner.set_Hand([9])
    AlleGewinner = [Gewinner]
    for Spieler in AlleSpieler:
        if Spieler.get_IstDrin():
            Karten = Spieler.get_Karten().copy()
            Karten.extend(KartenMitte.get_Karten())
            Hand = get_Hand(Karten)
            Spieler.set_Hand(Hand)
            
    AlleHände = [(Spieler.get_Hand(), Spieler) for Spieler in AlleSpieler if Spieler.get_IstDrin()]
    AlleHände.sort(key=lambda x: x[0], reverse=True)  # Sortiere nach Handstärke
    GewinnerReihenfolge = [[]]
    AktuelleHand = AlleHände[0][0]
    for _, Spieler in AlleHände:
        if Spieler.get_Hand() == AktuelleHand:
            GewinnerReihenfolge[-1].append(Spieler)
        else:
            GewinnerReihenfolge.append([Spieler])
        AktuelleHand = Spieler.get_Hand()
            # if Spieler != Gewinner:
            #     SpielerHand = Spieler.get_Hand()
                
                
                
            #     GewinnerHand = Gewinner.get_Hand()
            #     for Index in range(len(SpielerHand)):
            #         if Index == 0:
            #             if SpielerHand[Index] < GewinnerHand[Index]:
            #                 Gewinner = Spieler
            #                 AlleGewinner = [Gewinner]
            #                 break
            #             if SpielerHand[Index] > GewinnerHand[Index]:
            #                 break
            #         else:
            #             if SpielerHand[Index] > GewinnerHand[Index]:
            #                 Gewinner = Spieler
            #                 AlleGewinner = [Gewinner]
            #                 break
            #             if SpielerHand[Index] < GewinnerHand[Index]:
            #                 break
            #     else:
            #         AlleGewinner.append(Spieler)

    return GewinnerReihenfolge, HAND_NAMEN[Gewinner.get_Hand()[0]]


# ============================================================================
# SPIEL-FLOW
# ============================================================================


def naechster_aktiver_index(Spiel, StartIndex):
    """Sucht ab einem Index den naechsten Spieler, der noch handeln kann."""
    for Abstand in range(len(Spiel.get_Spieler())):
        Index = (StartIndex + Abstand) % len(Spiel.get_Spieler())
        Spieler = Spiel.get_Spieler()[Index]
        if Spieler.get_IstDrin() and not Spieler.get_Eliminiert() and Spieler.get_Chips() > 0 and not Spieler.get_AllIn():
            return Index
    return 0


def hand_starten(Spiel):
    """Setzt die Hand zurueck, mischt neu und teilt jedem aktiven Spieler zwei Karten aus."""
    def karten_austeilen(Ziele, Anzahl, Deck):
        """Teilt jedem Ziel eine bestimmte Anzahl Karten aus und speichert deren Namen."""
        for Ziel in Ziele:
            for _ in range(Anzahl):
                if Deck:  # Prüfe ob Deck nicht leer ist
                    KarteObjekt = Deck.pop()  # Direkt von der Liste pop'en
                    if hasattr(Ziel, "add_Karten"):
                        Ziel.add_Karten([KarteObjekt])
                    else:
                        Ziel["cards"].append(KarteObjekt.get_Name())
        return Deck

    def blind_setzen(Spieler, Betrag):
        Gezahlt = min(Betrag, Spieler.get_Chips())
        Spieler.add_Chips(-Gezahlt)
        Spieler.add_ChipsGesetzt(Gezahlt)
        Spieler.set_AllIn(Spieler.get_Chips() == 0)
        Spiel.add_Chips(Gezahlt)
        return Gezahlt

    def blinds_setzen():
        SpielerListe = Spiel.get_Spieler()
        BlindIndex = Spiel.get_BlindIndex() % len(SpielerListe)
        SmallBlindSpieler = SpielerListe[BlindIndex]
        BigBlindSpieler = SpielerListe[(BlindIndex + 1) % len(SpielerListe)]

        SmallBlindGezahlt = blind_setzen(SmallBlindSpieler, SMALL_BLIND)
        BigBlindGezahlt = blind_setzen(BigBlindSpieler, BIG_BLIND)
        BigBlindSpieler.set_Gehandelt(True)

        Spiel.set_AktuellerEinsatz(max(SmallBlindGezahlt, BigBlindGezahlt))
        Spiel.set_BlindIndex((BlindIndex + 1) % len(SpielerListe))
        Spiel.set_ZugIndex(naechster_aktiver_index(Spiel, BlindIndex + 2))
        Spiel.set_LetzteAktion(
            f"{SmallBlindSpieler.get_Name()} setzt Small Blind ({SmallBlindGezahlt}), "
            f"{BigBlindSpieler.get_Name()} setzt Big Blind ({BigBlindGezahlt})."
        )

    Spiel.set_Spieler([Spieler for Spieler in Spiel.get_Spieler() if Spieler.get_Chips() > 0])
    if len(Spiel.get_Spieler()) < 2:
        Spiel.set_Gestartet(False)
        Spiel.set_Phase("lobby")
        Spiel.set_Nachricht("Es werden mindestens zwei Spieler mit Chips benoetigt.")
        return

    Spiel.set_Deck(Spiel.erstelle_deck())
    Spiel.set_Karten([])
    Spiel.set_Chips(0)
    Spiel.set_AktuellerEinsatz(0)
    Spiel.set_Phase("preflop")
    Spiel.set_Gewinner(None)
    Spiel.set_LetzteAktion(None)
    Spiel.set_Gestartet(True)
    for Spieler in Spiel.get_Spieler():
        Spieler.set_ChipsGesetzt(0)
        Spieler.set_IstDrin(True)
        Spieler.set_AllIn(False)
        Spieler.set_Gehandelt(False)
        Spieler.set_Eliminiert(Spieler.get_Chips() <= 0)
        Spieler.clear_Karten()

    Spiel.set_Deck(karten_austeilen(Spiel.get_Spieler(), 2, Spiel.get_Deck())) # Zwei Karten an Spieler austeilen

    blinds_setzen()
    Spiel.set_Nachricht(f"{aktueller_spieler(Spiel).get_Name()} ist dran.")


def naechste_phase(Spiel):
    """Wechselt von Preflop zu Flop, Turn, River oder beendet danach die Runde."""
    def karten_ziehen(Deck, Anzahl):
        """Zieht mehrere Karten vom Deck und gibt ihre Kartencodes zurueck."""
        return [Deck.pop().get_Name() for _ in range(Anzahl) if Deck]

    for Spieler in Spiel.get_Spieler():
        Spieler.set_ChipsGesetzt(0)
        Spieler.set_Gehandelt(False)
    Spiel.set_AktuellerEinsatz(0)

    if Spiel.get_Phase() == "preflop":
        Spiel.add_Karten(karten_ziehen(Spiel.get_Deck(), 3))
        Spiel.set_Phase("flop")
        Spiel.set_Nachricht("Der Flop liegt auf dem Tisch.")
    elif Spiel.get_Phase() == "flop":
        Spiel.add_Karten(karten_ziehen(Spiel.get_Deck(), 1))
        Spiel.set_Phase("turn")
        Spiel.set_Nachricht("Der Turn wurde aufgedeckt.")
    elif Spiel.get_Phase() == "turn":
        Spiel.add_Karten(karten_ziehen(Spiel.get_Deck(), 1))
        Spiel.set_Phase("river")
        Spiel.set_Nachricht("Der River wurde aufgedeckt.")
    else:
        runde_beenden(Spiel)
        return

    Spiel.set_ZugIndex(naechster_aktiver_index(Spiel, 0))
    if aktueller_spieler(Spiel):
        Spiel.add_Nachricht(f" {aktueller_spieler(Spiel).get_Name()} ist dran.")


def zug_weitergeben(Spiel):
    """Gibt den Zug weiter, wechselt bei Bedarf die Phase oder beendet die Runde."""
    def setzrunde_abgeschlossen(Spiel):
        """Prueft, ob alle aktiven Spieler gehandelt und den aktuellen Einsatz erreicht haben."""
        AktiveSpieler = aktive_spieler(Spiel)
        if len(AktiveSpieler) <= 1:
            return True
        return all(Spieler.get_Gehandelt() and (Spieler.get_ChipsGesetzt() == Spiel.get_AktuellerEinsatz() or Spieler.get_AllIn()) for Spieler in AktiveSpieler)

    if len(aktive_spieler(Spiel)) == 1:
        runde_beenden(Spiel)
        return

    if setzrunde_abgeschlossen(Spiel):
        naechste_phase(Spiel)
        return

    Spiel.set_ZugIndex(naechster_aktiver_index(Spiel, Spiel.get_ZugIndex() + 1))
    if aktueller_spieler(Spiel):
        Spiel.set_Nachricht(f"{aktueller_spieler(Spiel).get_Name()} ist dran.")


# ============================================================================
# RUNDE-VERWALTUNG
# ============================================================================

def runde_beenden(Spiel):
    """Bestimmt den Gewinner, zahlt den Pot aus und setzt das Spiel auf Showdown."""
    Kandidaten = aktive_spieler(Spiel)
    if len(Kandidaten) == 1:
        Gewinner = Kandidaten[0]
        Gewinner.add_Chips(Spiel.get_Chips())
        Ergebnis = None
    else:
        # Gewinner direkt bestimmen mit gewinner_bestimmen
        GewinnerSpieler, Ergebnis = gewinner_bestimmen(Kandidaten, Spiel.get_Karten())
    
    AnzahlGewinner = len(GewinnerSpieler)
    PotProGewinner = Spiel.get_Chips() // AnzahlGewinner if AnzahlGewinner else 0
    for Gewinner in GewinnerSpieler:
        Gewinner.add_Chips(PotProGewinner)

    Spiel.set_Gewinner(''.join(f'{Gewinner.get_Name()}, ' for Gewinner in GewinnerSpieler))
    Spiel.set_Gewinner(Spiel.get_Ergebnis().rstrip(', '))
    Spiel.set_Phase("showdown")
    Spiel.set_Nachricht(f"{Gewinner.get_Name()} gewinnt {Spiel.get_Chips()} Chips" + (f" mit {Ergebnis}." if Ergebnis else "."))
    Spiel.set_Chips(0)
