#Nastavenia-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from time import *
from math import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mbox
from random import *
import os
import smajlotkgui05 as gui
from WinDesMan2 import *
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    print("DPI nastavenia neboli použité.")
áno=True
prY,prX,minms=1080,1920, 1/120
prBG="#000"
tick=0
spomalenie=1
flscr=True


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


class app1(WindowedApp):
    label="DVD^2"
    def icon(c,x,y,tags):
        pr.create_rectangle(x-10,y-10,x+10,y+10,fill="red",tags=tags)

    def update(c,clicking,hover,v,t):
        t*=120
        c.objs.sort(key=sortbyxpos)
        act=[]
        poscol=set()
        for l in c.objs:
            act=[b for b in act if b.px+b.rad>b.px-b.rad]
            for ab in act:
                if(l.px-l.rad<ab.px+ab.rad):
                    poscol.add((l,ab))
            act.append(l)

        for i in c.objs:
            i.px+=i.sx*t
            i.py+=i.sy*t
            if i.px+i.rad>c.dx:
                i.px=(i.px+i.rad-c.dx)*-1-i.rad+c.dx
                i.sx*=-1
            elif i.px-i.rad<0:
                i.px=(i.px-i.rad)*-1+i.rad
                i.sx*=-1
            if i.py+i.rad>c.dy:
                i.py=(i.py+i.rad-c.dy)*-1-i.rad+c.dy
                i.sy*=-1
            elif i.py-i.rad<0:
                i.py=(i.py-i.rad)*-1+i.rad
                i.sy*=-1
            i.wf=0,0
        
        for p in poscol:
            for k in range(2):
                if(k==0):
                    i=p[0]
                    o=p[1]
                else:
                    i=p[1]
                    o=p[0]
                if o.px-i.rad<=i.px+i.rad<=o.px+i.rad and o.py-o.rad<=i.py<=o.py+o.rad:
                    l=o.px
                    i.px=o.px-o.rad-i.rad
                    #o.px=l+i.rad+o.rad
                    i.sx+=o.sx
                    o.sx=i.sx-o.sx
                    i.sx=i.sx-o.sx
                if o.py-i.rad<=i.py+i.rad<=o.py+i.rad and o.px-o.rad<=i.px<=o.px+o.rad:
                    l=o.py
                    i.py=o.py-o.rad-i.rad
                    #o.py=l+i.rad+o.rad
                    i.sy+=o.sy
                    o.sy=i.sy-o.sy
                    i.sy=i.sy-o.sy
        for i in c.objs:
            pr.moveto(str(c)+str(i.id),round(c.x+i.px-i.rad),round(c.y+i.py-i.rad))
    
    def draw(c):
        pr.delete(str(c))
        for i in c.objs:
            pr.create_rectangle(c.x+i.px-i.rad,c.y+i.py-i.rad,c.x+i.px+i.rad,c.y+i.py+i.rad,fill="red",tags=c.tags+[str(c),str(c)+str(i.id)])

    def click(c, rx, ry):
        super().click(rx, ry)
        la=square()
        la.id=len(c.objs)
        la.wf=0,0
        la.sx=random()*3*choice((1,-1))
        la.sy=random()*3*choice((1,-1))
        la.rad=10
        la.px=rx
        la.py=ry
        c.objs+=[la]
        c.draw()

    def __init__(c, tags,window) -> None:
        super().__init__(tags,window)
        c.objs=[square()]
        for i in c.objs:
            i.id=0
            i.wf=0,0
            i.sx=random()*3*choice((1,-1))
            i.sy=random()*3*choice((1,-1))
            i.rad=10
            i.px=10
            i.py=10

