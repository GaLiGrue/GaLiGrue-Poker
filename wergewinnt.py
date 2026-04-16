from classes import Karte, Player, Mitte

def WerGewinnt(AlleSpieler, KartenMitte):
    """
    Alle Spieler vergleichen und den Gewinner bestimmen
    """
    def has_Flush(Karten):
        Counter = [[] for i in range(4)] # Speichert die Karten pro Suit
        for Karte in Karten:
            match Karte.get_Suit():
                case 'k':
                    Counter[0].append(Karte)
                case 'h':
                    Counter[1].append(Karte)
                case 'p':
                    Counter[2].append(Karte)
                case 's':
                    Counter[3].append(Karte)
        for Suit in Counter:
            if len(Suit) >= 5:
                Suitcopy = Suit.copy()
                Suitcopy.sort(key=lambda Karte: Karte.get_Value(), reverse=True) # Von höchster zu niedrigster Karte sortieren
                return True, Suitcopy
        return False, None
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
    
    Gewinner = Player('temp', 0, 'temp')
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
    