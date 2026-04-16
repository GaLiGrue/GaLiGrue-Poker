from classes import Kartendeck
from classes import Player

def Kartengeben(AlleSpieler, Anzahl, Deck):
    '''Teilt jedem Spieler Anzahl Karten aus'''
    for Spieler in AlleSpieler:
        for _ in range(Anzahl):
            Karte = Deck.get_Card()
            Spieler.add_Karten([Karte])
    return AlleSpieler, Deck


        

