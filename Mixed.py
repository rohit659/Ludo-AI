from random import seed
from random import choice
from Strategy import *
from Attacking import *
from Defensive import *
from Escape import *
from Random import *
class Mixed(Strategy):
    def __init__(self,name):
        Strategy.__init__(self,name)
        self.attack = Attacking("Attacking")
        self.defense = Defensive("Defensive")
        self.escape = Escape("Escape")
        self.randomm = Random("Random")
    def getCoinToMove(self,idx,colors,face,noofplayers):
        i = choice(range(1,100))
        if i<=32:
            return self.attack.getCoinToMove(idx,colors,face,noofplayers)
        elif i<=64:
            return self.defense.getCoinToMove(idx,colors,face,noofplayers)
        elif i<=96:
            return self.escape.getCoinToMove(idx,colors,face,noofplayers)
        else:
            return self.randomm.getCoinToMove(idx,colors,face,noofplayers)
            
        

