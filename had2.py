#Nastavenia-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import os
from time import *
from math import *
from tkinter import *
from tkinter import messagebox as mbox
from random import *
import smajlotkgui05 as gui
import WinDesMan2 as wdm
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    print("dpi nastavenia neboli použité")
import astar
MEDIA="C:\\Windows\\Media\\"
timeout=-3   #sec
áno=True
prY=800
prX=1200
prBG="#fff"
tick=0
minms=1/120 #fps
fpská=[]
hadr=0
hadg=255
hadb=0


#had=Had(20,10,20,"#0d0",prehra)


#Definície--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Had:
    def draw(c):
        if(not(c.ježivý)):return()
        if c.timetolick<=0:
            c.timelicking-=1
            if c.timelicking<0:
                c.timelicking=30
                c.timetolick=randint(0,120*5)
        else:
            c.timetolick-=1
        if(chvostdir and not(chvostredrawop)):
            a=((c.maxtime-c.timer)/c.maxtime)-1
        else:
            a=0
        pr.delete(str(c)+"h")
        if chvostredrawop:
            if len(c.chvost)>len(c.renew) or c.timer==c.maxtime-1:
                c.renew.append(
                    pr.create_rectangle(
                        c.x*c.scale+c.pos[0],
                        c.y*c.scale+c.pos[1],
                        c.x*c.scale+c.pos[0]+c.scale,
                        c.y*c.scale+c.pos[1]+c.scale,
                        fill=c.farb,tags=(str(c)+"ch","had",str(c)),width=1,stipple=c.stipp))
            if len(c.chvost)<len(c.renew)-1:
                pr.delete(c.renew[0])
                del c.renew[0]
        else:
            pr.delete(str(c)+"ch")
        for x,y,z in c.chvost:
            if(z>=0):
                x*=c.scale
                y*=c.scale
                if not chvostredrawop:
                    try:
                        pr.create_rectangle(
                            x+c.pos[0]+c.scale*a*dirtran(z)[0],
                            y+c.pos[1]+c.scale*a*dirtran(z)[1],
                            x+c.scale+c.pos[0]+c.scale*a*dirtran(z)[0],
                            y+c.scale+c.pos[1]+c.scale*a*dirtran(z)[1],
                            fill=c.farb,tags=(str(c)+"ch","had",str(c)),width=1,stipple=c.stipp)
                    except:
                        pass
                elif chvostdir:
                    b=((c.maxtime-c.timer)/c.maxtime)
                    if z==0:
                        pr.create_line(x+c.pos[0]+c.scale*b,y+c.pos[1],                 x+c.pos[0]+c.scale*b,y+c.pos[1]+c.scale, tags=(str(c)+"h","had",str(c)),width=3,stipple=c.stipp)
                    elif z==1:
                        pr.create_line(x+c.pos[0],y+c.pos[1]+c.scale*b,                 x+c.pos[0]+c.scale,y+c.pos[1]+c.scale*b, tags=(str(c)+"h","had",str(c)),width=3,stipple=c.stipp)
                    elif z==2:
                        pr.create_line(x+c.pos[0]+c.scale-c.scale*b,y+c.pos[1]+c.scale, x+c.pos[0]+c.scale-c.scale*b,y+c.pos[1], tags=(str(c)+"h","had",str(c)),width=3,stipple=c.stipp)
                    elif z==3:
                        pr.create_line(x+c.pos[0]+c.scale,y+c.pos[1]+c.scale-c.scale*b, x+c.pos[0],y+c.pos[1]+c.scale-c.scale*b, tags=(str(c)+"h","had",str(c)),width=3,stipple=c.stipp)
        pr.create_rectangle(
            c.x*c.scale+c.pos[0]+c.scale*a*dirtran(c.dir)[0],
            c.y*c.scale+c.pos[1]+c.scale*a*dirtran(c.dir)[1],
            c.x*c.scale+c.pos[0]+c.scale*a*dirtran(c.dir)[0]+c.scale,
            c.y*c.scale+c.pos[1]+c.scale*a*dirtran(c.dir)[1]+c.scale,
            fill=c.farb,tags=(str(c)+"h","had",str(c)),stipple=c.stipp)
        if c.timetolick<=0:
            t=15-abs(c.timelicking-15)
            if c.dir==0:
                pr.create_rectangle(
                    c.x*c.scale+c.pos[0]+c.scale+c.scale*a*dirtran(c.dir)[0],                   c.y*c.scale+c.pos[1]+c.scale/4+c.scale*a*dirtran(c.dir)[1],
                    c.x*c.scale+c.pos[0]+c.scale+t/15*c.scale*2+c.scale*a*dirtran(c.dir)[0],    c.y*c.scale+c.pos[1]+c.scale/4*3+c.scale*a*dirtran(c.dir)[1],
                    fill="red",tags=(str(c)+"h","had",str(c)),stipple=c.stipp
                    )
            elif c.dir==1:
                pr.create_rectangle(
                    c.x*c.scale+c.pos[0]+c.scale/4+c.scale*a*dirtran(c.dir)[0],                 c.y*c.scale+c.pos[1]+c.scale+c.scale*a*dirtran(c.dir)[1],
                    c.x*c.scale+c.pos[0]+c.scale/4*3+c.scale*a*dirtran(c.dir)[0],               c.y*c.scale+c.pos[1]+c.scale+t/15*c.scale*2+c.scale*a*dirtran(c.dir)[1],
                    fill="red",tags=(str(c)+"h","had",str(c)),stipple=c.stipp
                    )
            elif c.dir==2:
                pr.create_rectangle(
                    c.x*c.scale+c.pos[0]+c.scale*a*dirtran(c.dir)[0],                           c.y*c.scale+c.pos[1]+c.scale/4+c.scale*a*dirtran(c.dir)[1],
                    c.x*c.scale+c.pos[0]-t/15*c.scale*2+c.scale*a*dirtran(c.dir)[0],            c.y*c.scale+c.pos[1]+c.scale/4*3+c.scale*a*dirtran(c.dir)[1],
                    fill="red",tags=(str(c)+"h","had",str(c)),stipple=c.stipp
                    )
            elif c.dir==3:
                pr.create_rectangle(
                    c.x*c.scale+c.pos[0]+c.scale/4+c.scale*a*dirtran(c.dir)[0],                 c.y*c.scale+c.pos[1]+c.scale*a*dirtran(c.dir)[1],
                    c.x*c.scale+c.pos[0]+c.scale/4*3+c.scale*a*dirtran(c.dir)[0],               c.y*c.scale+c.pos[1]-t/15*c.scale*2+c.scale*a*dirtran(c.dir)[1],
                    fill="red",tags=(str(c)+"h","had",str(c)),stipple=c.stipp
                    )
        dt=dirtran(c.dir)
        pr.create_rectangle(
            c.x*c.scale+c.scale/2+c.pos[0]+dt[0]*c.scale/2-c.scale/5*dt[0]-c.scale/4*(1-abs(dt[0]))+c.scale*a*dirtran(c.dir)[0],
            c.y*c.scale+c.scale/2+c.pos[1]+dt[1]*c.scale/2-c.scale/5*dt[1]-c.scale/4*(1-abs(dt[1]))+c.scale*a*dirtran(c.dir)[1],
            c.x*c.scale+c.scale/2+c.pos[0]+dt[0]*c.scale/2-c.scale/5*dt[0]-c.scale/4*(1-abs(dt[0]))+c.scale*a*dirtran(c.dir)[0],
            c.y*c.scale+c.scale/2+c.pos[1]+dt[1]*c.scale/2-c.scale/5*dt[1]-c.scale/4*(1-abs(dt[1]))+c.scale*a*dirtran(c.dir)[1], outline="white",width=4*c.scale/20,tags=(str(c)+"h","had",str(c)),stipple=c.stipp
            )
        pr.create_rectangle(
            c.x*c.scale+c.scale/2+c.pos[0]+dt[0]*c.scale/2-c.scale/5*dt[0]+c.scale/4*(1-abs(dt[0]))+c.scale*a*dirtran(c.dir)[0],
            c.y*c.scale+c.scale/2+c.pos[1]+dt[1]*c.scale/2-c.scale/5*dt[1]+c.scale/4*(1-abs(dt[1]))+c.scale*a*dirtran(c.dir)[1],
            c.x*c.scale+c.scale/2+c.pos[0]+dt[0]*c.scale/2-c.scale/5*dt[0]+c.scale/4*(1-abs(dt[0]))+c.scale*a*dirtran(c.dir)[0],
            c.y*c.scale+c.scale/2+c.pos[1]+dt[1]*c.scale/2-c.scale/5*dt[1]+c.scale/4*(1-abs(dt[1]))+c.scale*a*dirtran(c.dir)[1], outline="white",width=4*c.scale/20,tags=(str(c)+"h","had",str(c)),stipple=c.stipp
            )
        pr.create_rectangle(
            c.x*c.scale+c.scale/2+c.pos[0]+dt[0]*c.scale/2-c.scale/10*dt[0]-c.scale/4*(1-abs(dt[0]))+c.scale*a*dirtran(c.dir)[0],
            c.y*c.scale+c.scale/2+c.pos[1]+dt[1]*c.scale/2-c.scale/10*dt[1]-c.scale/4*(1-abs(dt[1]))+c.scale*a*dirtran(c.dir)[1],
            c.x*c.scale+c.scale/2+c.pos[0]+dt[0]*c.scale/2-c.scale/10*dt[0]-c.scale/4*(1-abs(dt[0]))+c.scale*a*dirtran(c.dir)[0],
            c.y*c.scale+c.scale/2+c.pos[1]+dt[1]*c.scale/2-c.scale/10*dt[1]-c.scale/4*(1-abs(dt[1]))+c.scale*a*dirtran(c.dir)[1], width=4*c.scale/20,tags=(str(c)+"h","had",str(c)),stipple=c.stipp
            )
        pr.create_rectangle(
            c.x*c.scale+c.scale/2+c.pos[0]+dt[0]*c.scale/2-c.scale/10*dt[0]+c.scale/4*(1-abs(dt[0]))+c.scale*a*dirtran(c.dir)[0],
            c.y*c.scale+c.scale/2+c.pos[1]+dt[1]*c.scale/2-c.scale/10*dt[1]+c.scale/4*(1-abs(dt[1]))+c.scale*a*dirtran(c.dir)[1],
            c.x*c.scale+c.scale/2+c.pos[0]+dt[0]*c.scale/2-c.scale/10*dt[0]+c.scale/4*(1-abs(dt[0]))+c.scale*a*dirtran(c.dir)[0],
            c.y*c.scale+c.scale/2+c.pos[1]+dt[1]*c.scale/2-c.scale/10*dt[1]+c.scale/4*(1-abs(dt[1]))+c.scale*a*dirtran(c.dir)[1], width=4*c.scale/20,tags=(str(c)+"h","had",str(c)),stipple=c.stipp
            )
        
    def refresh(c):
        for i in range(len(c.contr)):
            if(c.contr[i] in gui.spress):
                c.dirch(i)

    def step(c):
        if(not(c.ježivý)):return()
        if c.isai:
            if(portalbarr and not fastai):
                c.m=astar.mriežka(c.velk[0]*3,c.velk[1]*3)
                ozač=c.m.bunky[c.x+c.velk[0]][c.y+c.velk[1]]
                for i in c.otherhads+[c]:
                    for x,y,z in i.chvost:
                        if(c.velk[0]>x>=0 and c.velk[1]>y>=0):
                            c.m.bunky[x][y].stav=1
                            c.m.bunky[x][y+c.velk[1]].stav=1
                            c.m.bunky[x][y+c.velk[1]*2].stav=1
                            c.m.bunky[x+c.velk[0]][y].stav=1
                            c.m.bunky[x+c.velk[0]][y+c.velk[1]].stav=1
                            c.m.bunky[x+c.velk[0]][y+c.velk[1]*2].stav=1
                            c.m.bunky[x+c.velk[0]*2][y].stav=1
                            c.m.bunky[x+c.velk[0]*2][y+c.velk[1]].stav=1
                            c.m.bunky[x+c.velk[0]*2][y+c.velk[1]*2].stav=1
                    if(not(c is i) and i.ježivý):
                        c.m.bunky[i.x][i.y].stav=1
                        c.m.bunky[i.x][i.y+c.velk[1]].stav=1
                        c.m.bunky[i.x][i.y+c.velk[1]*2].stav=1
                        c.m.bunky[i.x+c.velk[0]][i.y].stav=1
                        c.m.bunky[i.x+c.velk[0]][i.y+c.velk[1]].stav=1
                        c.m.bunky[i.x+c.velk[0]][i.y+c.velk[1]*2].stav=1
                        c.m.bunky[i.x+c.velk[0]*2][i.y].stav=1
                        c.m.bunky[i.x+c.velk[0]*2][i.y+c.velk[1]].stav=1
                        c.m.bunky[i.x+c.velk[0]*2][i.y+c.velk[1]*2].stav=1
                    

                c.m.bunky[c.x+c.velk[0]][c.y+c.velk[1]].stav=2
                if(c.aitarget[0]%c.velk[0]!=c.jabl[0]%c.velk[0] or c.aitarget[1]%c.velk[1]!=c.jabl[1]%c.velk[1]):
                    c.m.bunky[c.jabl[0]][c.jabl[1]].stav=3
                    c.m.bunky[c.jabl[0]][c.jabl[1]+c.velk[1]].stav=3
                    c.m.bunky[c.jabl[0]][c.jabl[1]+c.velk[1]*2].stav=3
                    c.m.bunky[c.jabl[0]+c.velk[0]][c.jabl[1]].stav=3
                    c.m.bunky[c.jabl[0]+c.velk[0]][c.jabl[1]+c.velk[1]].stav=3
                    c.m.bunky[c.jabl[0]+c.velk[0]][c.jabl[1]+c.velk[1]*2].stav=3
                    c.m.bunky[c.jabl[0]+c.velk[0]*2][c.jabl[1]].stav=3
                    c.m.bunky[c.jabl[0]+c.velk[0]*2][c.jabl[1]+c.velk[1]].stav=3
                    c.m.bunky[c.jabl[0]+c.velk[0]*2][c.jabl[1]+c.velk[1]*2].stav=3
                else:
                    c.m.bunky[c.aitarget[0]][c.aitarget[1]].stav=3
            else:
                c.m=astar.mriežka(c.velk[0],c.velk[1])
                ozač=c.m.bunky[c.x][c.y]
                for i in c.otherhads+[c]:
                    for x,y,z in i.chvost:
                        c.m.bunky[x][y].stav=1
                    if(not(c is i) and i.ježivý):
                        c.m.bunky[i.x][i.y].stav=1
                c.m.bunky[c.x][c.y].stav=2
                c.m.bunky[c.jabl[0]][c.jabl[1]].stav=3
            c.mm=c.m.find()
            if(c.mm!=[]):
                c.aitarget=[c.mm[0].x,c.mm[0].y]
                mmm=c.mm[-2]
                if(mmm.x-ozač.x==1):
                    c.dirchr()
                elif(mmm.x-ozač.x==-1):
                    c.dirchl()
                if(mmm.y-ozač.y==1):
                    c.dirchd()
                elif(mmm.y-ozač.y==-1):
                    c.dirchu()
            else:
                if(c.barrierc(c.x+dirtran(c.dir)[0],c.y) or c.barrierc(c.x,c.y+dirtran(c.dir)[1])):
                    c.dir=randint(0,3)
                elif(c.m.bunky[c.x+dirtran(c.dir)[0]][c.y+dirtran(c.dir)[1]].stav==1):
                    c.dir=randint(0,3)

            
        c.chvost.append([c.x,c.y,c.dir])
        c.dir=c.dirr
        c.polickacas+=1
        if(not(c.velk[0]>c.chvost[0][0]>=0) or not(c.velk[1]>c.chvost[0][1]>=0)):
            del c.chvost[0]
        del c.chvost[0]
        c.x+=dirtran(c.dir)[0]
        c.y+=dirtran(c.dir)[1]
        bar=c.barrierc(c.x,c.y)
        if bar[0]:
            if portalbarr:
                c.chvost.append([c.x,c.y,c.dir])
                c.x+=c.velk[0]*bar[1]
                c.y+=c.velk[1]*bar[2]
                c.aitarget=[c.aitarget[0]+c.velk[0]*bar[1],c.aitarget[1]+c.velk[1]*bar[2]]
            else:
                c.preh(c)

        for l in c.otherhads+[c]:
            if len(l.chvost)>1:
                for i in l.chvost:
                    if(i[0]==c.x and i[1]==c.y):
                        c.preh(c)
        if c.jabl[0]==c.x and c.jabl[1]==c.y:
            c.eat()
    
    def barrierc(c,x,y):
        ano=False
        dirx=0
        diry=0
        if x>=c.velk[0]:
            ano=True
            dirx=-1
        elif x<0:
            ano=True
            dirx=1
        if y>=c.velk[1]:
            ano=True
            diry=-1
        elif y<0:
            ano=True
            diry=1
        return ano,dirx,diry

    def eat(c):
        c.chvost.append([c.x,c.y,-1])
        c.renew.append(0)
        niesom=True
        maxim=1000
        while niesom and maxim>0:
            niesom=False
            maxim-=1
            c.jabl=[randrange(c.velk[0]),randrange(c.velk[1])]
            for i in c.otherhads+[c]:
                if c.jabl[0]!=i.x and c.jabl[1]!=i.y:
                    for x,y,z in i.chvost:
                        if c.jabl[0]==x and c.jabl[1]==y:
                            niesom=True
                else:
                    niesom=True
        for i in c.otherhads:
            i.jabl=c.jabl
        pr.delete(str(c)+"j","jablko")
        pr.create_rectangle(
            c.jabl[0]*c.scale+c.pos[0],
            c.jabl[1]*c.scale+c.pos[1],
            c.jabl[0]*c.scale+c.scale+c.pos[0],
            c.jabl[1]*c.scale+c.scale+c.pos[1],
            fill="red",tags=(str(c)+"j","had","jablko",str(c)))
    
    def dirch(c,dir):
        if(c.dir!=(dir+2)%4):
            c.dirr=dir
    def dirchr(c,s=0):
        if c.dir!=2:
            c.dirr=0
    def dirchd(c,s=0):
        if c.dir!=3:
            c.dirr=1
    def dirchl(c,s=0):
        if c.dir!=0:
            c.dirr=2
    def dirchu(c,s=0):
        if c.dir!=1:
            c.dirr=3
    def bardraw(c):
        pr.create_rectangle(prX/2-c.velk[0]/2*c.scale,prY/2-c.velk[1]/2*c.scale,prX/2+c.velk[0]/2*c.scale,prY/2+c.velk[1]/2*c.scale,tags=(str(c)+"b","bariéra",str(c)))

    def __init__(c,Škála:int,Veľkosť:int,Čas:int,Farba:str,Prehra,AI:bool=False,Controls:str="dsaw") -> None:
        c.x=int(Veľkosť/2)
        c.y=int(Veľkosť/2)
        c.velk=Veľkosť,Veľkosť
        c.pos=prX/2-c.velk[0]/2*Škála,prY/2-c.velk[0]/2*Škála
        c.dir=0
        c.dirr=0
        c.stipp=""
        c.farb=Farba
        c.scale=Škála
        c.bardraw()
        c.chvost=[]
        c.otherhads=[]
        c.timer=Čas
        c.maxtime=Čas
        c.isai=AI
        c.contr=Controls
        if(AI):
            c.m=astar.mriežka(c.velk[0],c.velk[1])
            c.mm=[]
        c.preh=Prehra
        c.renew=[]
        c.polickacas=0
        c.timetolick=0
        c.timelicking=0
        c.aitarget=[0,0]
        c.ježivý=True
        c.eat()

