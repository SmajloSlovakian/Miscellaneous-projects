#Nastavenia
from random import *
from math import *
from tkinter import *
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    print("DPI nastavenia neboli použité.")
vykreslit=1             #fps/vykreslit je počet snímok vykreslených za sekundu (musí byť celé číslo)
fps=120                 #hodnoty väčšie znesenia spomalia hru! môže tiež spôsobiiť zmeny v animáciách
absorbcia=[2,2]         #menovateľ sily pri stene
so=60                   #sila ovládania
r=[30,45]               #polomer lopiet
g=[20,20]               #sila gravitácie lopiet
trenie=[0.6,0.6]        #čím väčšie tým menej sily sa bude uberať každú snímku
treniel=[50,50]         #percento zachovalej sily pri rovnobežnom dotyku
lopty=2                 #počet lopiet, musí sedieť
line=1                  #viditeľnosť čiary od lopty ku kurzoru
lowpower=0              #každá lopta je vypočítaná v inú snímku
zrychlovanie=0          #toto mení fyziku pri lowpower! zväčší množstvo sily pri viacerých loptách
deform=0.6              #deliteľ polomeru pri silnej zrážke
prekazkaXa=[245,258,272,295,343,360,394,433,468,502,541,599,655,679,698,720,744,767,778,577,629,827,96,228,228,228,188,228,181,228,228,228,228,228,201,222,196,827,827,827,67,644,569,221,75,75,657]
prekazkaYa=[467,462,455,448,437,433,428,417,407,390,373,352,333,324,313,302,290,286,282,364,340,70,59,478,478,478,484,478,480,478,478,478,478,478,490,489,516,70,70,70,176,351,365,481,78,78,276]
prekazkaXb=[295,308,322,345,393,410,444,483,518,552,591,649,705,729,748,770,794,817,828,627,679,897,183,278,278,278,238,278,231,278,278,278,278,278,251,272,246,897,897,897,96,694,619,271,200,500,707]
prekazkaYb=[517,512,505,498,487,483,478,467,457,440,423,402,383,374,363,352,340,336,332,414,390,559,578,528,528,528,534,528,530,528,528,528,528,528,540,539,566,559,559,559,229,401,415,531,300,400,326]
prekazky=27             #počet prekážok, musí sedieť... ^súradnice prekážok
defaultobrys="black"    #predvolený obrys vecí
prekazkaobrys=[defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys]
oznacobrys="red"        #predvolený obrys označených vecí... ^obrys prekážok
oznacoffset=30          #ako ďaleko musí kurzor byť pre označenie prekážok
prX=1600                #šírka prostredia
prY=900                 #výška prostredia
minX=0                  #X ľavej steny
minY=0                  #Y hornej steny
predX=[0,0]             #začiatočný počet snímok so stlačenou loptou
predY=[0,0]             #---||---
ms=int(1/fps*1000)      #výpočet čakacej doby na ďalšiu snímku
x=[600,1000]            #začiatočné pozície lopiet
y=[800,800]             #---||---
fx=[20,10]              #začiatočné sily lopiet
fy=[0,0]                #---||---
vyberl=0                #koľkáta lopta je teraz vybraná
o=-1                    #používa sa na výpočet [o] lopty
cursorhit=1             #či bude kurzor okolo seba mať prekážku
cursorR=40              #polomer prekážky kurzoru
cursorX=0               #
cursorY=0               #
cursorFx=0              #
cursorFy=0              #
cursorPx=0              #
cursorPy=0              #
treniecur=150           #percento zachovania sily lopiet pri dotyku s kurzorhitom
abssila=10              #činiteľ sily dávanej pri stlačení lopty

#Vytvoriť prostredia
pr = Canvas(height=prY,width=prX,bg="#fff")
pr.pack()

