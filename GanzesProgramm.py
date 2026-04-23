import classes

def WerGewinnt(AlleSpieler, KartenMitte):
    """
    Alle Spieler vergleichen und den Gewinner bestimmen
    """
    def get_Hand(Karten):
        """
        Gibt die beste Hand außer Straßen und Flushes zurück
        Also Vierlinge, Full House, Drillinge, Zwei Paare, Ein Paar oder High Card
        """
        def has_Straight(Karten, Counter=None):
            if not Counter:
                Counter = [0 for _ in range(13)]
                for Karte in Karten:
                    Value = Karte.get_Value()
                    Counter[14 - Value] += 1 # Von höchster zu niedrigster Karte zählen
            for i in range(9):
                if CounterValue[i] >= 1 and CounterValue[i + 1] >= 1 and CounterValue[i + 2] >= 1 and CounterValue[i + 3] >= 1 and CounterValue[i + 4] >= 1:
                    return True, 14 - i
            if CounterValue[0] >= 1 and CounterValue[9] >= 1 and CounterValue[10] >= 1 and CounterValue[11] >= 1 and CounterValue[12] >= 1:
                return True, 5
            return False, None
        
        def get_Beikarten(CounterValue, Anzahl, exclude=[]):
            Beikarten = []
            for i in range(13):
                if i not in exclude and CounterValue[i] == 1:
                    Beikarten.append(i)
                    if len(Beikarten) == Anzahl:
                        break
            return Beikarten
        # Counter von den Karten erstellen
        CounterValue = [0 for _ in range(13)]
        for Karte in Karten:
            Value = Karte.get_Value()
            CounterValue[14 - Value] += 1 # Von höchster zu niedrigster Karte zählen
        CounterFaces = [[] for _ in range(4)]
        for Karte in Karten:
            match Karte.get_Suit():
                case 'k':
                    CounterFaces[0].append(Karte)
                case 'h':
                    CounterFaces[1].append(Karte)
                case 'p':
                    CounterFaces[2].append(Karte)
                case 's':
                    CounterFaces[3].append(Karte)
        
        
        # Prüft ob es eine Straße gibt
        Straight, StraightCard = has_Straight(Karten, CounterValue)

        # Prüft, ob es einen Flush gibt
        Flush = False
        for Suit in CounterFaces:
            if len(Suit) >= 5:
                Suitcopy = Suit.copy()
                Suitcopy.sort(key=lambda Karte: Karte.get_Value(), reverse=True) # Von höchster zu niedrigster Karte sortieren
                Flush = True
                FlushCards = Suitcopy[:5]
                break

        # Prüft, ob es einen Straight Flush gibt
        if Straight and Flush:
            StraightFlush, HighStraightFlushCard = has_Straight(FlushCards)
            if StraightFlush:
                return [0, HighStraightFlushCard] # StraightFlush, Handvalue = höchste Karte

        if 4 in CounterValue:
            Beikarten = get_Beikarten(CounterValue, 1, exclude=[CounterValue.index(4)]) # Eine Beikarte, die nicht zum Vierling gehört
            return [1, CounterValue.index(4)] + Beikarten # Vierling + höchste Beikarte
        if 3 in CounterValue and 2 in CounterValue:
            return [2, CounterValue.index(3), CounterValue.index(2)] # Full House
        
        if Flush:
            return [3, FlushCards[0].get_Value(), FlushCards[1].get_Value(), FlushCards[2].get_Value(), FlushCards[3].get_Value(), FlushCards[4].get_Value()] # Flush, Handvalue ist die höchste Karte des Flush
        if Straight:
            return [4, StraightCard] # Straight, Handvalue = höchste Karte

        if 3 in CounterValue:
            Beikarten = get_Beikarten(CounterValue, 2, exclude=[CounterValue.index(3)]) # Zwei Beikarten, die nicht zum Drilling gehören
            return [5, CounterValue.index(3)] + Beikarten # Drilling + zwei höchste Beikarten
        if CounterValue.count(2) >= 2:
            Beikarten = get_Beikarten(CounterValue, 1, exclude=[CounterValue.index(2), CounterValue.index(2, CounterValue.index(2) + 1)]) # Eine Beikarte, die nicht zu den Paaren gehört
            return [6, CounterValue.index(2), CounterValue.index(2, CounterValue.index(2) + 1), CounterValue.index(1)] # Zwei Paare + höchste Beikarte
        if 2 in CounterValue:
            Beikarten = get_Beikarten(CounterValue, 3, exclude=[CounterValue.index(2)]) # Drei Beikarten, die nicht zum Paar gehören
            return [7, CounterValue.index(2)] + Beikarten # Ein Paar + drei höchste Beikarten
        
        Beikarten = get_Beikarten(CounterValue, 5) # Fünf höchste Beikarten
        return [8] + Beikarten # Alle Kartenwerte zurückgeben, von höchster zu niedrigster Karte
    
    Gewinner = classes.Player('temp', 0, 'temp')
    Gewinner.set_Hand([9]) # Handvalue 9 ist die schlechteste Hand, damit jeder Spieler besser ist als der Gewinner am Anfang
    AlleGewinner = [Gewinner]
    for Spieler in AlleSpieler:
        if Spieler.get_IstDrin():
            Karten = Spieler.get_Karten()
            Karten.extend(KartenMitte.get_Karten())
            Hand = get_Hand(Karten)
            Spieler.set_Hand(Hand)
            
            # Hand ausgeben
            print(f'{Spieler.get_Name()} hat Hand {Spieler.get_Hand()}')
            
            # Spieler mit der besten Hand bestimmen
            if Spieler != Gewinner:
                SpielerHand = Spieler.get_Hand()
                GewinnerHand = Gewinner.get_Hand()
                for i in range(len(SpielerHand)):
                    if SpielerHand[i] < GewinnerHand[i]: # Spieler hat bessere Hand
                        Gewinner = Spieler
                        AlleGewinner = [Gewinner]
                        break
                    elif SpielerHand[i] > GewinnerHand[i]: # Gewinner hat bessere Hand
                        break
                    else: # Beide haben gleiche Hand, weiter vergleichen
                        continue
                else: # Beide haben exakt gleiche Hand, beide gewinnen
                    AlleGewinner.append(Spieler)

    return AlleGewinner

