from tkinter import *
import time
import os
root = Tk()

frames = [PhotoImage(file='one_dice.gif',format = 'gif -index %i' %(i)) for i in range(9)]

def update(ind):

    frame = frames[ind]
    ind += 1
    if ind > 8:
        return
    label.configure(image=frame)
    root.after(1000, update,ind)

label = Label(root)
label.pack()
root.after(0, update,0)
root.mainloop()