#Program
def lopticka(o):#sledovanie stlačenia a vykreslenie lopty o
    global x,y,predX,predY,prekazkaXa,prekazkaXb,prekazkaYa,prekazkaYb,prekazky,fps
    if o==vyberl:
        oznaceny=oznacobrys
    else:
        oznaceny=defaultobrys
    for i in range(0,prekazky):
        if (prekazkaXb[i]-1>x[o]+r[o]>prekazkaXa[i]+1 and prekazkaYb[i]-1>y[o]>prekazkaYa[i]+1):
            predX[o]=(2/60)*fps
        elif (prekazkaXb[i]-1>x[o]>prekazkaXa[i]+1 and prekazkaYb[i]-1>y[o]+r[o]>prekazkaYa[i]+1):
            predY[o]=(2/60)*fps
        elif (prekazkaXb[i]-1>x[o]-r[o]>prekazkaXa[i]+1 and prekazkaYb[i]-1>y[o]>prekazkaYa[i]+1):
            predX[o]=(2/60)*fps
        elif (prekazkaXb[i]-1>x[o]>prekazkaXa[i]+1 and prekazkaYb[i]-1>y[o]-r[o]>prekazkaYa[i]+1):
            predY[o]=(2/60)*fps
    for i in range(0,lopty):
        if x[i]+r[i]-1>x[o]+r[o]>x[i]-r[i]+1 and y[i]+r[i]-1>y[o]>y[i]-r[i]+1:
            predX[o]=(2/60)*fps
        if x[i]+r[i]-1>x[o]>x[i]-r[i]+1 and y[i]+r[i]-1>y[o]+r[o]>y[i]-r[i]+1:
            predY[o]=(2/60)*fps
        if x[i]+r[i]-1>x[o]-r[o]>x[i]-r[i]+1 and y[i]+r[i]-1>y[o]>y[i]-r[i]+1:
            predX[o]=(2/60)*fps
        if x[i]+r[i]-1>x[o]>x[i]-r[i]+1 and y[i]+r[i]-1>y[o]-r[o]>y[i]-r[i]+1:
            predY[o]=(2/60)*fps
    if (x[o]+r[o]>prX+1 or x[o]-r[o]<minX-1):
        predX[o]=(2/60)*fps
    elif (y[o]+r[o]>prY+1 or y[o]-r[o]<minY-1):
        predY[o]=(2/60)*fps #kurzorhit V
    if cursorX+cursorR>=x[o]+r[o]>=cursorX-cursorR and cursorY+cursorR>=y[o]>=cursorY-cursorR:
        predX[o]=(2/60)*fps
    elif cursorX+cursorR>=x[o]>=cursorX-cursorR and cursorY+cursorR>=y[o]+r[o]>=cursorY-cursorR:
        predY[o]=(2/60)*fps
    elif cursorX+cursorR>=x[o]-r[o]>=cursorX-cursorR and cursorY+cursorR>=y[o]>=cursorY-cursorR:
        predX[o]=(2/60)*fps
    elif cursorX+cursorR>=x[o]>=cursorX-cursorR and cursorY+cursorR>=y[o]-r[o]>=cursorY-cursorR:
        predY[o]=(2/60)*fps
    if predX[o]>=1:
        pr.create_oval(x[o]-r[o]*deform,y[o]-r[o]/deform, x[o]+r[o]*deform,y[o]+r[o]/deform, outline=oznaceny,tag=o)
        predX[o]=predX[o]-1
    elif predY[o]>=1:
        pr.create_oval(x[o]-r[o]/deform,y[o]-r[o]*deform, x[o]+r[o]/deform,y[o]+r[o]*deform, outline=oznaceny,tag=o)
        predY[o]=predY[o]-1
    else: #keď je v pohybe tak tu sa robí deformácia v tom zmysle
        ry=r[o]/(1+abs(fx[o]/60*fps)*0.01)
        rx=r[o]/(1+abs(fy[o]/60*fps)*0.01)
        pr.create_oval(x[o]-rx, y[o]-ry, x[o]+rx, y[o]+ry, outline=oznaceny,tag=o)