def AlleSpielerGleichziehen(AlleSpieler, Preflop, Mittelfeld):
    """
    Geht solgange, bis alle Spieler den gleichen Betrag gesetzt haben
    """
    Pott = 0
    CallAmount = 0
    SmallBlind = 25
    BigBlind = 50
    for Spieler in AlleSpieler: # ersten Spieler bestimmen
        if Spieler.get_Position() == 1:
            LastRaiser = Spieler
            AktuellerSpieler = Spieler # SmallBlind ist erster der dran ist
            if Preflop:   
                # SmallBlind setzen 
                Spieler.add_Chips(-SmallBlind)
                Spieler.set_ChipsGesetzt(SmallBlind)
                Pott += SmallBlind
                AktuellerSpieler = Spieler.get_Nächster()

                # BigBlind setzen
                AktuellerSpieler.add_Chips(-BigBlind)
                AktuellerSpieler.set_ChipsGesetzt(BigBlind)
                Pott += BigBlind
                LastRaiser = AktuellerSpieler
                AktuellerSpieler = AktuellerSpieler.get_Nächster()
                CallAmount = BigBlind

    AnzahlDrin = len(AlleSpieler)
    while True: # Bis alle gesetzt haben
        if AktuellerSpieler.get_IstDrin():  # Ob der Spieler noch drin ist
            Valid = False
            while not Valid: # Bis der Spieler eine valide Aktion gemacht hat
                GesetzterBetrag = CallAmount - AktuellerSpieler.get_ChipsGesetzt() # Muss er sowieso setzen
                
                # Informationen ausgeben
                Karten = AktuellerSpieler.get_Karten()
                MittelfeldKarten = Mittelfeld.get_Karten()
                print('\n'*20)
                print(f'Spieler {AktuellerSpieler.get_Name()} ist am Zug')
                print(f'Deine Karten: {[Karte.get_Name() for Karte in Karten]}')
                print(f'Mittelfeld Karten: {[Karte.get_Name() for Karte in MittelfeldKarten]}')
                print(f'aktuelle Chips: {AktuellerSpieler.get_Chips()}, Call Amount: {GesetzterBetrag}\n')
                
                Aktion = input(f'Spieler {AktuellerSpieler.get_Name()} Hier noch Aktion erhalten: ')
                match Aktion:
                    case 'call':
                        if GesetzterBetrag > AktuellerSpieler.get_Chips():
                            print('Wenn du All in gehen willst, schreibe "all in"')
                            Valid = False
                            continue
                        AktuellerSpieler.add_Chips(-GesetzterBetrag)
                        AktuellerSpieler.add_ChipsGesetzt(GesetzterBetrag)
                        Pott += GesetzterBetrag
                        Valid = True
                    case 'fold':
                        AktuellerSpieler.set_IstDrin(False)
                        AnzahlDrin -= 1
                        Valid = True
                    case 'raise':
                        Valid = True
                        RaiseBetrag = int(input('Hier noch Betrag erhalten: '))
                        if RaiseBetrag >= AktuellerSpieler.get_Chips():
                            print('Wenn du All in gehen willst, schreibe "all in"')
                            Valid = False
                            continue
                        if RaiseBetrag <= GesetzterBetrag:
                            print('Raise muss höher als Call sein')
                            Valid = False
                            continue
                        CallAmount += RaiseBetrag - GesetzterBetrag
                        AktuellerSpieler.add_Chips(-RaiseBetrag)
                        AktuellerSpieler.add_ChipsGesetzt(RaiseBetrag)
                        Pott += RaiseBetrag
                        LastRaiser = AktuellerSpieler
                    case 'all in':
                        RaiseBetrag = AktuellerSpieler.get_Chips()
                        AktuellerSpieler.set_AllIn(True)
                        if RaiseBetrag > GesetzterBetrag:
                            CallAmount += RaiseBetrag - GesetzterBetrag
                            LastRaiser = AktuellerSpieler
                        AktuellerSpieler.add_Chips(-RaiseBetrag)
                        AktuellerSpieler.add_ChipsGesetzt(RaiseBetrag)
                        Pott += RaiseBetrag
                        Valid = True
                    case _:
                        print('Bitte nochmal(invalide Eingabe)')
        AktuellerSpieler = AktuellerSpieler.get_Nächster()
        if AktuellerSpieler == LastRaiser: # Abbruchbedingung
            break
        if AnzahlDrin == 1: # Wenn nur noch ein Spieler übrig ist, wird der Pott diesem Spieler gegeben
            break
    Mittelfeld.add_Chips(Pott)
    return Mittelfeld, AlleSpieler

