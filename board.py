import tkinter as tk
from random import randrange
from tkinter import *
import PIL.Image, PIL.ImageTk
from gameconfig import *




class LudoBoard:

    def __init__(self,master):
        self.canvas=tk.Canvas(master,width=Board.BOARD_WIDTH,height=Board.BOARD_HEIGHT,bg = Color.PINK)
        self.Exit = tk.Button(master, text='EXIT', command=master.quit, relief=tk.RAISED, bg = '#E3F09B', bd = 4,activebackground = '#DDF45B', width=20, height=2)
        self.title_bar = tk.Label(master, text=Text.HEADER, fg=Color.DEFAULT, bg=Color.CYAN, font=(None, 40), relief=tk.RAISED)
        self.status_bar = tk.Label(master, text=Text.MADE_BY, bd=1, relief=tk.SUNKEN)

    def draw_rectangle(self,lx,ly,bx,by,color,width):
        self.canvas.create_rectangle(
            lx * Board.SQUARE_SIZE,
            ly * Board.SQUARE_SIZE,
            bx * Board.SQUARE_SIZE,
            by * Board.SQUARE_SIZE,
            fill=color,
            width=width
        )
    
    def draw_circle(self, x1, y1, x2, y2, color):
        self.canvas.create_oval(
            x1 * Board.SQUARE_SIZE,
            y1 * Board.SQUARE_SIZE,
            x2 * Board.SQUARE_SIZE,
            y2 * Board.SQUARE_SIZE,
            fill=color
        )

    def draw_polygon(self,x1,y1,x2,y2,color,width):
        self.canvas.create_polygon(
            x1 * Board.SQUARE_SIZE,
            y1 * Board.SQUARE_SIZE,
            (Board.BOARD_WIDTH//2)+6,
            (Board.BOARD_HEIGHT//2),
            x2 * Board.SQUARE_SIZE,
            y2 * Board.SQUARE_SIZE,
            fill=color,
            width=width
        )
    
    def draw_line(self,x1,y1,x2,y2,color,width):
        self.canvas.create_line(
            x1 * Board.SQUARE_SIZE,
            y1 * Board.SQUARE_SIZE,
            x2 * Board.SQUARE_SIZE,
            y2 * Board.SQUARE_SIZE,
            fill=color,
            width=width
        )
    
    def draw_safe(self,x, y):
        self.canvas.create_image(
            x*Board.SQUARE_SIZE,
            y*Board.SQUARE_SIZE,
            anchor=tk.NW, image=self.safe)

    def path(self):
        self.canvas.place(x=20, y=80)


    def create_panel(self,master):
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        self.canvas.place(x=width//2 - Board.BOARD_WIDTH//2, y = height//2 - Board.BOARD_HEIGHT//2)
        self.Exit.place(x=1610, y=930)
        self.title_bar.pack(side=tk.TOP, fill=tk.X)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_jail(self) :
        self.draw_rectangle(0.8,0.5,6.8,6.5, Color.BLUE, 3)
        self.draw_rectangle(1.4,1.2, 6.1,5.9, Color.DEFAULT, 0)
        self.draw_line(3.8, 0.5, 3.8, 6.5,Color.BLUE,10)
        self.draw_line(0.8, 3.5, 6.8, 3.5,Color.BLUE,10)

        self.draw_rectangle(0.8, 9.5, 6.8,15.5, Color.RED, 3)
        self.draw_rectangle(1.4,10.2, 6.1,14.9, Color.DEFAULT, 0)
        self.draw_line(3.8, 9.5, 3.8, 15.5,Color.RED,10)
        self.draw_line(0.8, 12.5, 6.8, 12.5,Color.RED,10)
        
        self.draw_rectangle(9.8, 0.5,15.8, 6.5, Color.YELLOW, 3)
        self.draw_rectangle(10.4,1.2, 15.1,5.9, Color.DEFAULT, 0)
        self.draw_line(12.8, 0.5, 12.8, 6.5,Color.YELLOW,10)
        self.draw_line(9.8, 3.5, 15.8, 3.5,Color.YELLOW,10)
        
        self.draw_rectangle(9.8,9.5, 15.8,15.5, Color.GREEN, 3)
        self.draw_rectangle(10.4,10.2, 15.1,14.9, Color.DEFAULT, 0)
        self.draw_line(12.8, 9.5, 12.8, 15.5,Color.GREEN,10)
        self.draw_line(9.8, 12.5, 15.8, 12.5,Color.GREEN,10)

    def create_home(self):
        self.draw_polygon(6.8, 6.5, 6.8, 9.5, Color.BLUE, 1)
        self.draw_polygon(6.8, 6.5, 9.8, 6.5, Color.YELLOW, 1)
        self.draw_polygon(6.8, 9.5, 9.8, 9.5, Color.RED, 1)
        self.draw_polygon(9.8, 6.5, 9.8, 9.5, Color.GREEN, 1)
    
        
    def create_path(self):
        self.isafe = PIL.Image.open("./images/safe.png")
        self.safe = PIL.ImageTk.PhotoImage(self.isafe)
        for i in range(6, 9):
            for j in range(15):
                if((i!=7 and j!=7) or (i==7 and j==0) or (i==7 and j==14)):
                    self.draw_rectangle(i + 0.8, j + 0.5, i + 1.8, j + 1.5, Color.PINK, 1)
                    self.draw_rectangle(j + 0.8, i + 0.5, j + 1.8, i + 1.5, Color.PINK, 1)
                elif(i==7 and j<=7):
                    self.draw_rectangle(i + 0.8, j + 0.5, i + 1.8, j + 1.5, Color.YELLOW, 1)
                    self.draw_rectangle(j + 0.8, i + 0.5, j + 1.8, i + 1.5, Color.BLUE, 1)
                else:
                     self.draw_rectangle(j + 0.8, i + 0.5, j + 1.8, i + 1.5, Color.GREEN, 1)
                     self.draw_rectangle(i + 0.8, j + 0.5, i + 1.8, j + 1.5, Color.RED, 1)
        
        for i,j in Board.SAFE_V:
            if i > j:
                self.draw_rectangle(i + 0.8, j + 0.5, i + 1.8, j + 1.5, Color.YELLOW, 1)
            else:
                self.draw_rectangle(i + 0.8, j + 0.5, i + 1.8, j + 1.5, Color.RED, 1)
            self.draw_safe(i+1.0,j+0.7)
        for i,j in Board.SAFE_H:
            if i > j:
                self.draw_rectangle(i + 0.8, j + 0.5, i + 1.8, j + 1.5, Color.GREEN, 1)
            else:
                self.draw_rectangle(i + 0.8, j + 0.5, i + 1.8, j + 1.5, Color.BLUE, 1)
            self.draw_safe(i+1.0, j+0.7)

                

            
                
                    

    
    def create(self,master):
        self.create_panel(master)
        self.create_jail()
        self.create_path()
        self.create_home()
    
    def get_canvas(self):
        return self.canvas
 
        