def kolizie():#vypočítanie sily a miesta pri kolízii
    global x,r,minX,minY,prX,prY,absorbcia,fx,fy,x,y,prekazky,prekazkaXa,prekazkaYa,prekazkaXb,prekazkaYb,o,treniecur,abssila
    if cursorhit==1: #kolízie s kurzorhitom
        if cursorX+cursorR>=x[o]+r[o]>=cursorX-cursorR and cursorY+cursorR>=y[o]>=cursorY-cursorR:
            fx[o]=fx[o]*(-1)/(absorbcia[o])
            x[o]=cursorX-cursorR-r[o]
            indexfx=fx[o]-cursorFx
            indexfy=fy[o]-cursorFy
            fx[o]=(fx[o]-abs(indexfx))
            fy[o]=fy[o]-indexfy/200*treniecur
        elif cursorX+cursorR>=x[o]>=cursorX-cursorR and cursorY+cursorR>=y[o]+r[o]>=cursorY-cursorR:
            fy[o]=fy[o]*(-1)/(absorbcia[o])
            y[o]=cursorY-cursorR-r[o]+1
            indexfx=fx[o]-cursorFx
            indexfy=fy[o]-cursorFy
            fy[o]=(fy[o]-abs(indexfy))
            fx[o]=fx[o]-indexfx/200*treniecur
        elif cursorX+cursorR>=x[o]-r[o]>=cursorX-cursorR and cursorY+cursorR>=y[o]>=cursorY-cursorR:
            fx[o]=fx[o]*(-1)/(absorbcia[o])
            x[o]=cursorX+cursorR+r[o]
            indexfx=fx[o]-cursorFx
            indexfy=fy[o]-cursorFy
            fx[o]=(fx[o]+abs(indexfx))
            fy[o]=fy[o]-indexfy/200*treniecur
        elif cursorX+cursorR>=x[o]>=cursorX-cursorR and cursorY+cursorR>=y[o]-r[o]>=cursorY-cursorR:
            fy[o]=fy[o]*(-1)/(absorbcia[o])
            y[o]=cursorY+cursorR+r[o]
            indexfx=fx[o]-cursorFx
            indexfy=fy[o]-cursorFy
            fy[o]=(fy[o]+abs(indexfy))
            fx[o]=fx[o]-indexfx/200*treniecur
    for i in range(0,prekazky): #kolízie s prekážkami
        if prekazkaXb[i]>=x[o]+r[o]>=prekazkaXa[i] and prekazkaYb[i]>=y[o]>=prekazkaYa[i]:
            fx[o]=fx[o]*(-1)/(absorbcia[o])
            x[o]=prekazkaXa[i]-r[o]
        elif prekazkaXb[i]>=x[o]>=prekazkaXa[i] and prekazkaYb[i]>=y[o]+r[o]>=prekazkaYa[i]:
            fy[o]=fy[o]*(-1)/(absorbcia[o])
            y[o]=prekazkaYa[i]-r[o]
        elif prekazkaXb[i]>=x[o]-r[o]>=prekazkaXa[i] and prekazkaYb[i]>=y[o]>=prekazkaYa[i]:
            fx[o]=fx[o]*(-1)/(absorbcia[o])
            x[o]=prekazkaXb[i]+r[o]
        elif prekazkaXb[i]>=x[o]>=prekazkaXa[i] and prekazkaYb[i]>=y[o]-r[o]>=prekazkaYa[i]:
            fy[o]=fy[o]*(-1)/(absorbcia[o])
            y[o]=prekazkaYb[i]+r[o]
    for i in range(0,lopty): #kolízie s loptami (skrátené pre žiadnu potrebu)
        if i!=o:
            if x[i]+r[i]>=x[o]+r[o]>=x[i]-r[i] and y[i]+r[i]>=y[o]>=y[i]-r[i]:
                indexfx=fx[o]-fx[i]
                indexfy=fy[o]-fy[i]
                fx[o]=(fx[o]-indexfx)
                fx[i]=(fx[i]+indexfx)
                fy[o]=fy[o]-indexfy/200*(treniel[o]+treniel[i])
                fy[i]=fy[i]+indexfy/200*(treniel[o]+treniel[i])
                x[o]=x[i]-r[i]-r[o]
                if predX[o]>=1:
                    fx[o]-=absorbcia[o]*predX[o]/fps*abssila
                if predX[i]>=1:
                    fx[i]+=absorbcia[i]*predX[i]/fps*abssila
            elif x[i]+r[i]>=x[o]>=x[i]-r[i] and y[i]+r[i]>=y[o]+r[o]>=y[i]-r[i]:
                indexfx=fx[o]-fx[i]
                indexfy=fy[o]-fy[i]
                fy[o]=(fy[o]-indexfy)
                fy[i]=(fy[i]+indexfy)
                fx[o]=fx[o]-indexfx/200*(treniel[o]+treniel[i])
                fx[i]=fx[i]+indexfx/200*(treniel[o]+treniel[i])
                y[o]=y[i]-r[i]-r[o]
                if predY[o]>=1:
                    fy[i]+=absorbcia[o]*predY[o]/fps*abssila
                if predX[i]>=1:
                    fy[o]-=absorbcia[i]*predY[i]/fps*abssila
    if x[o]+r[o]>=prX: #kolízie so stenami
        fx[o]=fx[o]*(-1)/(absorbcia[o])
        x[o]=prX-r[o]-1
    elif x[o]-r[o]<=minX:
        fx[o]=fx[o]*(-1)/(absorbcia[o])
        x[o]=r[o]+1
    if y[o]+r[o]>=prY:
        fy[o]=fy[o]*(-1)/(absorbcia[o])
        y[o]=prY-r[o]
    elif y[o]-r[o]<=minY:
        fy[o]=fy[o]*(-1)/(absorbcia[o])
        y[o]=r[o]
                    
