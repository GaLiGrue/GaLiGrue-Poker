class Spieler:
    def __init__(self, Name, Chips, Position):
        self.__Name = Name
        self.__Chips = Chips
        self.__Karten = []
        self.__Position = Position
        self.__Nächster = None
        self.__ChipsGesetzt = 0
        self.__IstDrin = True
