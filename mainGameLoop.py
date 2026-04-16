from classes import Kartendeck, Mitte, Player
import Kartengeben, chipSetzen, wergewinnt
# Spieler erstellen
SpielerAnzahl = int(input('Spieler Anzahl: '))
AlleSpieler = []
for i in range(1, SpielerAnzahl + 1):
    Spieler1 = Player(1000, i, f'Spieler {i}')
    AlleSpieler.append(Spieler1)
for i in range(SpielerAnzahl):
    if i == SpielerAnzahl - 1:
        AlleSpieler[i].set_Nächster(AlleSpieler[0])
    else:
        AlleSpieler[i].set_Nächster(AlleSpieler[i + 1])

while True:
    # Deck erstellen
    Deck = Kartendeck()

    # Mittelfeld erstellen
    KartenMitte = Mitte(0)

    # erste Karten austeilen
    AlleSpieler, Deck = Kartengeben.Kartengeben(AlleSpieler, 2, Deck)

    # Preflop spielen
    KartenMitte, AlleSpieler = chipSetzen.AlleSpielerGleichziehen(AlleSpieler, True, KartenMitte)

    # Flop
    KartenMittenliste, Deck = Kartengeben.Kartengeben([KartenMitte], 3, Deck)
    KartenMitte = KartenMittenliste[0]
    KartenMitte, AlleSpieler = chipSetzen.AlleSpielerGleichziehen(AlleSpieler, False, KartenMitte)

    # Turn
    KartenMittenliste, Deck = Kartengeben.Kartengeben([KartenMitte], 1, Deck)
    KartenMitte = KartenMittenliste[0]
    KartenMitte, AlleSpieler = chipSetzen.AlleSpielerGleichziehen(AlleSpieler, False, KartenMitte)

    # River
    KartenMittenliste, Deck = Kartengeben.Kartengeben([KartenMitte], 1, Deck)
    KartenMitte = KartenMittenliste[0]
    KartenMitte, AlleSpieler = chipSetzen.AlleSpielerGleichziehen(AlleSpieler, False, KartenMitte)

    # Gewinner bestimmen
    AlleGewinner = wergewinnt.WerGewinnt(AlleSpieler, KartenMitte)
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