def prekazkyf():#vykreslenie prekážok
    global prekazky
    for i in range(0,prekazky):
        pr.create_rectangle(prekazkaXa[i],prekazkaYa[i],prekazkaXb[i],prekazkaYb[i], outline=prekazkaobrys[i],tag='prekazky')
    if cursorhit==1:
        pr.create_rectangle(cursorX-cursorR,cursorY-cursorR, cursorX+cursorR,cursorY+cursorR,tag='prekazky')

def ambientF(p):#vypočítanie polohy na základe sily a pridanie sily prostredia
    global o,x,y,fx,fy
    x[o]=x[o]+fx[o]*120/fps*p                 #pridať silu
    y[o]=y[o]+fy[o]*120/fps*p                 #pridať silu
    fx[o]=fx[o]/(trenie[o]/fps+1)*p         #trenie
    fy[o]=fy[o]/(trenie[o]/fps+1)*p         #trenie
    fy[o]=fy[o]+g[o]/fps*p                  #gravitácia
    
def L(p):#pohyby
    global fx,vyberl
    fx[vyberl]=fx[vyberl]-(so/fps)
def R(p):
    global fx,vyberl
    fx[vyberl]=fx[vyberl]+(so/fps)
def U(p):
    global fy,vyberl
    fy[vyberl]=fy[vyberl]-(so/fps)
def D(p):
    global fy,vyberl
    fy[vyberl]=fy[vyberl]+(so/fps)
def klik(p):
    global x,y,fx,fy,line,vyberl
    if line==1:
        pr.create_line(x[vyberl],y[vyberl],p.x,p.y, tag="track")
    if p.x>x[vyberl]:
        fx[vyberl]=fx[vyberl]+(p.x-x[vyberl])/(200/60*fps)
    elif p.x<x[vyberl]:
        fx[vyberl]=fx[vyberl]-(x[vyberl]-p.x)/(200/60*fps)
    if p.y>y[vyberl]:
        fy[vyberl]=fy[vyberl]+(p.y-y[vyberl])/(200/60*fps)
    elif p.y<y[vyberl]:
        fy[vyberl]=fy[vyberl]-(y[vyberl]-p.y)/(200/60*fps)

def oznacenieA(p):#presúvanie ľavého horného rohu
    global prekazkaXa,prekazkaXb
    for i in range(0,prekazky):
        if prekazkaXb[i]+oznacoffset>=p.x>=prekazkaXa[i]-oznacoffset and prekazkaYb[i]+oznacoffset>=p.y>=prekazkaYa[i]-oznacoffset:
            prekazkaXa[i]=p.x
            prekazkaYa[i]=p.y
            
def oznacenieB(p):#presúvanie pravého dolného rohu
    global prekazkaXa,prekazkaXb
    for i in range(0,prekazky):
        if prekazkaXb[i]+oznacoffset>=p.x>=prekazkaXa[i]-oznacoffset and prekazkaYb[i]+oznacoffset>=p.y>=prekazkaYa[i]-oznacoffset:
            prekazkaXb[i]=p.x
            prekazkaYb[i]=p.y

def objekt(p):#výroba prekážky
    global prekazky,prekazkaXa,prekazkaXb
    prekazkaXa.insert(prekazky,p.x)
    prekazkaYa.insert(prekazky,p.y)
    prekazkaXb.insert(prekazky,p.x+50)
    prekazkaYb.insert(prekazky,p.y+50)
    prekazkaobrys.insert(prekazky,"black")
    prekazky=prekazky+1

def oznacenie(p):#pohyb myši dá túto funkciu
    global prekazkaobrys,defaultobrys
    for i in range(0,prekazky):#sledovanie či je prekážka označená
        if prekazkaXb[i]+oznacoffset>=p.x>=prekazkaXa[i]-oznacoffset and prekazkaYb[i]+oznacoffset>=p.y>=prekazkaYa[i]-oznacoffset:
            prekazkaobrys[i]=oznacobrys
        else:
            prekazkaobrys[i]=defaultobrys
    if cursorhit==1:#vypočítanie polohy kurzorhitu
        global cursorX,cursorY,cursorFx,cursorFy,cursorR
        cursorX=p.x
        cursorY=p.y
            
