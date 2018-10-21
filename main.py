import sys


sys.setrecursionlimit(1000000)


import tkinter as tk
import tkinter.messagebox 
import PIL.Image, PIL.ImageTk
from board import *
from tkinter.font import Font
from gameconfig import *
from random import choice
from time import time, sleep
from Strategy import *
from Attacking import *
from Defensive import *
from Human import *
from RLearning import *
from Escape import *
from Mixed import *


class coin():
    def __init__(self,master, x, y, path_list,color,id) :
        self.canvas = master
        self.id = id
        self.cur_x = x
        self.cur_y = y
        self.jail_x = x
        self.jail_y = y
        self.path_list = path_list
        self.my_turn = False
        self.icoin = PIL.Image.open("./images/{}.png".format(color))
        self.coin = PIL.ImageTk.PhotoImage(self.icoin)
        self.img = self.canvas.create_image(x, y, anchor=tk.NW, image=self.coin)
        self.canvas.tag_bind(self.img, '<1>', self.moveCoinHandler)
        self.win = 0
        self.pathindex=-1
    
    def isatjail(self):
        if self.pathindex==-1 :
            return True
        else:
            return False
    
    def go_to_jail(self):
        for i in range(self.pathindex,1,-1):
            self.pathindex -= 1
            self.canvas.delete(self.img)
            self.cur_x=self.path_list[self.pathindex][0]
            self.cur_y=self.path_list[self.pathindex][1]
            self.img=self.canvas.create_image(self.cur_x+20, self.cur_y+11, anchor=tk.NW, image=self.coin)
            self.canvas.tag_bind(self.img, '<1>', self.moveCoinHandler)
            self.canvas.update()
            sleep(0.1)
        
        self.canvas.delete(self.img)
        self.cur_x=self.jail_x
        self.cur_y=self.jail_y
        self.img=self.canvas.create_image(self.cur_x, self.cur_y, anchor=tk.NW, image=self.coin)
        self.canvas.tag_bind(self.img, '<1>', self.moveCoinHandler)
        self.canvas.update()
        sleep(0.1)
        self.pathindex = -1

    def updatecoinposition(self,cnt):

        in_x = self.cur_x
        in_y = self.cur_y
        
        for i in range(1,cnt+1):
            self.pathindex+=1
            self.canvas.delete(self.img)
            self.cur_x=self.path_list[self.pathindex][0]
            self.cur_y=self.path_list[self.pathindex][1]
            self.img=self.canvas.create_image(self.cur_x+20, self.cur_y+11, anchor=tk.NW, image=self.coin)
            self.canvas.tag_bind(self.img, '<1>', self.moveCoinHandler)
            self.canvas.update()
            sleep(0.1)
        
        if self.path_list[self.pathindex][2] == 0:
            ind = -1
            jnd = -1
            c = 0
            for i in range(0,4):
                if i != self.id:
                    for j in range(0,4):
                        if colors[i][j].cur_x == self.cur_x and colors[i][j].cur_y == self.cur_y :
                            ind = i
                            jnd = j
                            c += 1
            if c== 1:               
                colors[ind][jnd].go_to_jail()
        
        Dice.arrange_in_cell(self.cur_x,self.cur_y)
        Dice.arrange_in_cell(in_x,in_y)
        
    def moveCoin(self):
        if self.my_turn and Dice.unrolled==False:
            cnt=Dice.lastval
            if(self.ismovePossible(cnt)==False):
                return
            Dice.unrolled = True
            if self.isatjail()==True and cnt==6 :
                self.updatecoinposition(1)
            elif self.isatjail()==False:
                self.updatecoinposition(cnt)

            if Dice.lastval!=6:    
                Dice.turn = (Dice.turn + 1)%Dice.player_count
                Dice.update_dice_position()
            else:
                if players[Dice.turn].strategy != "Human Mode":
                    Dice.roll()


    
    def moveCoinHandler(self,event):
        self.moveCoin()
        
    def ismovePossible(self,cnt):
        if(self.pathindex == len(self.path_list) - 1):
                return False
        if self.pathindex == -1 and cnt != 6:
                return False
        if self.pathindex + cnt >= len(self.path_list):
                return False
        return True
        
    def change_state(self,chance):
        if self.id == chance:
            self.my_turn = True
        else:
            self.my_turn = False

