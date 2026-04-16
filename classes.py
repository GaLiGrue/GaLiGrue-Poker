import random

class Aktionen:
    def __init__(self,Chips):
        '''Konstruktor für die Klasse Aktionen'''
        self.__Chips = Chips
        self.__Karten = []

    def get_Chips(self):
        return self.__Chips
    def set_Chips(self, Value):
        self.__Chips = Value
    def add_Chips(self, Value):
        '''Wert auf den Chips addieren'''
        self.__Chips += Value
    def sub_Chips(self, Value):
        '''Wert auf den Chips Subtrahieren'''
        self.__Chips -= Value
    def get_Karten(self):
        return self.__Karten
    def set_Karten(self,Value):
        self.__Karten = Value
    def add_Karten(self, Value:list):
        self.__Karten.extend(Value)
    def clear_Karten(self):
        '''Die Liste der Karten leeren'''
        self.__Karten=[]
class Player(Aktionen):
    def __init__(self,Chips,Position,Name):
        super().__init__(Chips)
        self.__Name = Name
        self.__Position = Position
        self.__Nächster = None
        self.__ChipsGesetzt = 0
        self.__IstDrin = True
        self.__AllIn = False
        self.__Hand = None
    def get_Position(self):
        return self.__Position
    def set_Position(self, Value):
        self.__Position = Value
    def rotiere_Position(self, SpielerAnzahl):
        '''Die Position des Spielers um 1 erhöhen, wenn sie größer als die Anzahl der Spieler ist, wird sie auf 1 zurückgesetzt'''
        self.__Position += 1
        if self.__Position > SpielerAnzahl:
            self.__Position = 1
    def get_Name(self):
        return self.__Name
    def set_Name(self, Value):
        self.__Name=Value
    def get_Hand(self):
        return self.__Hand
    def set_Hand(self, Value):
        self.__Hand=Value
    def get_Nächster(self):
        return self.__Nächster
    def set_Nächster(self, Value):
        self.__Nächster=Value
    def get_IstDrin(self):
        return self.__IstDrin
    def set_IstDrin(self, Value):
        self.__IstDrin=Value
    def get_ChipsGesetzt(self):
        return self.__ChipsGesetzt
    def set_ChipsGesetzt(self, Value):
        self.__ChipsGesetzt=Value
    def add_ChipsGesetzt(self, Value):
        self.__ChipsGesetzt+=Value
    def get_AllIn(self):
        return self.__AllIn
    def set_AllIn(self, Value):
        self.__AllIn = Value
class Mitte(Aktionen):
    def __init__(self,Chips):
        super().__init__(Chips)

class Karte:
    def __init__(self, Name):
        self.__Name = Name
        self.__Suit = Name[0]
        self.__Value = int(Name[1:])
    def get_Name(self):
        return self.__Name
    def get_Suit(self):
        return self.__Suit
    def get_Value(self):
        return self.__Value

class Kartendeck():
    def __init__(self):
        Liste = ['k2','k3','k4','k5','k6','k7','k8','k9','k10','k11','k12','k13','k14','h2','h3','h4','h5','h6','h7','h8','h9','h10','h11','h12','h13','h14','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12','p13','p14','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14']
        random.shuffle(Liste)
        self.__Deck = []
        for Name in Liste:
            Card = Karte(Name)
            self.__Deck.append(Card)
        self.__Size = len(self.get_Deck())
    def get_Size(self):
        return self.__Size
    def set_size(self, Value):
        self.__Size = Value
    def get_Deck(self):
        return self.__Deck
    def get_Card(self) -> object:
        """
        gibt die erste Karte vom Kartendeck
        """
        Card = self.__Deck.pop()
        return Card
