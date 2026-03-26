class Aktionen:
    def __init__(self,Chips):
        '''Konstruktor für die Klasse Aktionen'''
        self.__Chips=Chips
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
    def __init__(self,Position,Name):
        super().__init__(1000)
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
        '''Wert auf ChipsGesetzt addieren'''
        self.__ChipsGesetzt+=Value  
class Mitte(Aktionen):
    def __init__(self,Karten):
        super().__init__(0)
    def flop(self,Karten):
        '''Fügt drei Karten bei der Mitte hinzu'''
        self.__Karten.extend(Karten)