class app2(WindowedApp):
    label="Physics squares"
    smallest=1,1
    def icon(c,x,y,tags):
        pr.create_rectangle(x-10,y-10,x+10,y+10,fill="green",tags=tags)

    def update(c,clicking,hover,v,t):
        t*=120
        c.objs.sort(key=sortbyxpos)
        act=[]
        poscol=set()
        for l in c.objs:
            act=[b for b in act if b.px+b.rad>b.px-b.rad]
            for ab in act:
                if(l.px-l.rad<ab.px+ab.rad):
                    poscol.add((l,ab))
            act.append(l)

        for i in c.objs:
            i.px+=i.sx*t
            i.py+=i.sy*t
            i.sx*=0.995**t
            i.sy*=0.995**t
            i.sy+=0.5*t
            if i.px+i.rad>c.dx:
                i.px=(i.px+i.rad-c.dx)*-1-i.rad+c.dx
                i.sx*=-0.5
                i.sx+=i.wf[0]
            elif i.px-i.rad<0:
                i.px=(i.px-i.rad)*-1+i.rad
                i.sx*=-0.5
                i.sx+=i.wf[0]
            if i.py+i.rad>c.dy:
                i.py=(i.py+i.rad-c.dy)*-1-i.rad+c.dy
                i.sy*=-0.5
                i.sy+=i.wf[1]
            elif i.py-i.rad<0:
                i.py=(i.py-i.rad)*-1+i.rad
                i.sy*=-0.5
                i.sy+=i.wf[1]
            i.wf=0,0
        
        for p in poscol:
            for k in range(2):
                if(k==0):
                    i=p[0]
                    o=p[1]
                else:
                    i=p[1]
                    o=p[0]
                if o.px-i.rad<=i.px+i.rad<=o.px+i.rad and o.py-o.rad<=i.py<=o.py+o.rad:
                    l=o.px
                    i.px=o.px-o.rad-i.rad
                    #o.px=l+i.rad+o.rad
                    i.sx*=0.5
                    o.sx*=0.5
                    i.sx+=o.sx
                    o.sx=i.sx-o.sx
                    i.sx=i.sx-o.sx
                if o.py-i.rad<=i.py+i.rad<=o.py+i.rad and o.px-o.rad<=i.px<=o.px+o.rad:
                    l=o.py
                    i.py=o.py-o.rad-i.rad
                    #o.py=l+i.rad+o.rad
                    i.sy*=0.5
                    o.sy*=0.5
                    i.sy+=o.sy
                    o.sy=i.sy-o.sy
                    i.sy=i.sy-o.sy
        for i in c.objs:
            pr.moveto(str(c)+str(i.id),round(c.x+i.px-i.rad),round(c.y+i.py-i.rad))

    def draw(c):
        pr.delete(str(c))
        for i in c.objs:
            pr.create_rectangle(c.x+i.px-i.rad,c.y+i.py-i.rad,c.x+i.px+i.rad,c.y+i.py+i.rad,fill="green",tags=c.tags+[str(c),str(c)+str(i.id)])

    def moved(c, x, y, dx, dy):
        for i in c.objs:
            i.px-=x-c.x
            i.py-=y-c.y
            i.wf=x-c.x,y-c.y
        super().moved(x, y, dx, dy)

    def click(c, rx, ry):
        super().click(rx, ry)
        la=square()
        la.id=len(c.objs)
        la.wf=0,0
        la.sx=0
        la.sy=0
        la.rad=10
        la.px=rx
        la.py=ry
        c.objs+=[la]
        c.draw()

    def __init__(c, tags,window) -> None:
        super().__init__(tags,window)
        c.objs=[square()]
        for i in c.objs:
            i.id=0
            i.wf=0,0
            i.sx=random()*3*choice((1,-1))
            i.sy=random()*3*choice((1,-1))
            i.rad=10
            i.px=0
            i.py=0