def prehra(c:Had):
    global menustate,jablká,najchvost,prejdenépol
    živ=0
    if(c!=0):
        c.stipp=gui.trasluc(8)[0]
        c.draw()
        pr.delete(str(c)+"h")
        c.ježivý=False
        for i in hady:
            if(i.ježivý):živ+=1
            if(not i.isai):
                jablká+=len(i.chvost)-1
                najchvost=max(najchvost,len(i.chvost))
                prejdenépol+=i.polickacas
    if(živ==0):
        menustate=6
        for i in dohralosa:
            i.activate()
        for i in hrasa0:
            i.deactivate()
        for i in hrasa1:
            i.deactivate()
        hrasa0[0].txt="||"


def znovu(c:Had):
    c.chvost=[]
    c.renew=[]
    c.x=int(c.velk[0]/2)
    c.y=int(c.velk[1]/2)
    c.polickacas=0
    c.ježivý=True
    c.stipp=""
    c.eat()
    pr.delete(str(c)+"h",str(c)+"ch")

def dirtran(s):
    if s==0:
        return [1,0]
    if s==1:
        return [0,1]
    if s==2:
        return [-1,0]
    if s==3:
        return [0,-1]

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
        pass

def fps(tick):
    try:
        return str(round(1/(time()-tick)))
    except:
        return str(9999)

