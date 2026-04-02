import random

class Aktionen:
    def __init__(self,Chips):
        '''Konstruktor für die Klasse Aktionen'''
        self.__Chips= Chips
        self.__Karten=[]

    def get_Chips(self):
        return self.__Chips
    def set_Chips(self, Value):
        self.__Chips=Value
    def add_Chips(self, Value):
        '''Wert auf den Chips addieren'''
        self.__Chips+=Value
    def sub_Chips(self, Value):
        '''Wert auf den Chips Subtrahieren'''
        self.__Chips-=Value
    def get_Karten(self):
        return self.__Karten
    def set_Karten(self,Value):
        self.__Karten=Value
    def add_Karten(self, Value):
        '''Wert auf den Chips addieren'''
        self.__Karten.append(Value)
    def clear_Karten(self):
        '''Die Liste der Karten leeren'''
        self.__Karten=[]
class Spieler(Aktionen):
    def __init__(self,Chips,Position,Name):
        super().__init__(Chips)
        self.__Name = Name
        self.__Position = Position
        self.__Nächster = None
        self.__ChipsGesetzt = 0
        self.__IstDrin = True
    def get_Position(self):
        return self.__Position
    def set_Position(self, Value):
        self.__Position=Value
    def get_Name(self):
        return self.__Name
    def set_Name(self, Value):
        self.__Name=Value
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
class Mitte(Aktionen):
    def __init__(self,Chips,Karten):
        super().__init__(Chips)
    def flop(self,Karten):
        '''Fügt drei Karten bei der Mitte hinzu'''
        self.__Karten.extend(Karten)

class Karte:
    def __init__(self, Name):
        self.__Name = Name
    def get_Name(self):
        return self.__Name
class Kartendeck():
    def __init__(self):
        Liste = ['k2','k3','k4','k5','k6','k7','k8','k9','k10','kb','kd','kk','ka','h2','h3','h4','h5','h6','h7','h8','h9','h10','hb','hd','hk','ha','p2','p3','p4','p5','p6','p7','p8','p9','p10','pb','pd','pk','pa','s2','s3','s4','s5','s6','s7','s8','s9','s10','sb','sd','sk','sa']
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
        print(Card.get_Name())
        return Card
