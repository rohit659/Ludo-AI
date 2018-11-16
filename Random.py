from Strategy import *
from random import choice
class Random(Strategy):
    def __init__(self,name):
        Strategy.__init__(self,name)
    def getCoinToMove(self,idx,colors,face,noofplayers):
        lst = []
        for i in range(4):
            if colors[idx][i].ismovePossible(face):
                lst.append(i)
        x = choice(lst)
        # print(self.reward(idx,x,colors,face))
        return x
    
    