from Strategy import *
class Defensive(Strategy):
    def __init__(self,name):
        Strategy.__init__(self,name)
    
    def checkatcords(self,idx,nx,ny):
        for i in range(4):
            if i == idx :
                continue
            for j in range(4):
                curx=colors[i][j].cur_x
                cury=colors[i][j].cur_y
                if curx==nx and  cury==ny :
                    return 1   

        return 0


    def getDangerLevel(self,idx,colors,face):
        dangerlist=[3,3,3,3]

        for coin in range(4):
            curx=colors[idx][coin].cur_x
            cury=colors[idx][coin].cur_y
            minn=1000
            if colors[idx][coin].ismovePossible(face)==0:
                dangerlist[coin]=-1
                continue
            cnt=0
            for i in range(4):
                if i== idx:
                    continue 
                for j in range(4):
                    pind=colors[i][j].pathindex
                    if pind == -1:
                        continue
                    maxpind=len(colors[i][j].path_list)
                    cnt=0
                    for k in range(pind,maxpind,1):
                        nx=colors[i][j].path_list[k][0]
                        ny=colors[i][j].path_list[k][1]
                        cnt+=1
                        if nx==curx and ny==cury:
                            minn=min(minn,cnt)
                            break

            if minn<=5 and (colors[idx][coin].pathindex==-1 or colors[idx][coin].path_list[colors[idx][coin].pathindex][2]==0) :
                dangerlist[coin]=0
            elif  minn <=11:
                dangerlist[coin]=1
            elif minn<=17:
                dangerlist[coin]=2
            else:
                dangerlist[coin]=3
                         
            
        
        
        return dangerlist


    def getpiecelist(self,level,dangerlist):
        Dlist=[]

        for i in range(4):
            if dangerlist[i]==level:
                Dlist.append(i)

        return Dlist

    def TieBreakAtZero(self,Dlist0,Dlist0sz,colors,idx):
          if Dlist0sz==1:
              return Dlist0[0]
          else:
              maxx=0
              for i in Dlist0:
                  pind=colors[idx][i].pathindex
                  maxx=max(maxx,pind)

              for i in Dlist0:
                   pind=colors[idx][i].pathindex
                   if pind==maxx:
                       return i
    
    
    def getSafecoins(self,idx,colors,face,Dlist1,Dlist1sz):

        safecoins=[0,0,0,0]

        for i in Dlist1:
            pind=colors[idx][i].pathindex
            if pind == -1:
                pind = -6
            if colors[idx][i].path_list[pind+face][2]==1:
                safecoins[i]=1
        maxx=-2
        for i in Dlist1:
            pind=colors[idx][i].pathindex
            if safecoins[i]==1:
                maxx=max(maxx,pind)
        
        for i in Dlist1:
            pind=colors[idx][i].pathindex
            if pind==maxx:
                return i
        return -1



    def TieBreakAtOne(self,Dlist1,Dlist1sz,colors,idx,face):

        coin=self.getSafecoins(idx,colors,face,Dlist1,Dlist1sz)
        return coin
        
        
    def getGoodDefensiveCoin(self,idx,face,colors):

        inDanger=[0,0,0,0]

        for coins in range(4):
            pind=colors[idx][coins].pathindex
            if colors[idx][coins].ismovePossible(face)==0:
                continue
            face1 = 1
            if pind == -1:
                face1 = 1
            else:
                face1 = face
            for move in range(0,face1):
                if pind+move == -1:
                    continue
                nx=colors[idx][coins].path_list[pind+move][0]
                ny=colors[idx][coins].path_list[pind+move][1]

                for i in range(4):
                    if i==idx:
                        continue
                    for j in range(4):
                        curx=colors[i][j].cur_x
                        cury=colors[i][j].cur_y
                        if curx==nx and cury==ny:
                            inDanger[coins]=1

            for i in range(4):
                if colors[idx][i].ismovePossible(face) and inDanger[i] == 0:
                    return i
            for i in range(4):
                if colors[idx][i].ismovePossible(face):
                    return i
            

    def getCoinToMove(self,idx,colors,face,noofplayers):


        #wo jail ka kuch dekhna hai   


        dangerlist=self.getDangerLevel(idx,colors,face)
        
        Dlist0=self.getpiecelist(0,dangerlist)
        Dlist0sz=len(Dlist0)

        Dlist1=self.getpiecelist(1,dangerlist)
        Dlist1sz=len(Dlist1)
        
        Dlist2=self.getpiecelist(2,dangerlist)
        Dlist2sz=len(Dlist2)
        
        Dlist3=self.getpiecelist(3,dangerlist)
        Dlist3sz=len(Dlist3)

        if Dlist0sz!=0:
            print('Here in 0***********')
            return self.TieBreakAtZero(Dlist0,Dlist0sz,colors,idx)
        elif Dlist1sz!=0 and self.TieBreakAtOne(Dlist1,Dlist1sz,colors,idx,face)!=-1:
            print('Here in 1***********')
            return self.TieBreakAtOne(Dlist1,Dlist1sz,colors,idx,face)
        elif  Dlist2sz!=0 and self.TieBreakAtOne(Dlist2,Dlist2sz,colors,idx,face)!=-1:
            print('Here in 2***********')
            return self.TieBreakAtOne(Dlist2,Dlist2sz,colors,idx,face) 
        elif  Dlist3sz!=0 and self.TieBreakAtOne(Dlist3,Dlist3sz,colors,idx,face)!=-1:
            print('Here in 3*********')
            return self.TieBreakAtOne(Dlist3,Dlist3sz,colors,idx,face) 
        else :
            print('Here in else')
            return self.getGoodDefensiveCoin(idx,face,colors)

        


            


















        