#Nastavenia-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from time import *
from math import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mbox
from random import *
import winsound as ws
import os
import smajlotkgui04 as gui
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
MEDIA="C:\\Windows\\Media\\"
timeout=3   #sec
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

def okolo(x,y):
    return [x-1,y-1],[x-1,y],[x-1,y+1],[x,y-1],[x,y+1],[x+1,y-1],[x+1,y],[x+1,y+1]

def vyhrAnim(t,p): #p[4]=1.1, p[5]=2, p[6]=2
    x,y=p[0:2]
    tt=-t
    if p[2]:
        pr.create_text(x-t*p[5],y+p[4]**(t-1)-t*p[6],text=p[3],tags="refresh",font="Arial "+str(int(mo.scale/1.5)))
    else:
        pr.create_text(x-tt*p[5],y+p[4]**(t-1)-t*p[6],text=p[3],tags="refresh",font="Arial "+str(int(mo.scale/1.5)))


class bounce:
    _reg=[]
    def updall(tick):
        for i in bounce._reg:
            i.update(tick)

    def update(c,t):
        t/=0.008333333333333333333333
        c.x+=c.fx/2*t
        c.y+=c.fy/2*t
        c.fy+=c.g/2*t
        if c.y>prY and c.count>0:
            c.fy*=-0.8
            c.y=(c.y-prY)*-1+prY
            c.count-=1
        elif c.y>prY+100 and c.count<=0:
            pr.delete(c.txt)
            c._reg.remove(c)
        if c.x>prX:
            c.fx*=-0.8
            c.x=(c.x-prX)*-1+prX
        if c.x<0:
            c.fx*=-0.8
            c.x*=-1
        pr.moveto(c.txt,c.x+c.offx,c.y+c.offx)
        pr.tag_raise(c.txt)
        
    def __init__(c,x,y,text,count,fx,fy,gravity,offX=0,offY=0) -> None:
        #count=randint(0,5),fx=random()*6-3,fy=random()*6-3,gravity=random()+1
        c._reg.append(c)
        c.x=x
        c.y=y
        c.fx=fx
        c.fy=fy
        c.offx=offX
        c.offy=offY
        c.g=gravity
        c.count=count
        c.txt=text

class uncover:
    _reg=[]
    def updall(tick):
        for i in uncover._reg:
            i.update(tick)

    def update(c,t):
        t/=0.008333333333333333333333
        c.xx-=c.fx*t
        c.yy-=c.fy*t
        if c.xx<=c.x:
            c.fx=0
        if c.yy<=c.y:
            c.fy=0
        if c.xx<=c.x and c.yy<=c.y:
            c._reg.remove(c)
        pr.create_rectangle(c.x,c.y,c.xx,c.yyy,width=0,tags="refresh",fill="grey")
        pr.create_rectangle(c.x,c.y,c.xxx,c.yy,width=0,tags="refresh",fill="grey")
        
    def __init__(c,x,y,xx,yy,fx=1,fy=1) -> None:
        #count=randint(0,5),fx=random()*6-3,fy=random()*6-3,gravity=random()+1
        c._reg.append(c)
        c.x=x
        c.y=y
        c.fx=fx
        c.fy=fy
        c.xx=xx
        c.yy=yy
        c.xxx=xx
        c.yyy=yy

