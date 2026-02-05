from Klassen import Spieler

Players = ['1', '2', '3']
SpielerAnz = len(Players)
Runde = 'Preflop'
AlleSpieler = []
Pott = 0
SmallBlind = 25
BigBlind = 50


for i in range(1, SpielerAnz + 1):
    Spieler1 = Spieler(Players[i - 1], 1000, i)
    AlleSpieler.append(Spieler1)
for i in range(SpielerAnz):
    if i == SpielerAnz - 1:
        AlleSpieler[i]._Spieler__Nächster = AlleSpieler[0]
    else:
        AlleSpieler[i]._Spieler__Nächster = AlleSpieler[i + 1]

# Spieler Positionen: 0 = Dealer, 1 = Small Blind, 2 = Big Blind, 3 = Erste Position nach Big Blind, usw.

def RundePreflop(AlleSpieler):
    global Pott
    for Spieler in AlleSpieler:
        if Spieler._Spieler__Position == 1:
            Spieler._Spieler__Chips -= SmallBlind
            Spieler._Spieler__ChipsGesetzt += SmallBlind
            Pott += SmallBlind
            SmallBlindPlayer = Spieler._Spieler__Name
            AktuellerSpieler = Spieler._Spieler__Nächster
            break

    AktuellerSpieler._Spieler__Chips -= BigBlind
    AktuellerSpieler._Spieler__ChipsGesetzt += BigBlind
    Pott += BigBlind
    LastRaiser = AktuellerSpieler
    AktuellerSpieler = AktuellerSpieler._Spieler__Nächster
    CallAmount = BigBlind

    while AktuellerSpieler != LastRaiser:
        if AktuellerSpieler._Spieler__IstDrin:
            Aktion = input(f'Spieler {AktuellerSpieler._Spieler__Name} Hier noch Aktion erhalten: ')
            match Aktion:
                case 'call':
                    GesetzterBetrag = CallAmount - AktuellerSpieler._Spieler__ChipsGesetzt
                    AktuellerSpieler._Spieler__Chips -= GesetzterBetrag
                    AktuellerSpieler._Spieler__ChipsGesetzt += GesetzterBetrag
                    Pott += GesetzterBetrag
                case 'fold':
                    AktuellerSpieler._Spieler__IstDrin = False
                case 'raise':
                    RaiseBetrag = int(input('Hier noch Betrag erhalten: '))
                    CallAmount = RaiseBetrag + AktuellerSpieler._Spieler__ChipsGesetzt
                    AktuellerSpieler._Spieler__Chips -= RaiseBetrag
                    AktuellerSpieler._Spieler__ChipsGesetzt += RaiseBetrag
                    Pott += RaiseBetrag
                    LastRaiser = AktuellerSpieler 
        
        AktuellerSpieler = AktuellerSpieler._Spieler__Nächster

    



RundePreflop(AlleSpieler)

for Spieler in AlleSpieler:
    print(f'Spieler: {Spieler._Spieler__Name}, Chips: {Spieler._Spieler__Chips}, Chips gesetzt: {Spieler._Spieler__ChipsGesetzt}, Ist drin: {Spieler._Spieler__IstDrin}')