class app3(WindowedApp):
    label="Physics circles"
    smallest=1,1
    def icon(c,x,y,tags):
        pr.create_oval(x-10,y-10,x+10,y+10,fill="green",tags=tags)

    def update(c,clicking,hover,v,t):
        t*=120
        c.objs.sort(key=sortbyxpos)
        act=[]
        poscol=set()
        for l in c.objs:
            act=[b for b in act if b.px+b.rad>b.px-b.rad]
            for ab in act:
                if(l.px-l.rad<=ab.px+ab.rad):
                    poscol.add((l,ab))
            act.append(l)

        for i in c.objs:
            i.px+=i.sx*t
            i.py+=i.sy*t
            i.sx*=0.995**t
            i.sy*=0.995**t
            #i.sy+=0.5*t
            if i.px+i.rad>=c.dx:
                i.px=(i.px+i.rad-c.dx)*-1-i.rad+c.dx
                i.sx*=-0.5
                i.sx+=i.wf[0]
            elif i.px-i.rad<=0:
                i.px=(i.px-i.rad)*-1+i.rad
                i.sx*=-0.5
                i.sx+=i.wf[0]
            if i.py+i.rad>=c.dy:
                i.py=(i.py+i.rad-c.dy)*-1-i.rad+c.dy
                i.sy*=-0.5
                i.sy+=i.wf[1]
            elif i.py-i.rad<=0:
                i.py=(i.py-i.rad)*-1+i.rad
                i.sy*=-0.5
                i.sy+=i.wf[1]
            i.wf=0,0
        
        for p in poscol:
            i=p[0]
            o=p[1]
            d=sqrt((i.px-o.px)**2+(i.py-o.py)**2)
            if(d==0):
                d=0.01
            if(d<=i.rad+o.rad):
                overlap=(d-i.rad-o.rad)/2

                i.px-=(i.px-o.px)/d*overlap
                i.py-=(i.py-o.py)/d*overlap

                o.px+=(i.px-o.px)/d*overlap
                o.py+=(i.py-o.py)/d*overlap

                '''nx=(o.px-i.px)/d
                ny=(o.py-i.py)/d

                kx = (i.sx - o.sx)
                ky = (i.sy - o.sy)
                p = 2.0 * (nx * kx + ny * ky) / (i.mass + o.mass)
                i.sx = i.sx - p * o.mass * nx
                i.sy = i.sy - p * o.mass * ny
                o.sx = o.sx + p * i.mass * nx
                o.sy = o.sy + p * i.mass * ny'''
        for i in c.objs:
            pr.moveto(str(c)+str(i.id),round(c.x+i.px-i.rad),round(c.y+i.py-i.rad))

    def draw(c):
        pr.delete(str(c))
        for i in c.objs:
            pr.create_oval(c.x+i.px-i.rad,c.y+i.py-i.rad,c.x+i.px+i.rad,c.y+i.py+i.rad,fill="green",tags=c.tags+[str(c),str(c)+str(i.id)])

    def moved(c, x, y, dx, dy):
        for i in c.objs:
            i.px-=x-c.x
            i.py-=y-c.y
            i.wf=x-c.x,y-c.y
        super().moved(x, y, dx, dy)

    def click(c, rx, ry):
        super().click(rx, ry)
        la=square()
        la.id=len(c.objs)
        la.wf=0,0
        la.sx=0
        la.sy=0
        la.rad=10
        la.mass=1
        la.px=rx
        la.py=ry
        c.objs+=[la]
        c.draw()

    def __init__(c, tags,window) -> None:
        super().__init__(tags,window)
        c.objs=[square()]
        for i in c.objs:
            i.id=0
            i.wf=0,0
            i.sx=random()*3*choice((1,-1))
            i.sy=random()*3*choice((1,-1))
            i.rad=10
            i.mass=1
            i.px=0
            i.py=0