class míny:
    def __init__(c,x,y,Vx,Vy,scale) -> None:
        c.tab=[] # číslo, otvorené bool, vlajka bool, bomba bool
        for i in range(Vx):
            c.tab.append([])
            for o in range(Vy):
                c.tab[i].append([])
        c.bomby=0
        c.posX=x
        c.posY=y
        c.generovať=True
        c.scale=scale
        c.hrať=True

    def draw(c):
        pr.delete("míny")
        for i in range(len(c.tab)):
            for o in range(len(c.tab[i])):
                if c.generovať:
                    pr.create_rectangle(c.posX+i*c.scale,c.posY+o*c.scale,c.posX+i*c.scale+c.scale,c.posY+o*c.scale+c.scale,fill="grey",tags="míny")
                else:
                    if c.tab[i][o][1]:
                        farba="white"
                    else:
                        farba="grey"
                    pr.create_rectangle(c.posX+i*c.scale,c.posY+o*c.scale,c.posX+i*c.scale+c.scale,c.posY+o*c.scale+c.scale,fill=farba,tags="míny")
                    if c.tab[i][o][1]:
                        if c.tab[i][o][3]:
                            pr.create_text(c.posX+i*c.scale+c.scale/2,c.posY+o*c.scale+c.scale/2,text="☢",tags="míny",font="Arial "+str(int(c.scale/1.5)),fill="red")
                        else:
                            pr.create_text(c.posX+i*c.scale+c.scale/2,c.posY+o*c.scale+c.scale/2,text=c.tab[i][o][0],tags="míny",font="Arial "+str(int(c.scale/1.5)))
                    if c.tab[i][o][2]:
                        pr.create_text(c.posX+i*c.scale+c.scale/2,c.posY+o*c.scale+c.scale/2,text="🚩",tags="míny",font="Arial "+str(int(c.scale/1.5)))

    def click(c,x,y,draw=True):
        if not c.hrať:
            return
        xc,yc=int((x-c.posX)/c.scale),int((y-c.posY)/c.scale)
        if 0<(x-c.posX)/c.scale<len(c.tab) and 0<(y-c.posY)/c.scale<len(c.tab[0]):
            while c.generovať:
                c.generate()
                if not c.tab[xc][yc][3] and c.tab[xc][yc][0]==0:
                    c.generovať=False
            if not c.tab[xc][yc][2]:
                c.uncover(xc,yc)
                if c.tab[xc][yc][3]:
                    c.hrať=False
                    for i in range(len(c.tab)):
                        for o in range(len(c.tab[i])):
                            if c.tab[i][o][2] and c.tab[i][o][3]:
                                #gui.Animation(vyhrAnim,120,params=(c.posX+i*c.scale+c.scale/2, c.posY+o*c.scale+c.scale/2, randint(0,1), "🎏", 1.1,2,2))
                                bounce(c.posX+i*c.scale+c.scale/2,c.posY+o*c.scale+c.scale/2,pr.create_text(c.posX+i*c.scale+c.scale/2,c.posY+o*c.scale+c.scale/2,text="🚩",font="Arial "+str(int(mo.scale/1.5))),randint(0,10),fx=random()*30-15,fy=random()*30-15,gravity=random()+1)
                            if c.tab[i][o][3]:
                                c.uncover(i,o)
            c.draw()
            c.čekvýhr()

    def vlajka(c,x,y):
        if not c.hrať:
            return
        xc,yc=int((x-c.posX)/c.scale),int((y-c.posY)/c.scale)
        if not c.generovať:
            if 0<(x-c.posX)/c.scale<len(c.tab) and 0<(y-c.posY)/c.scale<len(c.tab[0]) and not c.tab[xc][yc][1]:
                if c.tab[xc][yc][2]:
                    bounce(c.posX+xc*c.scale+c.scale/2,c.posY+yc*c.scale+c.scale/2,pr.create_text(c.posX+xc*c.scale+c.scale/2,c.posY+yc*c.scale+c.scale/2,text="🚩",font="Arial "+str(int(mo.scale/1.5))),randint(0,10),fx=random()*30-15,fy=random()*30-15,gravity=random()+1)
                else:
                    uncover(c.posX+xc*c.scale+1,c.posY+yc*c.scale+1, c.posX+xc*c.scale+c.scale-1,c.posY+yc*c.scale+c.scale-1,2,2)
                c.tab[xc][yc][2]=not c.tab[xc][yc][2]
                c.draw()
        c.čekvýhr()

    def generate(c):
        for i in range(len(c.tab)):
            for o in range(len(c.tab[i])):
                bomba=choice([True]+[False]*gsl2.conval)
                c.tab[i][o]=[0,False,False,bomba]
                if bomba:c.bomby+=1
        for i in range(len(c.tab)):
            for o in range(len(c.tab[i])):
                bombopoc=0
                for z,t in okolo(i,o):
                    if z>=0 and t>=0 and z<len(c.tab) and t<len(c.tab[i]):
                        if c.tab[z][t][3]:
                            bombopoc+=1
                c.tab[i][o][0]=bombopoc

    def uncover(c,xc,yc):
        if c.tab[xc][yc][1]==False:
            c.tab[xc][yc][2]=False
            c.tab[xc][yc][1]=True
            bounce(c.posX+xc*c.scale+c.scale/2,c.posY+yc*c.scale+c.scale/2,pr.create_rectangle(c.posX+xc*c.scale,c.posY+yc*c.scale, c.posX+xc*c.scale+c.scale,c.posY+yc*c.scale+c.scale,fill="grey"),count=randint(0,5),fx=random()*10-5,fy=random()*30-15,gravity=random()+1,offX=-c.scale/2-1,offY=-c.scale/2-1)#,count=randint(0,5),fx=random()*30-15,fy=random()*30-15,gravity=random()+1)
            if c.tab[xc][yc][0]==0 and not c.tab[xc][yc][3]:
                for z,t in okolo(xc,yc):
                    if z>=0 and t>=0 and z<len(c.tab) and t<len(c.tab[1]):
                        if not c.tab[z][t][1]:
                            c.uncover(z,t)

    def čekvýhr(c):
        if c.generovať:
            return
        for i in c.tab:
            for o in i:
                if not(o[1]) and not(o[2]):
                    return
                if o[3] and o[1]:
                    return
        c.vyhra()

    def vyhra(c):
        c.hrať=False
        for i in range(len(c.tab)):
            for o in range(len(c.tab[0])):
                if not c.tab[i][o][3]:
                    #gui.Animation(vyhrAnim,120,params=(c.posX+i*c.scale+c.scale/2, c.posY+o*c.scale+c.scale/2, randint(0,1), c.tab[i][o][0], randint(11,20)/10,randint(10,30)/10,randint(10,20)/10))
                    bounce(c.posX+i*c.scale+c.scale/2,c.posY+o*c.scale+c.scale/2,pr.create_text(c.posX+i*c.scale+c.scale/2,c.posY+o*c.scale+c.scale/2,text=c.tab[i][o][0],font="Arial "+str(int(mo.scale/1.5))),count=randint(0,5),fx=random()*30-15,fy=random()*30-15,gravity=random()+1)
                    c.tab[i][o][0]=""
        c.draw()


