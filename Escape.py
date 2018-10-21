from Strategy import *
class Escape(Strategy):
    def __init__(self,name):
        Strategy.__init__(self,name)
    def getCoinToMove(self,idx,colors,face):
        maxx=-2
        ind=-1
        for i in range(4):
            if colors[idx][i].ismovePossible(face):
                if colors[idx][i].pathindex > maxx:
                    maxx=colors[idx][i].pathindex
                    ind=i


        return ind






