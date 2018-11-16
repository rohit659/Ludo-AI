from Strategy import *
class Escape(Strategy):
    def __init__(self,name):
        Strategy.__init__(self,name)
    def getCoinToMove(self,idx,colors,face,noofplayers):
        maxx=-2
        ind=-1
        for i in range(4):
            if colors[idx][i].ismovePossible(face):
                if colors[idx][i].pathindex > maxx:
                    maxx=colors[idx][i].pathindex
                    ind=i

        print("#########3")
        print(self.reward(idx,ind,colors,face))
        return ind
    

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
            
    def reward(self,idx,n,colors,face):
        pathini = colors[idx][n].pathindex
        dangerlist = self.getDangerLevel(idx, colors,face)
        prevdanger = dangerlist[n]
        pathind = colors[idx][n].pathindex + face


        cnt = 0
        # if won
        if(pathind == len(colors[idx][n].path_list)-1):
                return 1


        # realising a piece from jail
        if pathini == -1 and face == 6:
            return 0.25
        
        npos = colors[idx][n].pathindex + face
        if colors[idx][n].path_list[npos][2] == 1:
            return 0.35
        else:
            nx = colors[idx][n].path_list[npos][0]
            ny = colors[idx][n].path_list[npos][1]
            #  knocking an opponent’s piece
            for coin in range(0, 4):
                if coin != idx:
                    for i in range(0, 4):
                        if colors[coin][i].cur_x == nx and colors[coin][i].cur_y == ny:
                            cnt = cnt+1
            if cnt == 1:
                return 0.4

        colors[idx][n].pathindex  = colors[idx][n].pathindex + face
        colors[idx][n].cur_x = colors[idx][n].path_list[colors[idx][n].pathindex][0]
        colors[idx][n].cur_y = colors[idx][n].path_list[colors[idx][n].pathindex][1]

        dangerlist = self.getDangerLevel(idx, colors,face)
        currdanger = dangerlist[n]
        colors[idx][n].pathindex = colors[idx][n].pathindex - face
        colors[idx][n].cur_x = colors[idx][n].path_list[colors[idx][n].pathindex][0]
        colors[idx][n].cur_y = colors[idx][n].path_list[colors[idx][n].pathindex][1]

        print("hehhe")
        print(prevdanger)
        print(currdanger)
        # defending a vulnerable piece
        if prevdanger < currdanger :
            return ((currdanger-prevdanger)/3)*0.75
        # for getting a piece knocked in the next turn    
        elif prevdanger > currdanger:
            return -((prevdanger-currdanger)/3)*0.75  



        

        # forming a blockade
        cnt = 0
        for i in range(0, 4):
            if i != n:
                if colors[idx][i].pathindex == pathind:
                    cnt = cnt+1
        if cnt > 1:
            return 0.05

        #  moving the piece that is closest to home.
        return pathind/56  
    
     

        
        






