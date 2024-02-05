#vytvoriť okno
from random import *
from math import *
import tkinter as tk
Prostredie = tk.Canvas(height=600,width=600,bg="#fff")
Prostredie.pack()




def lopticka(x,y):
    Prostredie.create_oval(x-10,y-10, x+10,y+10)
    Prostredie.update()
    Prostredie.after(10)
    Prostredie.delete('all')
    y=y+1
    Prostredie.create_oval(x-10,y-10, x+10,y+10)
    Prostredie.update()
    Prostredie.after(10)
    Prostredie.delete('all')
    y=y+1
    a=10
    for i in range(0,125):
        a=a-i*0.0003
        Prostredie.create_oval(x-a,y-10, x+a,y+10)
        Prostredie.update()
        Prostredie.after(10)
        Prostredie.delete('all')
        y=y+1+i*0.04
    y=y+15
    Prostredie.create_oval(x-13,y-8, x+13,y+8)
    Prostredie.update()
    Prostredie.after(10)
    Prostredie.delete('all')
    y=y-15
    Prostredie.create_oval(x-12,y-9, x+12,y+9)
    Prostredie.update()
    Prostredie.after(10)
    Prostredie.delete('all')
    y=y-6
    Prostredie.create_oval(x-11,y-10, x+11,y+10)
    Prostredie.update()
    Prostredie.after(10)
    Prostredie.delete('all')
    y=y-6
    Prostredie.create_oval(x-10,y-10, x+10,y+10)
    Prostredie.update()
    Prostredie.after(10)
    Prostredie.delete('all')
    a=8
    for i in range(0,139):
        a=a+i*0.0003
        y=y-6+i*0.04
        Prostredie.create_oval(x-a,y-10, x+a,y+10)
        Prostredie.update()
        Prostredie.after(10)
        Prostredie.delete('all')
    for i in range(0,20):
        y=y+1
        Prostredie.create_oval(x-10,y-10, x+10,y+10)
        Prostredie.update()
        Prostredie.after(10)
        Prostredie.delete('all')
    
    
    
    
    

for i in range(0,100):
    lopticka(100,150)