class app4(WindowedApp):
    label="DVD^0"
    smallest=1,1
    def icon(c,x,y,tags):
        pr.create_oval(x-10,y-10,x+10,y+10,fill="red",tags=tags)

    def update(c,clicking,hover,v,t):
        t*=120
        c.objs.sort(key=sortbyxpos)
        act=[]
        poscol=set()
        for l in c.objs:
            act=[b for b in act if b.px+b.rad>b.px-b.rad]
            for ab in act:
                if(l.px-l.rad<=ab.px+ab.rad):
                    poscol.add((l,ab))
            act.append(l)

        for i in c.objs:
            i.px+=i.sx*t
            i.py+=i.sy*t
            if i.px+i.rad>=c.dx:
                i.px=(i.px+i.rad-c.dx)*-1-i.rad+c.dx
                i.sx*=-1
            elif i.px-i.rad<=0:
                i.px=(i.px-i.rad)*-1+i.rad
                i.sx*=-1
            if i.py+i.rad>=c.dy:
                i.py=(i.py+i.rad-c.dy)*-1-i.rad+c.dy
                i.sy*=-1
            elif i.py-i.rad<=0:
                i.py=(i.py-i.rad)*-1+i.rad
                i.sy*=-1
        
        for p in poscol:
            i=p[0]
            o=p[1]
            d=sqrt((i.px-o.px)**2+(i.py-o.py)**2)
            if(d<=i.rad+o.rad):
                overlap=(d-i.rad-o.rad)/2

                i.px-=(i.px-o.px)/d*overlap
                i.py-=(i.py-o.py)/d*overlap

                o.px+=(i.px-o.px)/d*overlap
                o.py+=(i.py-o.py)/d*overlap

                nx,ny=(o.px-i.px)/d,(o.py-i.py)/d
                tx,ty=-ny,nx

                dpt1=i.sx*tx+i.sy*ty
                dpt2=o.sx*tx+o.sy*ty

                dpn1=i.sx*nx+i.sy*ny
                dpn2=o.sx*nx+o.sy*ny

                m1=(dpn1*(i.mass-o.mass)+2*o.mass*dpn2)/(i.mass+o.mass)
                m2=(dpn2*(o.mass-i.mass)+2*i.mass*dpn1)/(i.mass+o.mass)

                i.sx=(tx*dpt1+nx*m1)
                i.sy=(ty*dpt1+ny*m1)
                o.sx=(tx*dpt2+nx*m2)
                o.sy=(ty*dpt2+ny*m2)
        for i in c.objs:
            pr.moveto(str(c)+str(i.id),round(c.x+i.px-i.rad),round(c.y+i.py-i.rad))

    def draw(c):
        pr.delete(str(c))
        for i in c.objs:
            pr.create_oval(c.x+i.px-i.rad,c.y+i.py-i.rad,c.x+i.px+i.rad,c.y+i.py+i.rad,fill="red",tags=c.tags+[str(c),str(c)+str(i.id)])

    def moved(c, x, y, dx, dy):
        for i in c.objs:
            i.px-=x-c.x
            i.py-=y-c.y
            i.wf=x-c.x,y-c.y
        super().moved(x, y, dx, dy)

    def click(c, rx, ry):
        super().click(rx, ry)
        la=square()
        la.id=len(c.objs)
        la.wf=0,0
        la.sx=random()*3*choice((1,-1))
        la.sy=random()*3*choice((1,-1))
        la.rad=25
        la.mass=1
        la.px=rx
        la.py=ry
        c.objs+=[la]
        c.draw()

    def __init__(c, tags,window) -> None:
        super().__init__(tags,window)
        c.objs=[square()]
        for i in c.objs:
            i.id=0
            i.wf=0,0
            i.sx=random()*3*choice((1,-1))
            i.sy=random()*3*choice((1,-1))
            i.rad=25
            i.mass=1
            i.px=0
            i.py=0