class Dice:

    turn=0
    player_count=0
    past_six = 0
    dice_x = 340
    dice_y = 200
    unrolled = True
    lastval=-1
    @classmethod
    def update_dice_position(cls):
        if cls.turn==0:
            cls.dice_x=340
            cls.dice_y=200
        if cls.turn==1:
            cls.dice_x=1480
            cls.dice_y=200
        if cls.turn==2:
            cls.dice_x=1480
            cls.dice_y=750
        if cls.turn==3:
            cls.dice_x=340
            cls.dice_y=750
        cls.img = PIL.ImageTk.PhotoImage(PIL.Image.open('./images/dice_{}.png'.format(1)))
        cls.image_button["image"] = cls.img
        cls.image_button.place(x=cls.dice_x, y=cls.dice_y)
        for i in range(0,4):
            for j in range(0,4):
                colors[i][j].change_state(cls.turn)
        if players[cls.turn].strategy != "Human Mode":
            cls.roll()

    @classmethod 
    def arrange_in_cell(cls,x,y):
        lst = []
        for i in range(0,4):
            for j in range(0,4):
                if colors[i][j].cur_x == x and colors[i][j].cur_y == y :
                    lst.append((i,j))
        
        if len(lst) > 1 :
            for i in range(0,len(lst)-1):
                p = lst[i][0]
                q = lst[i][1]
                colors[p][q].canvas.delete(colors[p][q].img)
                colors[p][q].cur_x=colors[p][q].path_list[colors[p][q].pathindex][0]
                colors[p][q].cur_y=colors[p][q].path_list[colors[p][q].pathindex][1]
                colors[p][q].img=colors[p][q].canvas.create_image(colors[p][q].cur_x+4*i, colors[p][q].cur_y+11, anchor=tk.NW, image=colors[p][q].coin)
                colors[p][q].canvas.tag_bind(colors[p][q].img, '<1>', colors[p][q].moveCoinHandler)
        elif len(lst) == 1:
            p = lst[0][0]
            q = lst[0][1]
            colors[p][q].canvas.delete(colors[p][q].img)
            colors[p][q].cur_x=colors[p][q].path_list[colors[p][q].pathindex][0]
            colors[p][q].cur_y=colors[p][q].path_list[colors[p][q].pathindex][1]
            colors[p][q].img=colors[p][q].canvas.create_image(colors[p][q].cur_x+20, colors[p][q].cur_y+11, anchor=tk.NW, image=colors[p][q].coin)
            colors[p][q].canvas.tag_bind(colors[p][q].img, '<1>', colors[p][q].moveCoinHandler)
            colors[p][q].canvas.update()


    @classmethod
    def ismovePossible(cls):
        for i in range(0,4):
            if(colors[cls.turn][i].ismovePossible(cls.lastval)):
                    return True
        return False

    
    @classmethod
    def load_dice(cls):    
        cls.img = PIL.ImageTk.PhotoImage(PIL.Image.open('./images/dice_1.png'))
        cls.image_button = tk.Button(root, width=100, height=100, image=cls.img,command = cls.roll)
        cls.image_button.place(x=cls.dice_x, y=cls.dice_y)
        for i in range(0,4):
            colors[0][i].change_state(cls.turn)
        if players[cls.turn].strategy != "Human Mode":
            cls.roll()
    

    @classmethod
    def roll(cls):
        if (cls.unrolled):
            if(cls.past_six<=1):
                face = choice(range(1,7))
            else:
                face = choice(range(1,6))
            if(face == 6):
                cls.past_six += 1
            else:
                cls.past_six = 0
            
            cls.lastval=face
            cls.img = PIL.ImageTk.PhotoImage(PIL.Image.open('./images/dice_{}.png'.format(face)))
            cls.image_button["image"] = cls.img
            if(cls.ismovePossible()):
                cls.unrolled = False
                if players[cls.turn].strategy != "Human Mode":
                    idx = players[cls.turn].getCoinToMove(cls.turn,colors,cls.lastval)
                    colors[cls.turn][idx].moveCoin()
            else :
                root.update()
                sleep(0.3)
                cls.turn = (cls.turn+1)%cls.player_count
                cls.update_dice_position()

def position_coin(x, y, color, path_list,id):
    container = []
    for i in range(2):
        tmp = coin(app.get_canvas(), x, y + i*2*Board.SQUARE_SIZE, path_list,color=color,id=id)
        container.append(tmp)
    for i in range(2):
        tmp = coin(app.get_canvas(), x + 2*Board.SQUARE_SIZE, y + i*2*Board.SQUARE_SIZE,path_list, color=color,id = id)
        container.append(tmp)
    return container

def on_closingroot():
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit the game?"):
        root.destroy() 

