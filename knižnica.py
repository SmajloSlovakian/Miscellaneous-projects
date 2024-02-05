#Nastavenia-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from time import *
from math import *
from tkinter import *
from tkinter import ttk
from WinDesMan2 import Window
import smajlotkgui05 as gui
from WinDesMan2 import *
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

class záznamyapp(WindowedApp):
    label="Záznamy"
    deletable=False
    placement=(50,50)
    def update(c, clicking, hover, v: Window, t):
        super().update(clicking, hover, v, t)
        if(c.dx>hover[0]>0 and c.dy>hover[1]>0):
            off=0
            if(-c.dy+len(c.zoztl)*40>=-(c.offset+gui.sscroll*20)>=0):
                off=c.offset
                c.offset+=gui.sscroll*20
                off-=c.offset
            c.offset-=c.setoff
            off+=c.setoff
            c.setoff=0
            for i in c.zoztl:
                i:gui.Button
                for o in záznam._reg:
                    if(i.tags[0]==str(o)):
                        i.txt=o.autor+": "+o.názov+"\n"+o.rok+" - "+o.jazyk
                i.my-=off
                if(c.y+c.dy-10<i.my or i.my<c.y+10):
                    i.deactivate()
                else:
                    i.activate()
        if(c.gtl1.stat==3):
            t=záznam("id","názov","autor","cena","isbn","počet","rok","jazyk")
            tt=gui.Button(c.x+c.dx/2,c.y+len(záznam._reg)*40-20+c.offset,f"{t.autor}: {t.názov}\n{t.rok} - {t.jazyk}",tags=[str(t)]+c.tags).activate()
            c.zoztl+=[tt]
            c.guielements+=[tt]
        for i in c.zoztl:
            if(i.stat==3):
                for o in záznam._reg:
                    if(i.tags[0]==str(o)):
                        Window(jedenzázapp).app.záznam=o
        if(c.gtl2.stat==3):
            with open("knihy zoznam.txt","w",encoding="utf-8") as s:
                for i in záznam._reg:
                    i:záznam
                    s.write(i.id+";"+i.názov+";"+i.autor+";"+i.cena+";"+i.isbn+";"+i.strán+";"+i.rok+";"+i.jazyk+"\n")
        if(c.gtl3.stat==3):
            c.searching=not(c.searching)
            if(c.searching):
                c.gtl4.activate()
                c.gtl5.activate()
                pr.create_window(c.x+c.dx-50,c.y+100,tags=c.tags+[str(c)+"en1"],window=c.en1)
            else:
                pr.delete(str(c)+"en1")
                c.gtl4.deactivate()
                c.gtl5.deactivate()
                for i in c.zoztl:
                    i.grey=False
        if(c.searching):
            for i in c.zoztl:
                if(c.en1.get() in i.txt):
                    if(i.grey):
                        i.grey=False
                        i.draw()
                else:
                    if(not(i.grey)):
                        i.grey=True
                        i.draw()
        if(c.gtl4.stat==3):
            t=0
            for i in c.zoztl:
                i:gui.Button
                if(t==0 and i.stat==0):
                    t=2
                elif(t==2 and i.stat==-1):
                    c.setoff+=40
                    if(not(i.grey)):
                        break
        if(c.gtl5.stat==3):
            t=0
            tt=c.zoztl
            tt.reverse()
            for i in tt:
                i:gui.Button
                if(t==0 and i.stat==0):
                    t=2
                elif(t==2 and i.stat==-1):
                    c.setoff-=40
                    if(not(i.grey)):
                        break

    def draw(c):
        super().draw()
        c.gtl1.mx=c.x+25
        c.gtl1.my=c.y+25
        c.gtl2.mx=c.x-25+c.dx
        c.gtl2.my=c.y+25
        for i in c.zoztl:
            u=0
            t=False
            for o in záznam._reg:
                u+=1
                if(i.tags[0]==str(o)):
                    i.my=c.y+u*40-20+c.offset
                    t=True
            if(not(t)):
                i.forget()
                c.zoztl.remove(i)
                c.guielements.remove(i)
    def __init__(c, tags, window: Window) -> None:
        super().__init__(tags, window)
        c.offset=0
        c.setoff=0
        c.gtl1=gui.Button(c.x+25,c.y+25,"+",tags=tags,Dimensions=(-20,-20,20,20)).activate()
        c.gtl2=gui.Button(c.x+c.dx-25,c.y+25,"💾",tags=tags,Dimensions=(-20,-20,20,20)).activate()
        c.gtl3=gui.Button(c.x+c.dx-25,c.y+75,"🔎",tags=tags,Dimensions=(-20,-20,20,20)).activate()
        c.gtl4=gui.Button(c.x+c.dx-25,c.y+175,"⬇",tags=tags,Dimensions=(-20,-20,20,20))
        c.gtl5=gui.Button(c.x+c.dx-65,c.y+175,"⬆",tags=tags,Dimensions=(-20,-20,20,20))
        c.en1=ttk.Entry()
        c.searching=False
        c.zoztl=[]
        try:
            with open("knihy zoznam.txt",encoding="utf-8") as s:
                for i in s.readlines():
                    i=i.strip().split(";")
                    t=záznam(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])
                    c.zoztl+=[gui.Button(c.x+c.dx/2,c.y+len(záznam._reg)*40-20,f"{t.autor}: {t.názov}\n{t.rok} - {t.cena}",tags=[str(t)]+c.tags).activate()]
        except:
            with open("knihy zoznam.txt","w",encoding="utf-8"):
                pass
        c.guielements+=[c.gtl1,c.gtl2,c.gtl3,c.gtl4,c.gtl5]+c.zoztl

