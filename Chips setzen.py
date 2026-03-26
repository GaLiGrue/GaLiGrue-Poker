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

def AlleSpielerGleichziehen(AlleSpieler, AktuellerSpieler, Pott, LastRaiser = None, CallAmount = 0):
    """
    Geht solgange, bis alle Spieler den gleichen Betrag gesetzt haben
    """
    while AktuellerSpieler != LastRaiser: # Bis alle gesetzt haben
        if AktuellerSpieler.get_IstDrin():  # Ob der Spieler noch drin ist
            Valid = False
            while not Valid: # Bis der Spieler eine valide Aktion gemacht hat
                Aktion = input(f'Spieler {AktuellerSpieler.get_Name()} Hier noch Aktion erhalten: ')
                match Aktion:
                    case 'call':
                        GesetzterBetrag = CallAmount - AktuellerSpieler.get_ChipsGesetzt()
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
                        Valid = True
                        RaiseBetrag = int(input('Hier noch Betrag erhalten: '))
                        GesetzterBetrag = CallAmount - AktuellerSpieler.get_ChipsGesetzt() # Das muss er soqieso setzten
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
                    case _:
                        'Bitte nochmal(invalide Eingabe)'
        AktuellerSpieler = AktuellerSpieler.get_Nächster()
    return Pott

def RundePreflop(AlleSpieler):
    # Small und Big Blind
    global Pott
    for Spieler in AlleSpieler:
        if Spieler.get_Position() == 1:
            Spieler.add_Chips(-SmallBlind)
            Spieler.set_ChipsGesetzt(SmallBlind)
            Pott += SmallBlind
            SmallBlindPlayer = Spieler.get_Name()
            AktuellerSpieler = Spieler.get_Nächster()
            break

    AktuellerSpieler.add_Chips(-BigBlind)
    AktuellerSpieler.set_ChipsGesetzt(BigBlind)
    Pott += BigBlind
    LastRaiser = AktuellerSpieler
    AktuellerSpieler = AktuellerSpieler.get_Nächster()
    CallAmount = BigBlind

    Pott = AlleSpielerGleichziehen(AlleSpieler, AktuellerSpieler, Pott, LastRaiser, CallAmount)

    
        
        

    



RundePreflop(AlleSpieler)

for Player in AlleSpieler:
    print(f'Spieler: {Player.get_Name()}, Chips: {Player.get_Chips()}, Chips gesetzt: {Player.get_ChipsGesetzt()}, Ist drin: {Player.get_IstDrin()}')