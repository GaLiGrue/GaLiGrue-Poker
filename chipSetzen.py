from classes import Player

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