#Prostredie-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
tk=Tk()
tk.title("SmajloSlovakian™")
tk.protocol("WM_DELETE_WINDOW",koniec)
pr=Canvas(tk,height=prY,width=prX,bg=prBG)
pr.grid(columnspan=200)
gui.setup(pr)

#Setup------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
mo=míny(50,50,10,10,50)
mo.draw()

gtl1=gui.Button(800,100,"regen").activate()
gsl1=gui.Slider(800,150,"škála: {}",Min=1,Max=100,DefaultValue=50,IsInt=True,DisplayVal="50").activate()
gsl2=gui.Slider(800,200,"{}/1 šanca",Min=1,Max=200,DefaultValue=5,IsInt=True,DisplayVal="5").activate()

#Loop-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
start=time()
tick=time()
tick2=1
while áno:
    if gui.srelease:
        mo.click(gui.shover[0],gui.shover[1])
    if gui.srelease2:
        mo.vlajka(gui.shover[0],gui.shover[1])
    if gtl1.stat==3:
        mo.generovať=True
        mo.hrať=True
        mo.draw()
    if gsl1.stat==2:
        gsl1.dval=gsl1.conval
        mo.scale=gsl1.conval
        mo.draw()
    if gsl2.stat==2:
        gsl2.dval=gsl2.conval

    gui.updatelem(tick2)
    gui.updatetools()
    bounce.updall(tick2)
    uncover.updall(tick2)
    tk.update() #simple 120hz lock VV
    pr.delete("refresh")
    #psleep(nonneg(minms-(time()-tick)))
    print(fps(tick),end="                 \r")
    tick2=time()-tick
    tick=time()

#Koniec-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("program končí                                                            ")
ws.PlaySound(MEDIA+"tada.wav",10)
tk.update()
