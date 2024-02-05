#Nastavenia-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from time import *
from math import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mbox
from random import *
import winsound as ws
import smajlotkgui03 as gui
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
MEDIA="C:\\Windows\\Media\\"
timeout=-3   #sec
áno=True
prY=600
prX=1200
prBG="#fff"
tick=0
minms=1/120 #fps

rozm=50
dlzka=10

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

def pytagor(a,b):
    return sqrt(a**2+b**2)

def trasa(x,x1,percent):
    percent/=100
    return (x1-x)*percent+x

def choď():
    global j, lopta
    #j údaje lopty
    #j[0] na koľkej trase (i)
    #j[1] koľko percent z trasy (o)
    #j[2] úroveň bielej
    #len(a)-2 poradie poslednej trasy od 0
    if j[0]>len(a)-2:
        i=len(a)-2
    else:
        i=j[0]
    o=j[1]
    try:
        pr.create_oval(trasa(i*rozm,(i+1)*rozm,o)-10,trasa(a[i],a[i+1],o)-10,trasa(i*rozm,(i+1)*rozm,o)+10,trasa(a[i],a[i+1],o)+10,tag="b",outline=gui.rgb((j[2],j[2],j[2])))
    except Exception as e:
        print(e)
        pass
    j[1]+=1
    if j[1]>100 and j[0]<len(a)-2:
        j[1]=0
        j[0]+=1
    if j[1]>100 and j[0]>=len(a)-2:
        j[0]+=1
        j[2]+=5
    if j[2]>=255:
        del lopta[l]


    

#Prostredie-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
tk=Tk()
tk.title("SmajloSlovakian™")
tk.protocol("WM_DELETE_WINDOW",koniec)
pr=Canvas(tk,height=prY,width=prX,bg=prBG)
pr.grid(columnspan=200)

#Setup------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
a=randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100),randint(0,100)
a=100,20,80,50,100,110,40
a=()
for i in range(randint(2,int(prX/rozm))):
    a+=(randint(0,100),)
kles,rast=0,0
for i in range(len(a)-1):
    try:
        pr.create_line(i*rozm,a[i],(i+1)*rozm,a[i+1],tag="a")
        if a[i]<a[i+1]:
            kles+=pytagor(a[i+1]-a[i],rozm)
        elif a[i]>a[i+1]:
            rast+=pytagor(a[i+1]-a[i],rozm)
        else:
            rast+=pytagor(a[i+1]-a[i],rozm)/2
            kles+=pytagor(a[i+1]-a[i],rozm)/2
    except:
        pass
pr.create_text(150,300,text="Stúpanie: "+str(round(rast,2)),font=("Arial",20),tag="a")
pr.create_text(150,350,text="Klesanie: "+str(round(kles,2)),font=("Arial",20),tag="a")
pr.create_text(150,400,text="Celkom: "+str(round(kles+rast,2)),font=("Arial",20),tag="a")
gui.setup(pr)
tl0=gui.Button(400,400,"Regenerovať").activate()
tl1=gui.Button(600,400,"Gulička").activate()
sl0=gui.Slider(400,450,"Počet bodov: ",DefaultValue=(dlzka-2)/(prX/rozm-2),DisplayVal=str(dlzka)).activate()
sl1=gui.Slider(400,500,"Rozmedzie bodov: ",DefaultValue=(rozm)/(prX/dlzka),DisplayVal=str(dlzka)).activate()
lopta=[]

#Loop-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
start=time()
tick=time()
while áno:
    gui.update()
    if sl0.stat==2:
        sl0.value=round(sl0.value*(prX/rozm-2))/(prX/rozm-2)
        dlzka=round(sl0.value*(prX/rozm-2)+2)
        sl0.dval=str(dlzka)
    elif sl1.stat==2:
        sl1.value=round(sl1.value*(prX/dlzka))/(prX/dlzka)
        rozm=round(sl1.value*(prX/dlzka))
        sl1.dval=str(rozm)

    if tl1.stat==3:
        lopta.append([0,0,0])
    elif tl0.stat==3:
        e=dlzka
        if e<=prX/rozm:
            pr.delete("a")
            a=()
            for i in range(e):
                a+=(randint(0,100),)
            kles,rast=0,0
            for i in range(len(a)):
                try:
                    pr.create_line(i*rozm,a[i],(i+1)*rozm,a[i+1],tag="a")
                    if a[i]<a[i+1]:
                        kles+=pytagor(a[i+1]-a[i],rozm)
                    elif a[i]>a[i+1]:
                        rast+=pytagor(a[i+1]-a[i],rozm)
                    else:
                        rast+=pytagor(a[i+1]-a[i],rozm)/2
                        kles+=pytagor(a[i+1]-a[i],rozm)/2
                except:
                    pass
            pr.create_text(150,300,text="Stúpanie: "+str(round(rast,2)),font=("Arial",20),tag="a")
            pr.create_text(150,350,text="Klesanie: "+str(round(kles,2)),font=("Arial",20),tag="a")
            pr.create_text(150,400,text="Celkom: "+str(round(kles+rast,2)),font=("Arial",20),tag="a")
        else:
            pr.create_text(400,350,text="Príliš dlhá cesta",tag="a")

    pr.delete("b")
    for l in range(len(lopta)):
        if l<len(lopta):
            j=lopta[l]
            choď()
        else:
            break

    if tick-start>=timeout>=0:
        áno=False
    tk.update() #simple 120hz lock VV
    psleep(nonneg(minms-(time()-tick)))
    print(fps(tick),end="\r")
    tick=time()

#Koniec-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("program končí                                                            ")
ws.PlaySound(MEDIA+"tada.wav",10)
tk.update()
