#Nastavenia-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from time import *
from math import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mbox
from random import *
import winsound as ws
import GUI as gui
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
MEDIA="C:\\Windows\\Media\\"
timeout=-1   #sec
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
gui.setpr(pr)
gtl1=gui.tlačidlo(200,100,"Vymazanie tohto tlačidla",dimension=(-200,-100,100,20))
gtl2=gui.tlačidlo(200,200,"Print index, nepustiť z myši")
gtl3=gui.tlačidlo(200,220,"Ukončiť aplikáciu")



#Loop-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
start=time()
tick=time()
while áno:
    if gui.status(gtl1)==3:
        gui.terminate(gtl1)
    if gui.status(gtl2)==1:
        gui.modify(gtl2,0,gui.shover[0])
        gui.modify(gtl2,1,gui.shover[1])
    if gui.status(gtl2)==3:
        print(gui.idtoindex(gtl2))
    if gui.status(gtl3)==3:
        koniec()

    if tick-start>=timeout and timeout>=0:
        áno=False
    tk.update() #simple fps lock VV
    psleep(nonneg(minms-(time()-tick)))
    print(fps(tick),end="\r")
    gui.update()
    tick=time()

#Koniec-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("program končí                                                            ")
ws.PlaySound(MEDIA+"tada.wav",0)
tk.update()