def tobool(s):
    if s=="True":
        return True
    elif s=="False":
        return False
    else:
        return None

class hadapp(wdm.WindowedApp):
    label="Had"
    placement=10,200
    def update(c, clicking, hover, v, t):
        global hady
        super().update(clicking, hover, v, t)

        c.had.pos=c.x+c.dx/2-c.had.velk[0]/2*c.had.scale,c.y+c.dy/3*2-c.had.velk[0]/2*c.had.scale
        if c.had.timer<=0:
            pr.move(str(c.had)+"ch",-c.had.scale,0)
            c.had.timer=c.had.maxtime
        c.had.timer-=1
        c.had.draw()
        pr.tag_raise(str(c.had),"Win"+str(v))

        c.gtl1.dval=c.had.isai
        if(c.win.fadetick<0):
            if(menustate==7):
                hady.remove(c.had)
            pr.delete(str(c.had)+"h",str(c.had)+"ch",str(c.had))
        if(v.infocus):
            if(c.gtl1.stat==3):
                c.had.isai=not c.had.isai
            if(c.gtl2.stat==3):
                t=wdm.Window(hadapp)
                t.app.had=Had(scale,plátno,rýchlosť,gui.rgb([255-i for i in gui.revrgb(farba)]),prehra,True)
                t.app.hadr,t.app.hadg,t.app.hadb=[255-i for i in gui.revrgb(farba)]
                hady+=[t.app.had]
                t.app.had.chvost=[[t.app.had.x-1,t.app.had.y,0]]
                pr.delete("bariéra","jablko")

            if c.gsl1.stat==2:
                c.hadr=c.gsl1.conval
                c.gsl1.dval=str(c.gsl1.conval)
            elif c.gsl1.stat>=1:
                c.gsl1.ffl=()
                c.gsl1.ffr=()
                try:
                    c.gsl1.ffl=[(0,c.hadg,c.hadb)[i]-c.gsl1.fl[i] for i in range(3)]
                    c.gsl1.ffr=[(255,c.hadg,c.hadb)[i]-c.gsl1.fr[i] for i in range(3)]
                except: pass
                
            elif c.gsl2.stat==2:
                c.hadg=c.gsl2.conval
                c.gsl2.dval=str(c.gsl2.conval)
            elif c.gsl2.stat>=1:
                c.gsl2.ffl=()
                c.gsl2.ffr=()
                try:
                    c.gsl2.ffl=[(c.hadr,0,c.hadb)[i]-c.gsl2.fl[i] for i in range(3)]
                    c.gsl2.ffr=[(c.hadr,255,c.hadb)[i]-c.gsl2.fr[i] for i in range(3)]
                except: pass
                
            elif c.gsl3.stat==2:
                c.hadb=c.gsl3.conval
                c.gsl3.dval=str(c.gsl3.conval)
            elif c.gsl3.stat>=1:
                c.gsl3.ffl=()
                c.gsl3.ffr=()
                try:
                    c.gsl3.ffl=[(c.hadr,c.hadg,0)[i]-c.gsl3.fl[i] for i in range(3)]
                    c.gsl3.ffr=[(c.hadr,c.hadg,255)[i]-c.gsl3.fr[i] for i in range(3)]
                except: pass
        c.had.farb=gui.rgb((c.hadr,c.hadg,c.hadb))

    def draw(c):
        super().draw()
        if(c.had!=None):
            c.had.draw()

    def __init__(c, tags, window: wdm.Window) -> None:
        super().__init__(tags, window)
        dim=(-50,-10,50,10)
        c.gtl1=gui.Button(c.x+c.dx/4,c.y+30,"AI: {}",DisplayVal=False,Dimensions=dim,tags=["App"+str(c)]).activate()
        c.gtl2=gui.Button(c.x+c.dx/4*3,c.y+30,"+",Dimensions=(-20,-15,20,15),tags=["App"+str(c)]).activate()
        c.had:Had=None
        c.hadr=hadr
        c.hadg=hadg
        c.hadb=hadb
        c.gsl1=gui.Slider(prX/3*2,prY-450,"Červená: {}",Max=255,DisplayVal=str(c.hadr),IsInt=True,DefaultValue=hadr,FadeColorL=(0,hadg,hadb),FadeColorR=(255,hadg,hadb),Dimensions=dim,tags=["App"+str(c)]).activate()
        c.gsl2=gui.Slider(prX/3*2,prY-400,"Zelená: {}", Max=255,DisplayVal=str(c.hadg),IsInt=True,DefaultValue=hadg,FadeColorL=(hadr,0,hadb),FadeColorR=(hadr,255,hadb),Dimensions=dim,tags=["App"+str(c)]).activate()
        c.gsl3=gui.Slider(prX/3*2,prY-350,"Modrá: {}",  Max=255,DisplayVal=str(c.hadb),IsInt=True,DefaultValue=hadb,FadeColorL=(hadr,hadg,0),FadeColorR=(hadr,hadg,255),Dimensions=dim,tags=["App"+str(c)]).activate()
        c.gsl1.mx=c.x+c.dx/8
        c.gsl1.my=c.y+60
        c.gsl2.mx=c.x+c.dx/8*4
        c.gsl2.my=c.y+60
        c.gsl3.mx=c.x+c.dx/8*7
        c.gsl3.my=c.y+60

        c.guielements+=[c.gtl1,c.gtl2,c.gsl1,c.gsl2,c.gsl3]

