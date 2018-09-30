import copy
class Color:

    GREEN = '#3EB62B'
    RED = '#F71313'
    YELLOW = '#F3F012'
    BLUE = '#3575EC'
    DEFAULT = '#E9E9E9'
    PINK = '#FFB6C1'
    CYAN = '#4EB1BA'
    GRAY = '#A9A9A9'


class Board:

    SQUARE_SIZE = 55
    PANEL_WIDTH = 600
    PANEL_HEIGHT = 640
    BOARD_WIDTH = 900
    BOARD_HEIGHT = 880
    POINTS = [(0, 0), (0, 1), (1, 0), (1, 1)]
    SAFE_V = [(6, 2), (8, 1), (6, 13), (8, 12)]
    SAFE_H = [(1, 6), (2, 8), (13, 8), (12, 6)]

class Text:

    MADE_BY = 'Made By: Mansi Agrawal & Shivam Gupta'
    HEADER =  'LUDO - THE GAME'

class Path:
    
    def __init__(self):
        self.green_path = []
        self.red_path = []
        self.blue_path = []
        self.yellow_path = []
    
    def fill_path(self):

        self.fill_cords(self.blue_path, 2 - 0.2,6 + 0.5,'right',0,5) #init x,init y,dir,starpos,len
        self.fill_cords(self.blue_path, 7 - 0.2,5 + 0.5,'up',3,5)
        self.fill_cords(self.blue_path, 7 - 0.2,0 + 0.5,'right',-1,3)
        self.fill_cords(self.blue_path, 9 - 0.2,1 + 0.5,'down',0,5)
        self.fill_cords(self.blue_path, 10 - 0.2,6 + 0.5,'right',3,5)
        self.fill_cords(self.blue_path, 15 - 0.2,6 + 0.5,'down',-1,3)
        self.fill_cords(self.blue_path, 14 - 0.2,8 + 0.5,'left',0,5)
        self.fill_cords(self.blue_path, 9 - 0.2,9 + 0.5,'down',3,5)
        self.fill_cords(self.blue_path, 9 - 0.2,14 + 0.5,'left',-1,3)
        self.fill_cords(self.blue_path, 7 - 0.2,13 + 0.5,'up',0,5)
        self.fill_cords(self.blue_path, 6 - 0.2,8 + 0.5,'left',3,5)
        self.fill_cords(self.blue_path, 1 - 0.2,8 + 0.5,'up',-1,3)
        self.rotate(self.blue_path, self.yellow_path)
        self.rotate(self.yellow_path, self.green_path)
        self.rotate(self.green_path, self.red_path)
        self.blue_path.pop()
        self.fill_cords(self.blue_path,2 - 0.2, 7 + 0.5, 'right',-1,6)
        self.yellow_path.pop()
        self.fill_cords(self.yellow_path,8 - 0.2, 1 + 0.5, 'down',-1,6)
        self.green_path.pop()
        self.fill_cords(self.green_path,14 - 0.2, 7 + 0.5, 'left',-1,6)
        self.red_path.pop()
        self.fill_cords(self.red_path,8 - 0.2, 13 + 0.5, 'up',-1,6)


    def fill_cords(self,v,inix,iniy,dir,starpos,len):

        if dir=='up':
            dx=0
            dy=-1
        elif dir=='down':
            dx=0
            dy=1    
        elif dir=='left':
            dx=-1
            dy=0
        else:
            dx=1
            dy=0

        i=0
        while i<len:

            v.append ((inix*Board.SQUARE_SIZE,iniy*Board.SQUARE_SIZE,i==starpos))
            i = i+1   
            inix+=dx
            iniy+=dy

    def rotate (self,v1,v2):
        
        for i in range(13,52):
            v2.append(copy.deepcopy(v1[i]))

        for i in range (0,13) :
            v2.append(copy.deepcopy(v1[i]))

path = Path()
path.fill_path()












