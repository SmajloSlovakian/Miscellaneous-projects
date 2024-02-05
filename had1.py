#Nastavenia-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import os
from time import *
from math import *
from tkinter import *
from tkinter import messagebox as mbox
from random import *
import winsound as ws
import smajlotkgui04 as gui
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
MEDIA="C:\\Windows\\Media\\"
timeout=-3   #sec
áno=True
prY=800
prX=1200
prBG="#fff"
tick=0
minms=0#1/120 #fps
fpská=[]
hadr=0
hadg=255
hadb=0


#had=Had(20,10,20,"#0d0",prehra)


#Definície--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Had:
    def draw(c):
        if c.timetolick<=0:
            c.timelicking-=1
            if c.timelicking<0:
                c.timelicking=30
                c.timetolick=randint(0,120*5)
        else:
            c.timetolick-=1
        pr.delete(str(c)+"h")
        if chvostredrawop:
            if len(c.chvost)>len(c.renew) or c.timer==c.maxtime:
                c.renew.append(
                    pr.create_rectangle(
                        c.x+c.chvost[-1][0]*c.velk-c.velk/2,
                        c.y+c.chvost[-1][1]*c.velk-c.velk/2,
                        c.x+c.chvost[-1][0]*c.velk+c.velk/2,
                        c.y+c.chvost[-1][1]*c.velk+c.velk/2,
                        fill=c.farb,tags=(str(c)+"ch","had"),width=1))
            elif len(c.renew)>len(c.chvost):
                pr.delete(c.renew[0])
                del c.renew[0]
        elif not chvostredrawop:
            pr.delete(str(c)+"ch")
        for x,y,z in c.chvost:
            x*=c.velk
            y*=c.velk
            if not chvostredrawop:
                try:
                    pr.create_rectangle(
                        c.x+x-c.velk/2,
                        c.y+y-c.velk/2,
                        c.x+x+c.velk/2,
                        c.y+y+c.velk/2,
                        fill=c.farb,tags=(str(c)+"ch","had"),width=1)
                except:
                    pass
            if chvostdir:
                a=((c.maxtime-c.timer)/c.maxtime)
                if z==0:
                    pr.create_line( c.x+x-c.velk/2+c.velk*a, c.y+y-c.velk/2,
                                    c.x+x-c.velk/2+c.velk*a, c.y+y+c.velk/2,
                                    tags=(str(c)+"h","had"),width=3)
                elif z==1:
                    pr.create_line(c.x+x-c.velk/2, c.y+y-c.velk/2+c.velk*a,
                                        c.x+x+c.velk/2, c.y+y-c.velk/2+c.velk*a,
                                        tags=(str(c)+"h","had"),width=3)
                elif z==2:
                    pr.create_line(c.x+x+c.velk/2-c.velk*a, c.y+y+c.velk/2,
                                        c.x+x+c.velk/2-c.velk*a, c.y+y-c.velk/2,
                                        tags=(str(c)+"h","had"),width=3)
                elif z==3:
                    pr.create_line(c.x+x+c.velk/2, c.y+y+c.velk/2-c.velk*a,
                                        c.x+x-c.velk/2, c.y+y+c.velk/2-c.velk*a,
                                        tags=(str(c)+"h","had"),width=3)
        pr.create_rectangle(
            c.x-c.velk/2,
            c.y-c.velk/2,
            c.x+c.velk/2,
            c.y+c.velk/2,
            fill=c.farb,tags=(str(c)+"h","had"))
        if c.timetolick<=0:
            t=15-abs(c.timelicking-15)
            if c.dir==0:
                pr.create_rectangle(
                    c.x+c.velk/2,c.y-c.velk/4,
                    c.x+c.velk/2+t/15*c.velk*2,c.y+c.velk/4, fill="red",tags=(str(c)+"h","had")
                    )
            elif c.dir==1:
                pr.create_rectangle(
                    c.x-c.velk/4,c.y+c.velk/2,
                    c.x+c.velk/4,c.y+c.velk/2+t/15*c.velk*2, fill="red",tags=(str(c)+"h","had")
                    )
            elif c.dir==2:
                pr.create_rectangle(
                    c.x-c.velk/2,c.y-c.velk/4,
                    c.x-c.velk/2-t/15*c.velk*2,c.y+c.velk/4, fill="red",tags=(str(c)+"h","had")
                    )
            elif c.dir==3:
                pr.create_rectangle(
                    c.x-c.velk/4,c.y-c.velk/2,
                    c.x+c.velk/4,c.y-c.velk/2-t/15*c.velk*2, fill="red",tags=(str(c)+"h","had")
                    )
        dt=dirtran(c.dir)
        pr.create_rectangle(
            c.x+dt[0]*c.velk/2-c.velk/5*dt[0]-c.velk/4*(1-abs(dt[0])),
            c.y+dt[1]*c.velk/2-c.velk/5*dt[1]-c.velk/4*(1-abs(dt[1])),
            c.x+dt[0]*c.velk/2-c.velk/5*dt[0]-c.velk/4*(1-abs(dt[0])),
            c.y+dt[1]*c.velk/2-c.velk/5*dt[1]-c.velk/4*(1-abs(dt[1])), outline="white",width=4*c.velk/20,tags=(str(c)+"h","had")
            )
        pr.create_rectangle(
            c.x+dt[0]*c.velk/2-c.velk/5*dt[0]+c.velk/4*(1-abs(dt[0])),
            c.y+dt[1]*c.velk/2-c.velk/5*dt[1]+c.velk/4*(1-abs(dt[1])),
            c.x+dt[0]*c.velk/2-c.velk/5*dt[0]+c.velk/4*(1-abs(dt[0])),
            c.y+dt[1]*c.velk/2-c.velk/5*dt[1]+c.velk/4*(1-abs(dt[1])), outline="white",width=4*c.velk/20,tags=(str(c)+"h","had")
            )
        pr.create_rectangle(
            c.x+dt[0]*c.velk/2-c.velk/10*dt[0]-c.velk/4*(1-abs(dt[0])),
            c.y+dt[1]*c.velk/2-c.velk/10*dt[1]-c.velk/4*(1-abs(dt[1])),
            c.x+dt[0]*c.velk/2-c.velk/10*dt[0]-c.velk/4*(1-abs(dt[0])),
            c.y+dt[1]*c.velk/2-c.velk/10*dt[1]-c.velk/4*(1-abs(dt[1])), width=4*c.velk/20,tags=(str(c)+"h","had")
            )
        pr.create_rectangle(
            c.x+dt[0]*c.velk/2-c.velk/10*dt[0]+c.velk/4*(1-abs(dt[0])),
            c.y+dt[1]*c.velk/2-c.velk/10*dt[1]+c.velk/4*(1-abs(dt[1])),
            c.x+dt[0]*c.velk/2-c.velk/10*dt[0]+c.velk/4*(1-abs(dt[0])),
            c.y+dt[1]*c.velk/2-c.velk/10*dt[1]+c.velk/4*(1-abs(dt[1])) ,width=4*c.velk/20,tags=(str(c)+"h","had")
            )

    def update(c):
        if c.isai:
            aidir=True
            aiupdir=[]
            aidr=False
            aidd=False
            aidl=False
            aidu=False

            if c.jabl[0]>0:
                aidr=True
                aiupdir.append(0)
            if c.jabl[1]>0:
                aidd=True
                aiupdir.append(1)
            if c.jabl[0]<0:
                aidl=True
                aiupdir.append(2)
            if c.jabl[1]<0:
                aidu=True
                aiupdir.append(3)

            if c.dir==0 and aidr:
                aidir=False
            elif c.dir==1 and aidd:
                aidir=False
            elif c.dir==2 and aidl:
                aidir=False
            elif c.dir==3 and aidu:
                aidir=False

            if aidir and len(aiupdir)>0:
                aiupdir1=choice(aiupdir)
                if aiupdir1==0:
                    c.dirchr()
                elif aiupdir1==1:
                    c.dirchd()
                elif aiupdir1==2:
                    c.dirchl()
                elif aiupdir1==3:
                    c.dirchu()
        
            for x,y,z in c.chvost:
                if x==dirtran(c.dirr)[0]:
                    if y==dirtran(c.dirr)[1]:
                        if c.dirr==0:
                            c.dirchl()
                        elif c.dirr==1:
                            c.dirchu()
                        elif c.dirr==2:
                            c.dirchr()
                        elif c.dirr==3:
                            c.dirchd()
            
        c.dir=c.dirr
        for i in range(len(c.chvost)):
            c.chvost[i][0]-=dirtran(c.dir)[0]
            c.chvost[i][1]-=dirtran(c.dir)[1]
        c.polickacas+=1
        c.jabl[0]-=dirtran(c.dir)[0]*c.velk
        c.jabl[1]-=dirtran(c.dir)[1]*c.velk
        c.chvost.append([-i for i in dirtran(c.dir)]+[c.dir])
        del c.chvost[0]
        c.x+=dirtran(c.dir)[0]*c.velk
        c.y+=dirtran(c.dir)[1]*c.velk
        if len(c.chvost)>1:
            for i in range(len(c.chvost)-1):
                if c.chvost[i][0]==0:
                    if c.chvost[i][1]==0:
                        c.preh(c)
                        break
        if c.jabl[0]==0:
            if c.jabl[1]==0:
                c.eat()
        
        bar=c.barrierc(c.x,c.y)
        if bar[0]:
            if portalbarr:
                c.x+=c.barier*2*bar[1]
                c.y+=c.barier*2*bar[2]
                for i in c.chvost:
                    i[0]-=c.barier/c.velk*2*bar[1]
                    i[1]-=c.barier/c.velk*2*bar[2]
                c.jabl[0]-=c.barier*2*bar[1]
                c.jabl[1]-=c.barier*2*bar[2]
            else:
                c.preh(c)
    
    def barrierc(c,x,y):
        ano=False
        dirx=0
        diry=0
        if x>=prX/2+c.barier:
            ano=True
            dirx=-1
        elif x<=prX/2-c.barier:
            ano=True
            dirx=1
        if y>=prY/2+c.barier:
            ano=True
            diry=-1
        elif y<=prY/2-c.barier:
            ano=True
            diry=1
        return ano,dirx,diry

    def eat(c):
        c.chvost.append([0,0,c.dir])
        if chvostredrawop:
            try:
                if len(c.chvost)>len(c.renew) or c.timer==c.maxtime:
                    c.renew.append(
                        pr.create_rectangle(
                            c.x+c.chvost[-2][0]*c.velk-c.velk/2,
                            c.y+c.chvost[-2][1]*c.velk-c.velk/2,
                            c.x+c.chvost[-2][0]*c.velk+c.velk/2,
                            c.y+c.chvost[-2][1]*c.velk+c.velk/2,
                            fill=c.farb,tags=(str(c)+"ch","had"),width=1))
            except:4
        niesom=True
        maxim=100
        while niesom and maxim>0:
            maxim-=1
            c.jabl=[randrange(int(prX/2-c.barier+c.velk),int(prX/2+c.barier),c.velk)-c.x,randrange(int(prY/2-c.barier+c.velk),int(prY/2+c.barier),c.velk)-c.y]
            if c.jabl[0]!=0 and c.jabl[1]!=0:
                niesom=False
                for x,y,z in c.chvost:
                    if c.jabl[0]==x and c.jabl[1]==y:
                        niesom=True
                        break
        pr.delete(str(c)+"j")
        pr.create_rectangle(
            c.x+c.jabl[0]-c.velk/2,
            c.y+c.jabl[1]-c.velk/2,
            c.x+c.jabl[0]+c.velk/2,
            c.y+c.jabl[1]+c.velk/2,
            fill="red",tags=(str(c)+"j","had"))
    
    def dirchr(c,s=0):
        if c.dir!=2:
            c.dirr=0
        elif c.isai:
            c.dirr=choice((1,3))
            while c.barrierc(c.x+dirtran(c.dirr)[0],c.y+dirtran(c.dirr)[1])[0] and not portalbarr:
                c.dirr=choice((1,3))
    def dirchd(c,s=0):
        if c.dir!=3:
            c.dirr=1
        elif c.isai:
            c.dirr=choice((2,0))
            while c.barrierc(c.x+dirtran(c.dirr)[0],c.y+dirtran(c.dirr)[1])[0] and not portalbarr:
                c.dirr=choice((2,0))
    def dirchl(c,s=0):
        if c.dir!=0:
            c.dirr=2
        elif c.isai:
            c.dirr=choice((1,3))
            while c.barrierc(c.x+dirtran(c.dirr)[0],c.y+dirtran(c.dirr)[1])[0] and not portalbarr:
                c.dirr=choice((1,3))
    def dirchu(c,s=0):
        if c.dir!=1:
            c.dirr=3
        elif c.isai:
            c.dirr=choice((2,0))
            while c.barrierc(c.x+dirtran(c.dirr)[0],c.y+dirtran(c.dirr)[1])[0] and not portalbarr:
                c.dirr=choice((2,0))

    def __init__(c,Škála:int,Veľkosť:int,Čas:int,Farba:str,Prehra,AI:bool=False) -> None:
        c.x=prX/2
        c.y=prY/2
        c.dir=0
        c.dirr=0
        c.farb=Farba
        c.velk=Škála
        c.barier=Veľkosť*c.velk
        pr.create_rectangle(prX/2-c.barier,prY/2-c.barier,prX/2+c.barier,prY/2+c.barier,tags=(str(c)+"b","bariéra"))
        c.chvost=[]
        c.timer=Čas
        c.maxtime=Čas
        c.isai=AI
        c.preh=Prehra
        c.renew=[]
        c.polickacas=0
        c.timetolick=0
        c.timelicking=0
        c.eat()