#Prostredie-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
tk=Tk()
tk.title("SmajloSlovakian™")
tk.protocol("WM_DELETE_WINDOW",koniec)
pr=Canvas(tk,height=prY,width=prX,bg=prBG)
pr.grid(columnspan=200)

#Setup------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
chvostredrawop=False
chvostdir=True
portalbarr=True
scale=20
plátno=15
rýchlosť=20
farba="#0f0"
menuhady=True
fastai=False

jablká=0
najchvost=0
prejdenépol=0


if os.path.isfile("hadnastavenia.txt"):
    with open("hadnastavenia.txt",encoding="utf-8") as s:
        for i in s.readlines():
            i=i.strip().replace(" ","").split("=")
            try:
                if i[0]=="chvostredrawop":
                    chvostredrawop=tobool(i[1])
                elif i[0]=="chvostdir":
                    chvostdir=tobool(i[1])
                elif i[0]=="portalbarr":
                    portalbarr=tobool(i[1])
                elif i[0]=="scale":
                    scale=int(i[1])
                elif i[0]=="plátno":
                    plátno=int(i[1])
                elif i[0]=="rýchlosť":
                    rýchlosť=int(i[1])
                elif i[0]=="farba":
                    farba=str(i[1])
                    hadr,hadg,hadb=int(farba[1:3],16),int(farba[3:5],16),int(farba[5:7],16)
                elif i[0]=="menuhady":
                    menuhady=tobool(i[1])
            except Exception as e:
                print("Niektoré nastavenia nie sú správne!",i,e)