class hodiny(WindowedApp):
    label="Clock"
    dimensions=150,30
    def icon(c, x, y, tags):
        pr.create_oval(x-15,y-15,x+15,y+15,tags=tags)
        pr.create_line(x,y-13,x,y,x+13,y,tags=tags)
    def update(c, clicking, hover, v,t):
        if strftime("%H:%M:%S")!=c.pred:
            c.draw()

    def draw(c):
        pr.delete(str(c))
        c.pred=strftime("%H:%M:%S")
        pr.create_text(c.x+c.dx/2,c.y+c.dy/2,text=c.pred,font="Arial 20",tags=c.tags+[str(c)])

    def __init__(c, tags,window) -> None:
        c.pred=""
        super().__init__(tags,window)
            

class makeocircle(WindowedApp):
    label="Make o'Circle"
    def icon(c,x,y,tags):
        pr.create_oval(x-10,y-15,x+10,y+15,tags=tags)
    def click(c,rx,ry):
        pr.create_oval(c.x+rx,c.y+ry,c.x+rx+60,c.y+ry+70,tags=c.tags)

class quitapp(WindowedApp):
    label="Power down"
    dimensions=250,100
    def icon(c, x, y, tags):
        pr.create_oval(x-15,y-15,x+15,y+15,width=3,tags=tags)
        pr.create_line(x,y-12,x,y-16,width=10,tags=tags,fill="white")
        pr.create_line(x,y,x,y-20,width=3,tags=tags)

    def update(c, clicking, hover,v:Window,t):
        super().update(clicking,hover,v,t)
        c.tl1.layer=v.mask.layer
        if c.tl1.stat==3:
            c.quitting=True
            for i in Window._reg:
                i.fading=-Window.faspeed
        if c.quitting and v.fadetick<=1:
            koniec()
    
    def draw(c):
        super().draw()
        pr.delete(str(c)+"txt")
        pr.create_text(c.dx/2+c.x,c.dy/5+c.y,text="Are you sure you want to quit?",tags=c.tags+[str(c)+"txt"])
    
    def __init__(c, tags,window) -> None:
        super().__init__(tags,window)
        c.quitting=False
        c.tl1=gui.Button(c.dx/2+c.x,c.dy/3*2+c.y,"Yes, quit.",tags=c.tags,ActiDim=adim).activate()
        c.guielements+=[c.tl1]

class fpser(WindowedApp):
    label="SetFPS"
    dimensions=250,200
    def icon(c, x, y, tags):
        pr.create_rectangle(x-15,y-10,x+15,y+10,width=3,fill="cyan",stipple=gui.trasluc(4),tags=tags)
        pr.create_line(x-15,y-3,x+15,y-3,width=1,tags=tags)
        pr.create_line(x,y+10,x,y+15,width=2,tags=tags)
        pr.create_line(x-5,y+15,x+5,y+15,width=3,tags=tags)

    def update(c, clicking, hover,v:Window,t):
        super().update(clicking,hover,v,t)
        global minms,spomalenie
        if c.tl1.stat==2:
            c.tl1.dval=c.tl1.conval
            minms=1/c.tl1.conval
        if c.tl2.stat==2:
            c.tl2.dval=c.tl2.conval
            spomalenie=c.tl2.conval
    
    def draw(c):
        super().draw()
        pr.delete(str(c)+"txt")
        pr.create_text(c.dx/2+c.x,c.dy/5+c.y,text="Set it just like you want to...",tags=c.tags+[str(c)+"txt"])
    
    def __init__(c, tags,window) -> None:
        super().__init__(tags,window)
        c.quitting=False
        c.tl1=gui.Slider(c.dx/2+c.x,c.dy/4*2+c.y,"{} FPS",Min=1,Max=360,IsInt=True,DisplayVal=int(1/minms),DefaultValue=1/minms,tags=tags,ActiDim=adim).activate()
        c.tl2=gui.Slider(c.dx/2+c.x,c.dy/4*3+c.y,"Spomalenie: {}x",Min=0.1,Max=100,IsInt=False,DisplayVal=spomalenie,DefaultValue=spomalenie,tags=tags,ActiDim=adim).activate()
        c.guielements+=[c.tl1,c.tl2]