def prehra(c):
    global menustate,jablká,najchvost,prejdenépol
    menustate=6
    for i in dohralosa:
        i.activate()
    for i in hrasa0:
        i.deactivate()
    for i in hrasa1:
        i.deactivate()
    hrasa0[0].txt="||"
    if not had.isai:
        jablká+=len(had.chvost)-1
        najchvost=max(najchvost,len(had.chvost))
        prejdenépol+=had.polickacas

def znovu(c:Had):
    c.chvost=[]
    c.renew=[]
    c.x=prX/2
    c.y=prY/2
    c.polickacas=0
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
        0

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


menustate=0 # 0=Title, 1=Hl.menu, 2=Nastavenia, 3=Hra, 4=Pauza, 5=Štatistiky, 6=Prehra

gui.setup(pr)
actidim=(0,2.5+10,0,10-2.5,0,10)
actidim1l=(-10, 2.5, -10, -2.5, -10, 0)
actidim1r=(10, 2.5, 10, -2.5, 10, 0)
gui.autotime=prX/2,350,1,20
hlavnémenu=[
    gui.Button(prX/2,200,"Štart",FadeColor=(56,200,56),TTA=-1,ActiDim=actidim1r),
    gui.Button(prX/2,250,"Bot",TTA=-1,ActiDim=actidim1l),
    gui.Button(prX/2,300,"Štatistiky",FadeColor=(200,56,56),TTA=-1,ActiDim=actidim1r),
    gui.Button(prX/2,350,"Nič",FadeColor=(200,200,200),TTA=-1,ActiDim=actidim1l,Disabled=True),
    gui.Button(prX/2,400,"Nastavenia",FadeColor=(128,56,128),TTA=-1,ActiDim=actidim1r),
    gui.Button(prX/2,450,"Nič",FadeColor=(200,128,128),TTA=-1,ActiDim=actidim1l,Disabled=True),
    gui.Button(prX/2,500,"Nič",FadeColor=(56,200,200),TTA=-1,ActiDim=actidim1r,Disabled=True)
]
gui.autotime=prX/2,prY-150,20,20
nastmenu=[
    gui.Button(prX/2,prY-200,"Späť",TTA=-1,ActiDim=actidim),
    gui.Button(prX/2,100,"",(-1,),Disabled=True,ActiDim=(0,0,0,0,0,10)),

    gui.Button(prX/3,prY-550,"Rýchle vyk. chvostov: {}",TTA=-1,ActiDim=actidim1l,DisplayVal=str(chvostredrawop)),
    gui.Button(prX/3,prY-500,"Portály: {}",TTA=-1,ActiDim=actidim1l,DisplayVal=str(portalbarr)),
    gui.Slider(prX/3,prY-450,"Veľkosť plátna: {}",TTA=-1,ActiDim=actidim1l,DisplayVal=str(plátno),DefaultValue=(plátno-2)/28),
    gui.Button(prX/3,prY-400,"Hady v menu: {}",TTA=-1,ActiDim=actidim1l,DisplayVal=str(menuhady)),
    gui.Slider(prX/3*2,prY-450,"Červená: {}",Max=255,DisplayVal=str(hadr),IsInt=True,DefaultValue=hadr,TTA=-1,ActiDim=actidim1r,FadeColorL=(0,hadg,hadb),FadeColorR=(255,hadg,hadb)),
    gui.Slider(prX/3*2,prY-400,"Zelená: {}", Max=255,DisplayVal=str(hadg),IsInt=True,DefaultValue=hadg,TTA=-1,ActiDim=actidim1r,FadeColorL=(hadr,0,hadb),FadeColorR=(hadr,255,hadb)),
    gui.Slider(prX/3*2,prY-350,"Modrá: {}",  Max=255,DisplayVal=str(hadb),IsInt=True,DefaultValue=hadb,TTA=-1,ActiDim=actidim1r,FadeColorL=(hadr,hadg,0),FadeColorR=(hadr,hadg,255)),

    gui.Button(prX/3,prY-350,"Chvostový smer: {}",TTA=-1,ActiDim=actidim1l,DisplayVal=str(chvostdir)),
    gui.Slider(prX/3,prY-300,"Škála: {}",TTA=-1,ActiDim=actidim1l,DisplayVal=str(scale),DefaultValue=(scale-3)/37),
    gui.Slider(prX/3,prY-250,"Rýchlosť: {}",TTA=-1,ActiDim=actidim1l,DisplayVal=str(rýchlosť),DefaultValue=(rýchlosť-1)/39),
    gui.Button(prX/3*2,prY-350,"",TTA=-1,ActiDim=actidim1r,Disabled=True,Color=(-1,)),
    gui.Button(prX/3*2,prY-300,"",TTA=-1,ActiDim=actidim1r,Disabled=True,Color=(-1,)),
    gui.Button(prX/3*2,prY-250,"",TTA=-1,ActiDim=actidim1r,Disabled=True,Color=(-1,)),
    gui.Button(prX/3*2,prY-200,"",TTA=-1,ActiDim=actidim1r,Disabled=True,Color=(-1,))
]

