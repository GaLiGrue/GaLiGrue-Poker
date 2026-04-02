from Bauteil_Spieler_Mitte import Spieler

Players = ['1', '2', '3']
SpielerAnz = len(Players)
Runde = 'Preflop'
AlleSpieler = []
Pott = 0
SmallBlind = 25
BigBlind = 50


for i in range(1, SpielerAnz + 1):
    Spieler1 = Spieler(1000, i, Players[i - 1])
    AlleSpieler.append(Spieler1)
for i in range(SpielerAnz):
    if i == SpielerAnz - 1:
        AlleSpieler[i]._Spieler__Nächster = AlleSpieler[0]
    else:
        AlleSpieler[i]._Spieler__Nächster = AlleSpieler[i + 1]

# Spieler Positionen: 0 = Dealer, 1 = Small Blind, 2 = Big Blind, 3 = Erste Position nach Big Blind, usw.

def AlleSpielerGleichziehen(AlleSpieler, Preflop = False):
    """
    Geht solgange, bis alle Spieler den gleichen Betrag gesetzt haben
    """
    Pott = 0
    CallAmount = 0
    for Spieler in AlleSpieler: # ersten Spieler bestimmen
        Spieler.set_ChipsGesetzt(0)
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

    while True: # Bis alle gesetzt haben
        if AktuellerSpieler.get_IstDrin():  # Ob der Spieler noch drin ist
            Valid = False
            while not Valid: # Bis der Spieler eine valide Aktion gemacht hat
                GesetzterBetrag = CallAmount - AktuellerSpieler.get_ChipsGesetzt() # Muss er sowieso setzen
                print(f'aktuelle Chips: {AktuellerSpieler.get_Chips()}, Call Amount: {GesetzterBetrag}')
                Aktion = input(f'Spieler {AktuellerSpieler.get_Name()} Hier noch Aktion erhalten: ')
                match Aktion:
                    case 'call':
                        if GesetzterBetrag > AktuellerSpieler.get_Chips():
                            GesetzterBetrag = AktuellerSpieler.get_Chips() # All in
                        AktuellerSpieler.add_Chips(-GesetzterBetrag)
                        AktuellerSpieler.add_ChipsGesetzt(GesetzterBetrag)
                        Pott += GesetzterBetrag
                        Valid = True
                    case 'fold':
                        AktuellerSpieler.set_IstDrin(False)
                        Valid = True
                    case 'raise':
                        if not Preflop:
                            Valid = True
                            RaiseBetrag = int(input('Hier noch Betrag erhalten: '))
                            if RaiseBetrag >= AktuellerSpieler.get_Chips():
                                RaiseBetrag = AktuellerSpieler.get_Chips() # All in
                            if RaiseBetrag <= GesetzterBetrag:
                                print('Raise muss höher als Call sein')
                                Valid = False
                                continue
                            CallAmount += RaiseBetrag - GesetzterBetrag
                            AktuellerSpieler.add_Chips(-RaiseBetrag)
                            AktuellerSpieler.add_ChipsGesetzt(RaiseBetrag)
                            Pott += RaiseBetrag
                            LastRaiser = AktuellerSpieler
                        else:
                            print('Du darfst nicht in Preflop raisen')
                    case _:
                        print('Bitte nochmal(invalide Eingabe)')
        AktuellerSpieler = AktuellerSpieler.get_Nächster()
        if AktuellerSpieler == LastRaiser: # Abbruchbedingung
            break
    return Pott, AlleSpieler

Pott = 0


# Main Spiel Loop
# Preflop
NeuerPott, AlleSpieler = AlleSpielerGleichziehen(AlleSpieler, True)
Pott += NeuerPott
print(NeuerPott)
for Player in AlleSpieler:
    print(f'Spieler: {Player.get_Name()}, Chips: {Player.get_Chips()}, Ist drin: {Player.get_IstDrin()}')

# Normale Runden
for i in range(3):
    NeuerPott, AlleSpieler = AlleSpielerGleichziehen(AlleSpieler, False)
    print(NeuerPott)
    for Player in AlleSpieler:
        print(f'Spieler: {Player.get_Name()}, Chips: {Player.get_Chips()}, Ist drin: {Player.get_IstDrin()}')