class jedenzázapp(WindowedApp):
    placement=(500,50)
    def update(c, clicking, hover, v: Window, t):
        super().update(clicking, hover, v, t)
        if(not(c.tlmade) and c.záznam!=None):
            c.gtlist+=[gui.Button(c.x+100,c.y+10,"ID: {}",DisplayVal=c.záznam.id,Dimensions=(-100,-10,100,10)).activate()]
            c.gtlist+=[gui.Button(c.x+100,c.y+30,"Názov: {}",DisplayVal=c.záznam.názov,Dimensions=(-100,-10,100,10)).activate()]
            c.gtlist+=[gui.Button(c.x+100,c.y+50,"Autor: {}",DisplayVal=c.záznam.autor,Dimensions=(-100,-10,100,10)).activate()]
            c.gtlist+=[gui.Button(c.x+100,c.y+70,"Cena: {}",DisplayVal=c.záznam.cena,Dimensions=(-100,-10,100,10)).activate()]
            c.gtlist+=[gui.Button(c.x+100,c.y+90,"ISBN: {}",DisplayVal=c.záznam.isbn,Dimensions=(-100,-10,100,10)).activate()]
            c.gtlist+=[gui.Button(c.x+100,c.y+110,"Počet strán: {}",DisplayVal=c.záznam.strán,Dimensions=(-100,-10,100,10)).activate()]
            c.gtlist+=[gui.Button(c.x+100,c.y+130,"Rok: {}",DisplayVal=c.záznam.rok,Dimensions=(-100,-10,100,10)).activate()]
            c.gtlist+=[gui.Button(c.x+100,c.y+150,"Jazyk: {}",DisplayVal=c.záznam.jazyk,Dimensions=(-100,-10,100,10)).activate()]
            c.guielements+=c.gtlist
            c.tlmade=True
        o=-1
        for i in c.gtlist:
            o+=1
            if(c.edit==-1 or c.edit==o):
                if(i.grey):
                    i.grey=False
                    i.draw()
                if(i.stat==3):
                    if(c.edit==o):
                        c.edit=-1
                        pr.delete(c.en1win)
                    else:
                        c.edit=o
                        c.en1win=pr.create_window(c.x+c.dx/2,c.y+c.dy-20,window=c.en1,tags=c.tags)
                        c.en1.delete(0,END)
                        c.en1.insert(0,i.dval)
                if(c.edit==o):
                    i.dval=c.en1.get()
            else:
                if(not i.grey):
                    i.grey=True
                    i.draw()
        if(c.gtl1.stat==3):
            c.záznam.id=c.gtlist[0].dval
            c.záznam.názov=c.gtlist[1].dval
            c.záznam.autor=c.gtlist[2].dval
            c.záznam.cena=c.gtlist[3].dval
            c.záznam.isbn=c.gtlist[4].dval
            c.záznam.strán=c.gtlist[5].dval
            c.záznam.rok=c.gtlist[6].dval
            c.záznam.jazyk=c.gtlist[7].dval
        if(c.gtl2.stat==3):
            c.záznam.forget()
            c.win.fading=-c.win.faspeed
    def draw(c):
        super().draw()
        if(c.záznam!=None):
            c.label=c.záznam.autor+" - "+c.záznam.názov
    def __init__(c, tags, window: Window) -> None:
        super().__init__(tags, window)
        c.gtl1=gui.Button(c.x+c.dx-20,c.y+20,"💾",Dimensions=(-20,-20,20,20),tags=c.tags).activate()
        c.gtl2=gui.Button(c.x+c.dx-20,c.y+70,"❌",Dimensions=(-20,-20,20,20),tags=c.tags).activate()
        c.guielements+=[c.gtl1,c.gtl2]
        c.záznam:záznam=None
        c.tlmade=False
        c.gtlist:list[gui.Button]=[]
        c.en1=ttk.Entry()
        c.en1win=-1
        c.edit=-1

class záznam:
    id=""
    názov=""
    autor=""
    cena=""
    isbn=""
    strán=""
    rok=""
    jazyk=""
    _reg=[]
    def forget(c):
        záznam._reg.remove(c)
    def __init__(c,id,náz,au,cen,isb,st,rok,jaz) -> None:
        c.id=id
        c.názov=náz
        c.autor=au
        c.cena=cen
        c.isbn=isb
        c.strán=st
        c.rok=rok
        c.jazyk=jaz
        záznam._reg+=[c]

#Prostredie-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
tk=Tk()
tk.title("SmajloSlovakian™")
tk.protocol("WM_DELETE_WINDOW",koniec)
pr=Canvas(tk,height=prY,width=prX,bg=prBG)
pr.grid(columnspan=200)

#Setup------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
gui.setup(pr)
setup(pr,gui)
Window(záznamyapp)

#Loop-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
start=time()
tick=time()
tick2=1
while áno:
    
    gui.updatelem(tick2)
    Window.updall(tick2)
    gui.updatetools()
    tk.update()
    psleep(nonneg(minms-(time()-tick)))
    print(fps(tick),end="            \r")
    tick2=time()-tick
    tick=time()

#Koniec-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("\nprogram končí                                                            ")
tk.update()