else:
    with open("hadnastavenia.txt","w"):
        4

if os.path.isfile("hadstats.txt"):
    with open("hadstats.txt",encoding="utf-8") as s:
        try:
            for i in s.readlines():
                i=i.strip().replace(" ","").split("=")
                if i[0]=="jablká":
                    jablká=int(i[1])
                elif i[0]=="najchvost":
                    najchvost=int(i[1])
                elif i[0]=="prejdenépol":
                    prejdenépol=int(i[1])
        except:
            print("Niektoré Štatistiky nie sú správne!")
else:
    with open("hadstats.txt","w"):
        4


menustate=0 # 0=Title, 1=Hl.menu, 2=Nastavenia, 3=Hra, 4=Pauza, 5=Štatistiky, 6=Prehra, 7=Štart

gui.setup(pr)
wdm.setup(pr,gui)
actidim=(0,2.5+10,0,10-2.5,0,10)
actidim1l=(-10, 2.5, -10, -2.5, -10, 0)
actidim1r=(10, 2.5, 10, -2.5, 10, 0)
gui.autotime=prX/2,350,1,20
hlavnémenu=[
    gui.Button(prX/2,200,"Hrať",FadeColor=(56,200,56),TTA=-1,ActiDim=actidim1r),
    gui.Button(prX/2,250,"",TTA=-1,ActiDim=actidim1l).forget(),
    gui.Button(prX/2,250,"Štatistiky",FadeColor=(200,56,56),TTA=-1,ActiDim=actidim1r),
    gui.Button(prX/2,300,"",FadeColor=(200,200,200),TTA=-1,ActiDim=actidim1l).forget(),
    gui.Button(prX/2,300,"Nastavenia",FadeColor=(128,56,128),TTA=-1,ActiDim=actidim1r),
    gui.Button(prX/2,450,"",FadeColor=(200,128,128),TTA=-1,ActiDim=actidim1l).forget(),
    gui.Button(prX/2,500,"Odísť",FadeColor=(56,200,200),TTA=-1,ActiDim=actidim)
]
štartmenu=[
    gui.Slider(prX/2,200,"{} hráčov",TTA=-1,ActiDim=actidim1r,IsInt=True,DefaultValue=0).forget(),
    gui.Slider(prX/2,250,"{} botov",TTA=-1,ActiDim=actidim1l,IsInt=True,Max=25,DefaultValue=0).forget(),
    gui.Button(150,50,"Hrať",Color=(128,200,128),FadeColor=(200,250,56),ActiDim=actidim1r)
]
gui.autotime=prX/2,prY-150,20,20
nastmenu=[
    gui.Button(prX/2,prY-200,"Späť",TTA=-1,ActiDim=actidim),
    gui.Button(prX/2,100,"",(-1,),Disabled=True,ActiDim=(0,0,0,0,0,10)),

    gui.Button(prX/3,prY-550,"Rýchle vyk. chvostov: {}",TTA=-1,ActiDim=actidim1l,DisplayVal=str(chvostredrawop)),
    gui.Button(prX/3,prY-500,"Portály: {}",TTA=-1,ActiDim=actidim1l,DisplayVal=str(portalbarr)),
    gui.Slider(prX/3,prY-450,"Veľkosť plátna: {}",TTA=-1,IsInt=True,ActiDim=actidim1l,DisplayVal=str(plátno),DefaultValue=plátno,Min=2,Max=100),
    gui.Button(prX/3,prY-400,"Hady v menu: {}",TTA=-1,ActiDim=actidim1l,DisplayVal=str(menuhady)),
    gui.Slider(prX/3*2,prY-450,"Červená: {}",Max=255,DisplayVal=str(hadr),IsInt=True,DefaultValue=hadr,TTA=-1,ActiDim=actidim1r,FadeColorL=(0,hadg,hadb),FadeColorR=(255,hadg,hadb)),
    gui.Slider(prX/3*2,prY-400,"Zelená: {}", Max=255,DisplayVal=str(hadg),IsInt=True,DefaultValue=hadg,TTA=-1,ActiDim=actidim1r,FadeColorL=(hadr,0,hadb),FadeColorR=(hadr,255,hadb)),
    gui.Slider(prX/3*2,prY-350,"Modrá: {}",  Max=255,DisplayVal=str(hadb),IsInt=True,DefaultValue=hadb,TTA=-1,ActiDim=actidim1r,FadeColorL=(hadr,hadg,0),FadeColorR=(hadr,hadg,255)),

    gui.Button(prX/3,prY-350,"Chvostový smer: {}",TTA=-1,ActiDim=actidim1l,DisplayVal=str(chvostdir)),
    gui.Slider(prX/3,prY-300,"Škála: {}",TTA=-1,IsInt=True,ActiDim=actidim1l,DisplayVal=str(scale),DefaultValue=scale,Min=1,Max=500),
    gui.Slider(prX/3,prY-250,"Rýchlosť: {}",TTA=-1,IsInt=True,ActiDim=actidim1l,DisplayVal=str(rýchlosť),DefaultValue=rýchlosť,Min=1,Max=120),
    gui.Button(prX/3*2,prY-350,"",TTA=-1,ActiDim=actidim1r,Disabled=True,Color=(-1,)),
    gui.Button(prX/3*2,prY-300,"",TTA=-1,ActiDim=actidim1r,Disabled=True,Color=(-1,)),
    gui.Button(prX/3*2,prY-250,"",TTA=-1,ActiDim=actidim1r,Disabled=True,Color=(-1,)),
    gui.Button(prX/3*2,prY-200,"",TTA=-1,ActiDim=actidim1r,Disabled=True,Color=(-1,))
]