no_of_players = 4
players = []
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('{0}x{0}'.format(width,height))
root.title('Ludo')
app = LudoBoard(root)
app.create(root)
colors = []
colors.append(position_coin(2.5*Board.SQUARE_SIZE, 2.2*Board.SQUARE_SIZE, color='blue',path_list = path.blue_path, id=0))
colors.append(position_coin(11.5*Board.SQUARE_SIZE, 2.2*Board.SQUARE_SIZE, color='yellow',path_list = path.yellow_path, id=1))
colors.append(position_coin(11.5*Board.SQUARE_SIZE, 11.2*Board.SQUARE_SIZE, color='green',path_list = path.green_path, id=2))
colors.append(position_coin(2.5*Board.SQUARE_SIZE, 11.2*Board.SQUARE_SIZE, color='red',path_list =  path.red_path,id=3))

welcome_msg = ''' Welcome Champs let's get into the game of LUDO :-) \n
        Rules of the game:
- The players roll a six-sided die in turns and can advance any of their coins on the track by the number of steps as displayed by the dice.\n
- Once you get a six in a dice throw, you have to roll the dice again, and must use all scores while making the final selection of what coins to move where.\n
- If you get a six three times in a row, your throws are reset and you will lose that chance.\n
- The coin can advance in the home run only if it reaches exactly inside the home pocket, or moves closer to it through the home run. 
For example, if the coin is four squares away from the home pocket and the player rolls a five, he must apply the throw to some other coin. \
However, if you roll a two, you can advance the coin by two squares and then it rests there until the next move.\n 
    
    Enjoy the game and have fun.
        # Best of luck #
'''
tkinter.messagebox.showinfo('Welcome to Ludo', welcome_msg)
top = tk.Toplevel(root,bg = "#31D3EA")
strategytop = tk.Toplevel(root,bg = "#31D3EA")

top.geometry('800x800+{}+{}'.format(width//2 - 400, height//2 - 400))
strategytop.geometry('800x800+{}+{}'.format(width//2 - 400, height//2 - 400))

root.protocol("WM_DELETE_WINDOW", on_closingroot)
v = tk.IntVar()

def playgame():
    strategytop.destroy()
    for i in range(len(players)):
        if players[i].get() == "Human Mode":
            players[i] = Human("Human Mode")
        elif players[i].get() == "Attacking Mode": 
            players[i] = Attacking("Attacking Mode")
        elif players[i].get() == "Defensive Mode": 
            players[i] = Defensive("Defensive Mode")
        elif players[i].get() == "Escape Mode": 
            players[i] = Escape("Escape Mode")
        elif players[i].get() == "Mixed Mode": 
            players[i] = Mixed("Mixed Mode")
        elif players[i].get() == "Learning Mode": 
            players[i] = RLearning("Learning Mode")
    Dice.load_dice()
        
def selectstrategy():
    myFont = Font(family="Times New Roman", size=14)
    tk.Label(strategytop,text="Select Strategy of players",font=("Helvetica", 30),pady=60,bg = "#31D3EA").pack()
    
    for i in range(Dice.player_count):
        OPTIONS=[
            'Human Mode',
            'Attacking Mode',
            'Defensive Mode',
            'Mixed Mode',
            'Escape Mode',
            'Learning Mode'
        ]

        players.append(StringVar(strategytop))
        players[i].set(OPTIONS[0]) # default value

        w = OptionMenu(strategytop, players[i], *OPTIONS)
        w.pack()
        
        tk.Button(strategytop, text='Play',command = playgame, bg = '#FFF', width=20, height=2).place(x=300,y=600)
        
    
    
def startgame():
    if v.get() >= 1 :
        Dice.player_count = v.get() + 1
        top.destroy()
        selectstrategy()
    else :
        tkinter.messagebox.showinfo("Warning", "Please select number of players")


def create_entry_page():
    myFont = Font(family="Times New Roman", size=14)
    tk.Label(top,text="Select number of players",font=("Helvetica", 30),pady=60,bg = "#31D3EA").pack()
    tk.Radiobutton(top, text="Two",selectcolor='#42E123', background='#2390E1', activebackground='#42E123',variable=v, font=myFont,value=1, indicatoron=0,width= 40,height=5).place(x=210,y=200)
    tk.Radiobutton(top, text="Three", selectcolor='#42E123',background='#2390E1',activebackground='#42E123',variable=v,font=myFont, value=2, indicatoron=0,width= 40,height=5).place(x=210,y=320)
    tk.Radiobutton(top, text="Four", selectcolor='#42E123',background='#2390E1',activebackground='#42E123',variable=v,font=myFont, value=3,  indicatoron=0,width= 40,height=5).place(x=210,y=440)
    tk.Button(top, text='Submit',command=startgame, bg = '#FFF', width=20, height=2).place(x=300,y=600)

create_entry_page()

root.mainloop()
