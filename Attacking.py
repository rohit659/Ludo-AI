from Strategy import *
class Attacking(Strategy):
    def __init__(self,name):
        Strategy.__init__(self,name)
    def getCoinToMove(self,idx,colors,face):
        minDist1 = [100,100,100,100]
        mn1 = 100
        minDist2 = [100,100,100,100]
        mn2 = 100
        for i in range(4):
            if colors[idx][i].ismovePossible(face):
                if colors[idx][i].isatjail():
                    npos = 0
                else:
                    npos = colors[idx][i].pathindex + face
                print("hurrah")
                print(len(colors[idx][i].path_list))  
                for pos in range(npos,len(colors[idx][i].path_list)):
                    p = colors[idx][i].path_list[pos][2]
                    nx = colors[idx][i].path_list[pos][0]
                    ny = colors[idx][i].path_list[pos][1]
                    c = 0
                    for k in range(0,4):
                        if k != idx:
                            for j in range(0,4):
                                if colors[k][j].cur_x == nx and colors[k][j].cur_y == ny :
                                    c += 1
                    if c == 1 and p==0 and pos == npos:
                        minDist1[i] = pos - npos
                        if mn1 > minDist1[i]:
                            mn1 = minDist1[i]
                        break
                    elif c>0:
                        minDist2[i] = pos - npos
                        if mn2 > minDist2[i]:
                            mn2 = minDist2[i]
                        break
        print("lalala")
        print(mn1)
        print(mn2)               
        if mn1 != 100:
            travelled = -1
            ind = -1
            for i in range(4):
                if colors[idx][i].ismovePossible(face):
                    if ind == -1:
                        ind = i
                    if minDist1[i] == 100:
                        continue
                    pos = minDist1[i] + colors[idx][i].pathindex
                    nx = colors[idx][i].path_list[pos][0]
                    ny = colors[idx][i].path_list[pos][1]
                    for k in range(0,4):
                        if k != idx:
                            for j in range(0,4):
                                if colors[k][j].cur_x == nx and colors[k][j].cur_y == ny :
                                    if colors[k][j].pathindex > travelled:
                                        travelled = colors[k][j].pathindex
                                        ind = i
            return ind
        elif mn2 != 100:
            travelled = -1
            ind = -1
            for i in range(4):
                if colors[idx][i].ismovePossible(face):
                    if ind == -1:
                        ind = i
                    if minDist2[i] == mn2:
                        pos = minDist2[i] + colors[idx][i].pathindex
                        nx = colors[idx][i].path_list[pos][0]
                        ny = colors[idx][i].path_list[pos][1]
                        sum = 0
                        for k in range(0,4):
                            if k != idx:
                                for j in range(0,4):
                                    if colors[k][j].cur_x == nx and colors[k][j].cur_y == ny :
                                        sum += colors[k][j].pathindex
                        if sum > travelled:
                            travelled = sum
                            ind = i
            return ind
        else :
            for i in range(4):
                if colors[idx][i].ismovePossible(face):
                    return i

        