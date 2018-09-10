import tkinter as tk
from random import randrange
from tkinter import *
from gameconfig import *




class LudoBoard:

    def __init__(self,master):
        self.canvas=tk.Canvas(master,width=Board.BOARD_WIDTH,height=Board.BOARD_HEIGHT)
        self.frame=tk.Frame(master,width=Board.PANEL_WIDTH,height=Board.PANEL_HEIGHT, bg=Color.CYAN)
        self.Exit = tk.Button(master, text='EXIT', command=master.quit, relief=tk.RAISED, width=20, height=2)
        self.title_bar = tk.Label(master, text=Text.HEADER, fg=Color.DEFAULT, bg=Color.CYAN, font=(None, 40), relief=tk.RAISED)
        self.status_bar = tk.Label(master, text=Text.MADE_BY, bd=1, relief=tk.SUNKEN)
        self.create_panel()

    def draw_rectangle(self,lx,ly,bx,by,color,width):
        self.canvas.create_rectangle(lx,ly,bx,by,fill=color,width=width)


    def draw_polygon(self,x1,y1,x2,y2,color,width):
        self.canvas.create_polygon(
            x1,
            y1,
            Board.BOARD_WIDTH//2,
            Board.BOARD_HEIGHT//2,
            x2,
            y2,
            fill=color,
            width=width
        )

    def path(self):
        self.canvas.place(x=20, y=80)


    def create_panel(self):
        self.frame.place(x=700, y=80)
        self.Exit.place(x=910, y=620)
        self.title_bar.pack(side=tk.TOP, fill=tk.X)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create(self):
        self.path()
        self.home()
        self.create_panel() 
        

def main():
  
    root = Tk()
    root.geometry("2500x1500+3000+3000")
    app = LudoBoard(root)
    root.mainloop()  


if __name__ == '__main__':
    main()   