hrasa0=[
    gui.Button(prX-50,50,"||",FadeColor=(0,255,255),Dimensions=(-20,-20,20,20),ActiDim=actidim,HoverYoff=5,HoverXoff=5)
]
hrasa1=[
    gui.Button(prX-100,150,"Pokračovať",ActiDim=actidim1r,TTA=0,FadeColor=(56,200,56)),
    gui.Button(prX-100,200,"Eat",ActiDim=actidim1r,TTA=5,Disabled=False,FadeColor=(56,56,200)),
    gui.Button(prX-100,250,"Ukončiť hru",ActiDim=actidim1r,TTA=10,FadeColor=(200,56,56)),
    gui.Button(prX-100,280,"Dĺžka chvostu: {}",ActiDim=actidim1r,TTA=15,Color=(-1,)),
    gui.Button(prX-100,295,"Počet prejdených polí: {}",ActiDim=actidim1r,TTA=17,Color=(-1,))
]
dohralosa=[
    gui.Button(prX/2,prY/2-25,"Hlavné menu",FadeColor=(56,200,56)),
    gui.Button(prX/2,prY/2+25,"Hrať znovu",FadeColor=(200,56,200))
]

statsmenu=[
    gui.Button(prX/2,prY-200,"Späť",TTA=-1,ActiDim=actidim)
]

#hadimenu=[Had(randint(5,100),randint(5,20),randint(2,30),gui.rgb((randint(0,255) for i in range(3))),znovu,True) for i in range(randint(1,2))]
hadimenu=[Had(100,20,randint(2,30),gui.rgb((randint(0,255) for i in range(3))),znovu,True)]
hady=[]
nasthad=Had(scale,plátno,rýchlosť,farba,znovu)
nasthad.chvost=[[nasthad.x-1,nasthad.y,0]]

pr.delete("bariéra")

pr.create_text(prX/2,prY/2,text="Hadík Nokia",font="Arial 50",tags="txt")
pr.create_text(prX/2,prY/2+50,text="Klikni pre pokračovanie",tags="txt")


