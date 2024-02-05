#Nastavenia-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from time import *
from math import *
from tkinter import *
from tkinter import ttk
import smajlotkgui04 as gui
from astar import *

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    print("dpi nastavenia neboli použité")
áno=True
prY=600
prX=1200
prBG="#fff"
tick=0
minms=1/120 #fps

#Definície--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def koniec():
    global áno
    áno=False

def nonneg(a,b=0):
    if a<b:
        return b
    else:
        return a

def psleep(sec,precision=0.001):
    tick=time()
    while nonneg(sec-(time()-tick))>precision:
        ''

def fps(tick):
    try:
        return int(1/(time()-tick))
    except:
        return "max"

            

#Prostredie-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
tk=Tk()
tk.title("SmajloSlovakian™")
tk.protocol("WM_DELETE_WINDOW",koniec)
pr=Canvas(tk,height=prY,width=prX,bg=prBG)
pr.grid(columnspan=200)

#Setup------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
gui.setup(pr)
m=mriežka(20,10)
mm=50

gtl1=gui.Button(prX-100,prY-25,"Generuj").activate()



#Loop-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
start=time()
tick=time()
tick2=1
while áno:
    for i in m.bunky:
        for o in i:
            f=""
            if(o.x*mm+mm>gui.shover[0]>o.x*mm and o.y*mm+mm>gui.shover[1]>o.y*mm):
                if(gui.sclick and not gui.spclick):
                    o.stav=(o.stav+1)%4
                if(o.stav==0):
                    f="blue"
            if(o.stav==1):
                f="black"
            if(o.stav==2):
                f="red"
            if(o.stav==3):
                f="lime"
            pr.create_rectangle(o.x*mm,o.y*mm,o.x*mm+mm,o.y*mm+mm,tags="refresh",fill=f)
    
    if(gtl1.stat==3):
        p=-1
        for i in m.find():
            p+=1
            pr.create_text(i.x*mm+mm/2,i.y*mm+mm/2,text=p)
    
    gui.updatelem(tick2)
    gui.updatetools()
    tk.update()
    pr.delete("refresh")
    psleep(nonneg(minms-(time()-tick)))
    print(fps(tick),end="            \r")
    tick2=time()-tick
    tick=time()

#Koniec-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("\nprogram končí                                                            ")
tk.update()