class fullscreentoggle(WindowedApp):
    label="Toggle fullscreen"
    def icon(c, x, y, tags):
        if(flscr):
            pr.create_line(x-10,y-3,x-3,y-3,x-3,y-10,width=2,tags=tags)
            pr.create_line(x+10,y+3,x+3,y+3,x+3,y+10,width=2,tags=tags)
            pr.create_line(x+10,y-3,x+3,y-3,x+3,y-10,width=2,tags=tags)
            pr.create_line(x-10,y+3,x-3,y+3,x-3,y+10,width=2,tags=tags)
        else:
            pr.create_line(x-10,y-3,x-10,y-10,x-3,y-10,width=2,tags=tags)
            pr.create_line(x+10,y+3,x+10,y+10,x+3,y+10,width=2,tags=tags)
            pr.create_line(x+10,y-3,x+10,y-10,x+3,y-10,width=2,tags=tags)
            pr.create_line(x-10,y+3,x-10,y+10,x-3,y+10,width=2,tags=tags)
    
    def __init__(c, tags,window) -> None:
        global flscr
        super().__init__(tags,window)
        window.fading=-window.faspeed
        flscr=not(flscr)
        tk.attributes('-fullscreen', flscr)

class mínylauncher(WindowedApp):
    label="Míny"
    def icon(c, x, y, tags):
        pr.create_text(x,y,text="🚩",font="Arial 20",tags=tags)
    def update(c, clicking, hover, v: Window, t):
        super().update(clicking, hover, v, t)
        if(c.gtl1.stat==3):
            print("la")
            Window(WindowedApp)
        '''if(c.menustate==0):
            if(v.infocus and hover[1]>0 and gui.transclick("r1")):
                c.menustate=1
                pr.delete(str(c)+"pressstart")
                c.gtl1.activate()
        elif(c.menustate==1):
            if(c.gtl1.stat==3):
                c.gtl1.deactivate()
                c.menustate=2
        elif(c.menustate==2):
            4'''
    def draw(c):
        super().draw()
        if(c.menustate==0):
            pr.delete(str(c)+"pressstart")
            pr.create_text(c.x+c.dx/2,c.y+c.dy/2,text="Míny",tags=c.tags+[str(c)+"pressstart"])
        elif(c.menustate==2):
            4
    def __init__(c, tags, window: Window) -> None:
        super().__init__(tags, window)
        c.gtl1=gui.Button(c.dx/2+c.x,c.dy/4*2+c.y,"Spustiť",ActiDim=adim).activate()
        c.guielements+=[c.gtl1]
        c.menustate=0

class square:
    def __init__(c) -> None:
        pass
def sortbyxpos(o):
    return o.px
#Prostredie-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
tk=Tk()
tk.title("SmajloSlovakian™")
tk.protocol("WM_DELETE_WINDOW",koniec)
pr=Canvas(tk,height=prY,width=prX,bg=prBG)
pr.grid(columnspan=200)

#Setup------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
setup(pr,gui, quitapp,hodiny,app1,makeocircle,WindowedApp,app2,fpser,fullscreentoggle,mínylauncher,app3,app4)
gui.setup(pr)
tk.attributes('-fullscreen', True)
Window(app=appdrawer)
adim=(10,2.5,-10,-2.5,0,0)

#Loop-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
start=time()
tick=time()
tick2=1
while áno:
    pr.configure(height=tk.winfo_height(),width=tk.winfo_width())

    gui.updatelem(tick2)
    Window.updall(tick2)
    gui.updatetools()
    tk.update() #simple 120hz lock VV
    psleep(nonneg(minms-(time()-tick)))
    print(fps(tick),"    ",end="\r")
    pr.delete("refresh")
    tick2=(time()-tick)/spomalenie
    tick=time()

#Koniec-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("\nprogram končí                                                            ")
tk.update()
