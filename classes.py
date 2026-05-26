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
    def __init__(self,Chips,Name,ClientName):
        super().__init__(Chips)
        self.__Name = Name
        self.__Nächster = None
        self.__ChipsGesetzt = 0
        self.__IstDrin = True
        self.__AllIn = False
        self.__Hand = None
        self.__ClientName = ClientName
        self.__Gehandelt = False
        self.__Eliminiert = False
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
    def get_ClientName(self):
        return self.__ClientName
    def set_ClientName(self, Value):
        self.__ClientName=Value
    def get_Gehandelt(self):
        return self.__Gehandelt
    def set_Gehandelt(self, Value):
        self.__Gehandelt=Value
    def get_Eliminiert(self):
        return self.__Eliminiert
    def set_Eliminiert(self, Value):
        self.__Eliminiert = Value

class Mitte(Aktionen):
    def __init__(self):
        super().__init__(0)

class Spiel:
    def __init__(self, SpielId, Modus, HostId, SpielerListe):
        '''Konstruktor fuer die Klasse Spiel'''
        self.__Id = SpielId
        self.__Modus = Modus
        self.__HostId = str(HostId)
        self.__Deck = self.erstelle_deck()
        self.__Spieler = SpielerListe
        self.__Gemeinschaftskarten = []
        self.__Pot = 0
        self.__AktuellerEinsatz = 0
        self.__Phase = "lobby"
        self.__ZugIndex = 0
        self.__Nachricht = "Warte auf Spieler."
        self.__Gewinner = None
        self.__LetzteAktion = None
        self.__Gestartet = False
        self.__BlindIndex = 0

    def get_Id(self):
        return self.__Id
    def set_Id(self, Value):
        self.__Id = Value
    def get_Modus(self):
        return self.__Modus
    def set_Modus(self, Value):
        self.__Modus = Value
    def get_HostId(self):
        return self.__HostId
    def set_HostId(self, Value):
        self.__HostId = str(Value)
    def get_Deck(self):
        return self.__Deck
    def set_Deck(self, Value):
        self.__Deck = Value
    def get_Spieler(self):
        return self.__Spieler
    def set_Spieler(self, Value):
        self.__Spieler = Value
    def get_Gemeinschaftskarten(self):
        return self.__Gemeinschaftskarten
    def set_Gemeinschaftskarten(self, Value):
        self.__Gemeinschaftskarten = Value
    def add_Gemeinschaftskarten(self, Value):
        self.__Gemeinschaftskarten.extend(Value)
    def get_Pot(self):
        return self.__Pot
    def set_Pot(self, Value):
        self.__Pot = Value
    def add_Pot(self, Value):
        self.__Pot += Value
    def get_AktuellerEinsatz(self):
        return self.__AktuellerEinsatz
    def set_AktuellerEinsatz(self, Value):
        self.__AktuellerEinsatz = Value
    def get_Phase(self):
        return self.__Phase
    def set_Phase(self, Value):
        self.__Phase = Value
    def get_ZugIndex(self):
        return self.__ZugIndex
    def set_ZugIndex(self, Value):
        self.__ZugIndex = Value
    def get_Nachricht(self):
        return self.__Nachricht
    def set_Nachricht(self, Value):
        self.__Nachricht = Value
    def add_Nachricht(self, Value):
        self.__Nachricht += Value
    def get_Gewinner(self):
        return self.__Gewinner
    def set_Gewinner(self, Value):
        self.__Gewinner = Value
    def get_LetzteAktion(self):
        return self.__LetzteAktion
    def set_LetzteAktion(self, Value):
        self.__LetzteAktion = Value
    def get_Gestartet(self):
        return self.__Gestartet
    def set_Gestartet(self, Value):
        self.__Gestartet = Value
    def get_BlindIndex(self):
        return self.__BlindIndex
    def set_BlindIndex(self, Value):
        self.__BlindIndex = Value
    
    def erstelle_deck(self):
        '''Erstellt ein neues Kartendeck mit 52 Karten und shuffelt es.'''
        liste = ['k2','k3','k4','k5','k6','k7','k8','k9','k10','k11','k12','k13','k14',
                 'h2','h3','h4','h5','h6','h7','h8','h9','h10','h11','h12','h13','h14',
                 'p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12','p13','p14',
                 's2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14']
        random.shuffle(liste)
        deck = [Karte(name) for name in liste]
        return deck
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

    def get_image_path(self):
        SUIT_MAP = {
            'k': 'clubs',
            'h': 'hearts',
            'p': 'spades',
            's': 'diamonds'
        }

        suit_folder = SUIT_MAP[self.get_Suit()]
        value = self.get_Value()

        if value <= 10:
            filename = f"card_{value - 1}.svg"
        elif value == 11:
            filename = "jack.svg"
        elif value == 12:
            filename = "queen.svg"
        elif value == 13:
            filename = "king.svg"
        elif value == 14:
            filename = "ace.svg"
        return f"cards/{suit_folder}/{filename}"