def Kartengeben(AlleSpieler, Anzahl, Deck):
    '''Teilt jedem Spieler Anzahl Karten aus'''
    for Spieler in AlleSpieler:
        for _ in range(Anzahl):
            Karte = Deck.get_Card()
            Spieler.add_Karten([Karte])
    return AlleSpieler, Deck

# Spieler erstellen
SpielerAnzahl = int(input('Spieler Anzahl: '))
AlleSpieler = []
for i in range(1, SpielerAnzahl + 1):
    Spieler1 = classes.Player(1000, i, f'Spieler {i}')
    AlleSpieler.append(Spieler1)
for i in range(SpielerAnzahl):
    if i == SpielerAnzahl - 1:
        AlleSpieler[i].set_Nächster(AlleSpieler[0])
    else:
        AlleSpieler[i].set_Nächster(AlleSpieler[i + 1])

while True:
    # Deck erstellen
    Deck = classes.Kartendeck()

    # Mittelfeld erstellen
    KartenMitte = classes.Mitte(0)

    # erste Karten austeilen
    AlleSpieler, Deck = Kartengeben(AlleSpieler, 2, Deck)

    # Preflop spielen
    KartenMitte, AlleSpieler = AlleSpielerGleichziehen(AlleSpieler, True, KartenMitte)

    # Flop
    KartenMittenliste, Deck = Kartengeben([KartenMitte], 3, Deck)
    KartenMitte = KartenMittenliste[0]
    KartenMitte, AlleSpieler = AlleSpielerGleichziehen(AlleSpieler, False, KartenMitte)

    # Turn
    KartenMittenliste, Deck = Kartengeben([KartenMitte], 1, Deck)
    KartenMitte = KartenMittenliste[0]
    KartenMitte, AlleSpieler = AlleSpielerGleichziehen(AlleSpieler, False, KartenMitte)

    # River
    KartenMittenliste, Deck = Kartengeben([KartenMitte], 1, Deck)
    KartenMitte = KartenMittenliste[0]
    KartenMitte, AlleSpieler = AlleSpielerGleichziehen(AlleSpieler, False, KartenMitte)

    # Gewinner bestimmen
    AlleGewinner = WerGewinnt(AlleSpieler, KartenMitte)
    for Gewinner in AlleGewinner:
        print(f'{Gewinner.get_Name()} gewinnt {KartenMitte.get_Chips() // len(AlleGewinner)} Chips')
        Gewinner.add_Chips(KartenMitte.get_Chips() // len(AlleGewinner))
    
    
    for Player in AlleSpieler:
        print(f'{Player.get_Name()} hat {Player.get_Chips()} Chips')
        Player.clear_Karten()
        Player.set_IstDrin(True)
        Player.set_ChipsGesetzt(0)
        Player.set_Hand(None)
        Player.rotiere_Position(SpielerAnzahl)
        
    Beenden = input('Soll das Spiel beendet werden: ')
    if Beenden == 'ja':
        break
    
Gewinner = AlleSpieler[0]
for Player in AlleSpieler:
    if Player.get_Chips() > Gewinner.get_Chips():
        Gewinner = Player
print(f'{Gewinner.get_Name()} gewinnt das Spiel mit {Gewinner.get_Chips()} Chips')    