hrasa0=[
    gui.Button(prX-50,50,"||",FadeColor=(0,255,255),Dimensions=(-20,-20,20,20),ActiDim=actidim,HoverYoff=5,HoverXoff=5)
]
hrasa1=[
    gui.Button(prX/2,prY/2-100,"Pokračovať",ActiDim=actidim,TTA=0),
    gui.Button(prX/2,prY/2-50,"Eat",ActiDim=actidim,TTA=10,Disabled=True),
    gui.Button(prX/2,prY/2,"Ukončiť hru",ActiDim=actidim,TTA=20)
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
nasthad=Had(scale,plátno,rýchlosť,farba,znovu)
nasthad.x=prX/2
nasthad.y=prY/2
nasthad.chvost=[[-1,0,0]]
pr.delete("bariéra")

pr.create_text(prX/2,prY/2,text="Hadík Nokia",font="Arial 50",tags="txt")
pr.create_text(prX/2,prY/2+50,text="Klikni pre pokračovanie",tags="txt")


#Loop-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
start=time()
tick=time()
tick2=1
while áno:
    if menustate==0:
        if gui.sclick:
            pr.delete("txt")
            for i in hlavnémenu:
                i.activate()
            menustate=1
    elif menustate==1:
        if hlavnémenu[0].stat>=3:
            menustate=3
            pr.delete("had","bariéra")
            had=Had(scale,plátno,rýchlosť,farba,prehra)
            pr.bind_all("<d>",had.dirchr)
            pr.bind_all("<s>",had.dirchd)
            pr.bind_all("<a>",had.dirchl)
            pr.bind_all("<w>",had.dirchu)
            for i in hlavnémenu:
                i.deactivate()
            for i in hrasa0:
                i.activate()
        if hlavnémenu[1].stat>=3:
            menustate=3
            pr.delete("had","bariéra")
            had=Had(scale,plátno,rýchlosť,farba,prehra,True)
            for i in hlavnémenu:
                i.deactivate()
            for i in hrasa0:
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
            nastmenu[4].value=round(nastmenu[4].value*28)/28
            plátno=round(nastmenu[4].value*28+2)
            nastmenu[4].dval=str(plátno)
        elif nastmenu[4].stat>=1:
            nastmenu[1].activate()
            nastmenu[1].txt="Počíta sa po blokoch. Je to polomer plochy hry."
            
        elif nastmenu[10].stat==2:
            nastmenu[10].value=round(nastmenu[10].value*37)/37
            scale=round(nastmenu[10].value*37+3)
            nastmenu[10].dval=str(scale)
        elif nastmenu[10].stat>=1:
            nastmenu[1].activate()
            nastmenu[1].txt="Mal by to byť priemer blokov. Počíta sa v pixeloch."
            
        elif nastmenu[11].stat==2:
            nastmenu[11].value=round(nastmenu[11].value*39)/39
            rýchlosť=round(nastmenu[11].value*39+1)
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
            nastmenu[1].txt="Prefarbí hada."
            
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
            nastmenu[1].txt="Prefarbí hada."
            
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
            nastmenu[1].txt="Prefarbí hada."
            
        else:
            nastmenu[1].deactivate()
        
        nasthad.barier,nasthad.maxtime,nasthad.velk,nasthad.farb = nasthad.velk*plátno,rýchlosť,scale,gui.rgb((hadr,hadg,hadb))
        farba=nasthad.farb
        if nasthad.timer<=0:
            nasthad.timer=nasthad.maxtime
        else:
            nasthad.timer-=1
        nasthad.draw()
        pr.create_rectangle(prX/2-nasthad.barier,prY/2-nasthad.barier,prX/2+nasthad.barier,prY/2+nasthad.barier,tags=("refresh"))


        if nastmenu[0].stat==3:
            menustate=1
            pr.delete(str(nasthad)+"h",str(nasthad)+"ch")
            for i in hlavnémenu:
                i.activate()
            for i in nastmenu:
                i.deactivate()
    elif menustate==3:
        if hrasa0[0].stat==3:
            menustate=4
            hrasa0[0].txt="|>"
            hrasa0[0].draw()
            for i in hrasa1:
                i.activate()
        
        if had.timer<=0:
            had.update()
            had.timer=had.maxtime
        else:
            had.timer-=1
        had.draw()
    elif menustate==4:
        pr.create_text(prX/2,prY/2+100,text="Dĺžka chvostu: "+str(len(had.chvost))+"\nPočet prejdených polí: "+str(had.polickacas),tag="refresh")
        if hrasa1[0].stat==3 or hrasa0[0].stat==3:
            menustate=3
            for i in hrasa1:
                i.deactivate()
            hrasa0[0].txt="||"
            hrasa0[0].draw()
        if hrasa1[1].stat==3:
            had.eat()
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
        pr.create_text(prX/2,80,text="Dĺžka chvostu: "+str(len(had.chvost)),tags="refresh")
        pr.create_text(prX/2,100,text="Počet prejdených polí: "+str(had.polickacas),tags="refresh")
        if had.isai:
            pr.create_text(prX/2,120,text="Hral to bot, štatistiky nebudú uložené.",tags="refresh")
        if dohralosa[0].stat==3:
            menustate=1
            for i in dohralosa: i.deactivate()
            for i in hlavnémenu: i.activate()
        if dohralosa[1].stat==3:
            menustate=3
            znovu(had)
            for i in dohralosa: i.deactivate()
            for i in hrasa0: i.activate()

    
    if menuhady:
        if menustate==0 or menustate==1 or menustate==5:
            for i in hadimenu:
                if i.timer<=0:
                    i.update()
                    i.timer=i.maxtime
                else:
                    i.timer-=1
                i.draw()
    if tick-start>=timeout>=0:
        áno=False
    gui.updatelem(tick2)
    gui.updatetools()
    tk.update() #simple 120hz lock VV
    psleep(nonneg(minms-(time()-tick)))
    print(fps(tick),"     ",end="\r")
    tick2=time()-tick
    tick=time()
    pr.delete("refresh")

#Koniec-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("\nprogram končí                                                            ")
ws.PlaySound(MEDIA+"tada.wav",0)
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

