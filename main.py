import tkinter as tk
import tkinter.messagebox 
import PIL.Image, PIL.ImageTk
from board import *
from tkinter.font import Font


class coin():
    def __init__(self,master, x, y, color,id) :
        self.canvas = master
        self.id = id
        self.cur_x = x
        self.cur_y = y
        self.jail_x = x
        self.jail_y = y
        self.icoin = PIL.Image.open("./images/{}.png".format(color))
        self.coin = PIL.ImageTk.PhotoImage(self.icoin)
        self.img = self.canvas.create_image(x, y, anchor=tk.NW, image=self.coin)
        self.win = 0

def position_coin(x, y, color, id):
    container = []
    for i in range(2):
        tmp = coin(app.get_canvas(), x, y + i*2*Board.SQUARE_SIZE, color=color,id=id)
        container.append(tmp)
    for i in range(2):
        tmp = coin(app.get_canvas(), x + 2*Board.SQUARE_SIZE, y + i*2*Board.SQUARE_SIZE, color=color,id = id)
        container.append(tmp)
    return container


class dice:
    turn = 0

def on_closingroot():
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit the game?"):
        root.destroy() 

no_of_players = 4
players = []
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
print(width)
print(height)
root.geometry('{0}x{0}'.format(width,height))
root.title('Ludo')
app = LudoBoard(root)
app.create(root)
colors = []
colors.append(position_coin(2.5*Board.SQUARE_SIZE, 2.2*Board.SQUARE_SIZE, color='blue', id=0))
colors.append(position_coin(2.5*Board.SQUARE_SIZE, 11.2*Board.SQUARE_SIZE, color='red', id=1))
colors.append(position_coin(11.5*Board.SQUARE_SIZE, 11.2*Board.SQUARE_SIZE, color='green', id=2))
colors.append(position_coin(11.5*Board.SQUARE_SIZE, 2.2*Board.SQUARE_SIZE, color='yellow', id=3))

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
top = tk.Toplevel(root)
top.geometry('800x800+{}+{}'.format(width//2 - 400, height//2 - 400))
root.protocol("WM_DELETE_WINDOW", on_closingroot)

def create_entry_page():
    v = tk.IntVar()
    myFont = Font(family="Times New Roman", size=14)
    tk.Label(top,text="Select number of players",font=("Helvetica", 30),pady=60).pack()
    tk.Radiobutton(top, text="Two",selectcolor='#42E123', background='#2390E1', activebackground='#42E123',variable=v, font=myFont,value=1, indicatoron=0,width= 40,height=5).place(x=210,y=200)
    tk.Radiobutton(top, text="Three", selectcolor='#42E123',background='#2390E1',activebackground='#42E123',variable=v,font=myFont, value=2, indicatoron=0,width= 40,height=5).place(x=210,y=320)
    tk.Radiobutton(top, text="Four", selectcolor='#42E123',background='#2390E1',activebackground='#42E123',variable=v,font=myFont, value=3,  indicatoron=0,width= 40,height=5).place(x=210,y=440)
    tk.Button(top, text='Play',bg = '#E3F09B',activebackground = '#DDF45B', width=20, height=2).place(x=300,y=600)
create_entry_page()
root.mainloop()