def printit(p):#napísanie nastavení prekážok
    print(*prekazkaXa,sep=",")
    print(*prekazkaYa,sep=",")
    print(*prekazkaXb,sep=",")
    print(*prekazkaYb,sep=",")
    print(prekazky)
    
def vymaz(p):#vymazanie prekážky
    global prekazky,prekazkaXb,prekazkaXa,prekazkaYb,prekazkaYa,oznacoffset
    for i in range(0,prekazky):
        if prekazkaXb[i]+oznacoffset>=p.x>=prekazkaXa[i]-oznacoffset and prekazkaYb[i]+oznacoffset>=p.y>=prekazkaYa[i]-oznacoffset:
            prekazky-=1
            for o in range(i,prekazky-1):
                prekazkaXa[o]=prekazkaXa[o+1]
                prekazkaYa[o]=prekazkaYa[o+1]
                prekazkaXb[o]=prekazkaXb[o+1]
                prekazkaYb[o]=prekazkaYb[o+1]
    
def vyberB(p):#výber lopty
    global vyberl,lopty
    if p.delta==-120:
        if vyberl<=0:
            vyberl=0
        else:
            vyberl-=1
    elif p.delta==120:
        if vyberl>=lopty-1:
            vyberl=lopty-1
        else:
            vyberl+=1
    print(vyberl)

def objektl(p):#lopta pridaná
    global x,y,r,fx,fy,g,absorbcia,trenie,treniel,lopty,vyberl
    x.insert(lopty,p.x)
    y.insert(lopty,p.y)
    r.insert(lopty,r[vyberl])
    fx.insert(lopty,fx[vyberl])
    fy.insert(lopty,fy[vyberl])
    g.insert(lopty,g[vyberl])
    absorbcia.insert(lopty,absorbcia[vyberl])
    trenie.insert(lopty,trenie[vyberl])
    treniel.insert(lopty,treniel[vyberl])
    predX.insert(lopty,predX[vyberl])
    predY.insert(lopty,predY[vyberl])
    lopty+=1

def vymazl(p):
    global lopty
    lopty-=1

def kurzorhitF():
    global cursorPx,cursorPy,cursorFx,cursorFy,cursorX,cursorY
    cursorFx=cursorX-cursorPx
    cursorFy=cursorY-cursorPy
    cursorPx=cursorX
    cursorPy=cursorY

def magneto(p):
    for o in range(0,lopty):
        x[o]=p.x
        y[o]=p.y

pr.bind('<MouseWheel>',vyberB)
pr.bind_all('<Left>',L)
pr.bind_all('<Right>',R)
pr.bind_all('<Up>',U)
pr.bind_all('<Down>',D)
pr.bind_all('<Return>',objekt)
pr.bind('<B1-Motion>',klik)
pr.bind('<Button-1>',klik)
pr.bind('<Button-3>',oznacenieA)
pr.bind('<B3-Motion>',oznacenieA)
pr.bind('<Button-2>',oznacenieB)
pr.bind('<B2-Motion>',oznacenieB)
pr.bind('<Motion>',oznacenie)
pr.bind_all('<Delete>',vymaz)
pr.bind_all('<P>',printit)
pr.bind_all('<N>',objektl)
pr.bind_all('<M>',vymazl)
pr.bind_all('<H>',magneto)

vykreslita=1
while lowpower==0:
    for o in range(0,lopty):
        ambientF(1)
        kolizie()
    if vykreslita>=vykreslit:
        vykreslita=1
        for o in range(0,lopty):
            lopticka(o)
        pr.update()
        pr.delete('all')
    
    vykreslita+=1
    kurzorhitF()
    prekazkyf()
    pr.after(ms)


while lowpower==1:
    if o>=lopty-1:
        o=0
    else:
        o+=1
    if zrychlovanie==1:
        ambientF(lopty)
    else:
        ambientF(1)
    
    kurzorhitF()
    kolizie()
    for i in range(0,lopty):
        lopticka(i)
    prekazkyf()
    pr.update()
    pr.delete('all')
    pr.after(ms)
    