#Loop-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
start=time()
tick=time()
tick2=1
while áno:
    #print(gui.scursor.hovering,gui.scursor.dragging)
    if menustate==0:
        if "1" in gui.spclick and not "1" in gui.sclick:
            pr.delete("txt")
            for i in hlavnémenu:
                i.activate()
            menustate=1
    elif menustate==1:
        if hlavnémenu[0].stat>=3:
            menustate=7
            pr.delete("had","bariéra")
            for i in hlavnémenu:
                i.deactivate()
            if(len(hady)==0):
                hady+=[Had(scale,plátno,rýchlosť,farba,prehra)]
                pr.delete("bariéra","jablko")
            for i in hady:
                t=wdm.Window(hadapp)
                t.app.had=i
                i.ježivý=True
                i.x=int(i.velk[0]/2)
                i.y=int(i.velk[1]/2)
                i.dir=0
                i.chvost=[[i.velk[0]/2-1,i.velk[1]/2,0]]
                t.app.gsl1.value=gui.revrgb(i.farb)[0]/255
                t.app.gsl2.value=gui.revrgb(i.farb)[1]/255
                t.app.gsl3.value=gui.revrgb(i.farb)[2]/255
                t.app.gsl1.dval=gui.revrgb(i.farb)[0]
                t.app.gsl2.dval=gui.revrgb(i.farb)[1]
                t.app.gsl3.dval=gui.revrgb(i.farb)[2]
            for i in štartmenu:
                i.activate()
        if hlavnémenu[2].stat>=3:
            menustate=5
            for i in hlavnémenu:
                i.deactivate()
            for i in statsmenu:
                i.activate()
        if hlavnémenu[4].stat==3:
            menustate=2
            for i in hlavnémenu:
                i.deactivate()
            for i in nastmenu:
                i.activate()
        if(hlavnémenu[6].stat==3):
            koniec()
    elif menustate==7:
        if štartmenu[0].stat==2:
            štartmenu[0].dval=štartmenu[0].conval
        elif štartmenu[1].stat==2:
            štartmenu[1].dval=štartmenu[1].conval
        elif štartmenu[2].stat==3:
            pr.delete("had","bariéra")
            #hady=[Had(scale,plátno,rýchlosť,farba,prehra) for i in range(štartmenu[0].conval)]+[Had(scale,plátno,rýchlosť,farba,prehra,True) for i in range(štartmenu[1].conval)]
            hady=[Had(scale,plátno,rýchlosť,i.app.had.farb,prehra,i.app.had.isai) for i in wdm.Window._reg]
            for i in hady:
                i.dir=randint(0,3)
                i.dirr=i.dir
                for o in hady:
                    if(not(i is o)):
                        o.otherhads+=[i]
            for i in štartmenu:
                i.deactivate()
            for i in wdm.Window._reg:
                i.fading=-1
            for i in hrasa0:
                i.activate()
            menustate=3
        if(len(wdm.Window._reg)==0):
            for i in štartmenu:
                i.deactivate()
            for i in hlavnémenu:
                i.activate()
            menustate=1
    elif menustate==2:
        if nastmenu[2].stat==3:
            pr.delete("had")
            chvostredrawop=not chvostredrawop
            nastmenu[2].dval=str(chvostredrawop)
        elif nastmenu[2].stat>=1:
            nastmenu[1].activate()
            nastmenu[1].txt="Toto by malo prilepšiť hre na stránke výkonu tým,\nže nebude vykresľovať už vykreslené bloky chvostu.\nToto nastavenie môže spôsobiť blikanie a zaostávanie niektorých blokov kvôli neprepracovanosti!\nPo aplikovaní sa na existujúcich hadoch objavia chvíľkové diery."
        
        elif nastmenu[9].stat==3:
            chvostdir=not chvostdir
            nastmenu[9].dval=str(chvostdir)
        elif nastmenu[9].stat>=1:
            nastmenu[1].activate()
            nastmenu[1].txt="Zrýchli výkon vypnutím efektu smeru plazenia chvostov."

        elif nastmenu[3].stat==3:
            portalbarr=not portalbarr
            nastmenu[3].dval=str(portalbarr)
        elif nastmenu[3].stat>=1:
            nastmenu[1].activate()
            nastmenu[1].txt="Pri chode do bariéry namiesto prehry teleportuj hráča cez pole."

        elif nastmenu[4].stat==2:
            plátno=nastmenu[4].conval
            nastmenu[4].dval=str(plátno)
            nasthad.chvost=[[nasthad.x-1,nasthad.y,0]]
            nasthad.x=int(nasthad.velk[0]/2)
            nasthad.y=int(nasthad.velk[1]/2)
        elif nastmenu[4].stat>=1:
            nastmenu[1].activate()
            nastmenu[1].txt="Je to priemer plochy hry. Počíta sa v blokoch."
            
        elif nastmenu[10].stat==2:
            scale=nastmenu[10].conval
            nastmenu[10].dval=str(scale)
            nasthad.chvost=[[nasthad.x-1,nasthad.y,0]]
            nasthad.x=int(nasthad.velk[0]/2)
            nasthad.y=int(nasthad.velk[1]/2)
        elif nastmenu[10].stat>=1:
            nastmenu[1].activate()
            nastmenu[1].txt="Je to priemer blokov. Počíta sa v pixeloch."
            
        elif nastmenu[11].stat==2:
            rýchlosť=nastmenu[11].conval
            nastmenu[11].dval=str(rýchlosť)
        elif nastmenu[11].stat>=1:
            nastmenu[1].activate()
            nastmenu[1].txt="Počíta sa v snímkach. Každých x snímok sa had pohne."
        
        elif nastmenu[5].stat==3:
            menuhady=not menuhady
            nastmenu[5].dval=str(menuhady)
        elif nastmenu[5].stat>=1:
            nastmenu[1].activate()
            nastmenu[1].txt="Zrýchli výkon vypnutím pozadia v menu - vypnutím botov v menu."

        elif nastmenu[6].stat==2:
            hadr=nastmenu[6].conval
            nastmenu[6].dval=str(nastmenu[6].conval)
        elif nastmenu[6].stat>=1:
            nastmenu[6].ffl=()
            nastmenu[6].ffr=()
            try:
                nastmenu[6].ffl=[(0,hadg,hadb)[i]-nastmenu[6].fl[i] for i in range(3)]
                nastmenu[6].ffr=[(255,hadg,hadb)[i]-nastmenu[6].fr[i] for i in range(3)]
            except: pass
            nastmenu[1].activate()
            nastmenu[1].txt="Predvolená farba hada."
            
        elif nastmenu[7].stat==2:
            hadg=nastmenu[7].conval
            nastmenu[7].dval=str(nastmenu[7].conval)
        elif nastmenu[7].stat>=1:
            nastmenu[7].ffl=()
            nastmenu[7].ffr=()
            try:
                nastmenu[7].ffl=[(hadr,0,hadb)[i]-nastmenu[7].fl[i] for i in range(3)]
                nastmenu[7].ffr=[(hadr,255,hadb)[i]-nastmenu[7].fr[i] for i in range(3)]
            except: pass
            nastmenu[1].activate()
            nastmenu[1].txt="Predvolená farba hada."
            
        elif nastmenu[8].stat==2:
            hadb=nastmenu[8].conval
            nastmenu[8].dval=str(nastmenu[8].conval)
        elif nastmenu[8].stat>=1:
            nastmenu[8].ffl=()
            nastmenu[8].ffr=()
            try:
                nastmenu[8].ffl=[(hadr,hadg,0)[i]-nastmenu[8].fl[i] for i in range(3)]
                nastmenu[8].ffr=[(hadr,hadg,255)[i]-nastmenu[8].fr[i] for i in range(3)]
            except: pass
            nastmenu[1].activate()
            nastmenu[1].txt="Predvolená farba hada."
            
        else:
            nastmenu[1].deactivate()
        
        nasthad.maxtime,nasthad.scale,nasthad.farb,nasthad.velk = rýchlosť,scale,gui.rgb((hadr,hadg,hadb)),(plátno,plátno)
        nasthad.pos=prX/2-nasthad.velk[0]/2*nasthad.scale,prY/2-nasthad.velk[0]/2*nasthad.scale
        farba=nasthad.farb
        if nasthad.timer<=0:
            pr.move(str(nasthad)+"ch",-nasthad.scale,0)
            nasthad.timer=nasthad.maxtime
        nasthad.timer-=1
        nasthad.draw()
        pr.tag_lower(pr.create_rectangle(prX/2-nasthad.velk[0]/2*nasthad.scale,prY/2-nasthad.velk[1]/2*nasthad.scale,prX/2+nasthad.velk[0]/2*nasthad.scale,prY/2+nasthad.velk[1]/2*nasthad.scale,tags=("refresh")),"stkgui")
        pr.tag_lower("had","stkgui")

        if nastmenu[0].stat==3:
            menustate=1
            pr.delete(str(nasthad)+"h",str(nasthad)+"ch")
            for i in hlavnémenu:
                i.activate()
            for i in nastmenu:
                i.deactivate()
    elif menustate==3:
        if hrasa0[0].stat==3 or gui.transpress("p;"):
            menustate=4
            hrasa0[0].txt="|>"
            hrasa0[0].draw()
            #hrasa1[3].dval=len(had.chvost)
            #hrasa1[4].dval=had.polickacas
            for i in hrasa1:
                i.activate()
        
        for i in hady:
            if i.timer<=0:
                i.step()
                i.timer=i.maxtime
            i.timer-=1
            i.draw()
            for o in range(len(i.contr)):
                if(i.contr[o] in gui.spress):
                    i.dirch(o)
    elif menustate==4:
        #pr.create_text(prX/2,prY/2+100,text="Dĺžka chvostu: "+str(len(had.chvost))+"\nPočet prejdených polí: "+str(had.polickacas),tag="refresh")
        if hrasa1[0].stat==3 or hrasa0[0].stat==3 or gui.transpress("p;"):
            menustate=3
            for i in hrasa1:
                i.deactivate()
            hrasa0[0].txt="||"
            hrasa0[0].draw()
        if hrasa1[1].stat==3:
            for i in hady:
                i.eat()
        if hrasa1[2].stat==3:
            prehra(0)
    elif menustate==5:
        pr.create_text(prX/2,90,
        text="""Celkovo pozbieraných jabĺk: {}
        Najväčší chvost za hru: {}
        Celková prejdená dĺžka: {}""".format(jablká,najchvost,prejdenépol),font="Arial 20",tags="refresh")
        if statsmenu[0].stat==3:
            menustate=1
            for i in statsmenu: i.deactivate()
            for i in hlavnémenu: i.activate()
    elif menustate==6:
        pr.create_text(prX/2,50,text="Prehral si!",font="Arial 25",tags="refresh")
        '''pr.create_text(prX/2,80,text="Dĺžka chvostu: "+str(len(had.chvost)),tags="refresh")
        pr.create_text(prX/2,100,text="Počet prejdených polí: "+str(had.polickacas),tags="refresh")
        if had.isai:
            pr.create_text(prX/2,120,text="Hral to bot, štatistiky nebudú uložené.",tags="refresh")'''
        if dohralosa[0].stat==3 or gui.transpress("p;"):
            menustate=1
            for i in dohralosa: i.deactivate()
            for i in hlavnémenu: i.activate()
        if dohralosa[1].stat==3 or gui.transpress("p "):
            menustate=3
            for i in hady:
                znovu(i)
            for i in dohralosa: i.deactivate()
            for i in hrasa0: i.activate()

    
    if menuhady:
        if menustate==0 or menustate==1 or menustate==5:
            for i in hadimenu:
                if i.timer<=0:
                    i.step()
                    i.timer=i.maxtime
                else:
                    i.timer-=1
                i.draw()
    gui.updatelem(tick2)
    wdm.Window.updall(tick2)
    gui.updatetools()
    tk.update() #simple 120hz lock VV
    psleep(nonneg(minms-(time()-tick)))
    #print(fps(tick),"     ",end="\r")
    tick2=time()-tick
    tick=time()
    pr.delete("refresh")

#Koniec-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("\nprogram končí                                                            ")
tk.update()
o=0
e=0
p=[]
for i in fpská:
    i:str
    if i.isnumeric():
        p.append(i)
        o+=int(i)
        e+=1

with open("hadnastavenia.txt","w",encoding="utf-8") as s:
    s.writelines([
        "\nchvostredrawop="+str(chvostredrawop),
        "\nchvostdir="+str(chvostdir),
        "\nportalbarr="+str(portalbarr),
        "\nscale="+str(scale),
        "\nplátno="+str(plátno),
        "\nrýchlosť="+str(rýchlosť),
        "\nfarba="+str(farba),
        "\nmenuhady="+str(menuhady)
        ])

with open("hadstats.txt","w",encoding="utf-8") as s:
    s.writelines([
        "\njablká="+str(jablká),
        "\nnajchvost="+str(najchvost),
        "\nprejdenépol="+str(prejdenépol)
        ])
