import Kartendeck
import Bauteil_Spieler_Mitte

Deck=Kartendeck.Kartendeck()

SpielerAnz=int(input('Spieler Anzahl:'))
AlleSpieler = []
for i in range(1, SpielerAnz + 1):
    Spieler1 = Bauteil_Spieler_Mitte.Spieler(i,'Spieler')
    AlleSpieler.append(Spieler1)
print(AlleSpieler)
ja=(AlleSpieler[1].get_IstDrin())
print(ja)


        

