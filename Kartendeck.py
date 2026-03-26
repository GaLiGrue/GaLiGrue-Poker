import random
class Kartendeck:
    def __init__(self,Size=52):
        self.__Deck=['k2','k3','k4','k5','k6','k7','k8','k9','k10','kb','kd','kk','ka','h2','h3','h4','h5','h6','h7','h8','h9','h10','hb','hd','hk','ha','p2','p3','p4','p5','p6','p7','p8','p9','p10','pb','pd','pk','pa','s2','s3','s4','s5','s6','s7','s8','s9','s10','sb','sd','sk','sa']
        self.__Size=Size
    def get_Size(self):
        return self.__Size
    def set_size(self, Value):
        self.__Size=Value
    def new_Deck(self):
        '''neues und gemischtes Deck'''
        self.__Deck=['k2','k3','k4','k5','k6','k7','k8','k9','k10','kb','kd','kk','ka','h2','h3','h4','h5','h6','h7','h8','h9','h10','hb','hd','hk','ha','p2','p3','p4','p5','p6','p7','p8','p9','p10','pb','pd','pk','pa','s2','s3','s4','s5','s6','s7','s8','s9','s10','sb','sd','sk','sa']
        for i in range(500):
            Stelle1=random.randint(0,51)
            Stelle2=random.randint(0,51)
            self.__Deck[Stelle1],self.__Deck[Stelle2]=self.__Deck[Stelle2],self.__Deck[Stelle1]
    def get_Deck(self):
        return self.__Deck
    def give_Cards(self,Number):
        '''Gibt Karten aus'''
        Karten=[]
        for i in range(3):
            Karten.append(self.__Deck[52-self.__Size])
            self.__Size-=1
        return Karten
