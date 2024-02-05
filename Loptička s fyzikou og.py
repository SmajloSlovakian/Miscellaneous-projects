#Nastavenia
from random import *
from math import *
from tkinter import *
fps=120 #hodnoty väčšie znesenia spomalia hru! môže tiež spôsobiiť zmeny v animáciách
absorbcia=3 #menovateľ sily pri stene
so=60 #sila ovládania
r=20
g=20
trenie=0.6
line=1
deform=0.6
prekazkaXa=[245,258,272,295,343,360,394,433,468,502,541,599,655,679,698,720,744,767,778,577,629,827,96,228,228,228,188,228,181,228,228,228,228,228,201,222,196,827,827,827,67,644,569,221,75,75,657]
prekazkaYa=[467,462,455,448,437,433,428,417,407,390,373,352,333,324,313,302,290,286,282,364,340,70,59,478,478,478,484,478,480,478,478,478,478,478,490,489,516,70,70,70,176,351,365,481,78,78,276]
prekazkaXb=[295,308,322,345,393,410,444,483,518,552,591,649,705,729,748,770,794,817,828,627,679,897,183,278,278,278,238,278,231,278,278,278,278,278,251,272,246,897,897,897,96,694,619,271,200,500,707]
prekazkaYb=[517,512,505,498,487,483,478,467,457,440,423,402,383,374,363,352,340,336,332,414,390,559,578,528,528,528,534,528,530,528,528,528,528,528,540,539,566,559,559,559,229,401,415,531,300,400,326]
defaultobrys="black"
prekazkaobrys=[defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys,defaultobrys]
oznacobrys="red"
prekazky=27
oznacoffset=30
prX=1000
prY=600
minX=0
minY=0
predX=0
predY=0
ms=int(1/fps*1000)
x=100
y=100
fx=0
fy=0

#Vytvoriť prostredia
pr = Canvas(height=prY,width=prX,bg="#fff")
pr.pack()

#Program
def lopticka():
    global x,y,predX,predY,prekazkaXa,prekazkaXb,prekazkaYa,prekazkaYb,prekazky,fps
    x=x+fx*120/fps
    y=y+fy*120/fps
    pr.delete('all')
    for i in range(0,prekazky):
        if (prekazkaXb[i]-1>x+r>prekazkaXa[i]+1 and prekazkaYb[i]-1>y>prekazkaYa[i]+1):
            predX=(2/60)*fps
        elif (prekazkaXb[i]-1>x>prekazkaXa[i]+1 and prekazkaYb[i]-1>y+r>prekazkaYa[i]+1):
            predY=(2/60)*fps
        elif (prekazkaXb[i]-1>x-r>prekazkaXa[i]+1 and prekazkaYb[i]-1>y>prekazkaYa[i]+1):
            predX=(2/60)*fps
        elif (prekazkaXb[i]-1>x>prekazkaXa[i]+1 and prekazkaYb[i]-1>y-r>prekazkaYa[i]+1):
            predY=(2/60)*fps
    if (x+r>prX+1 or x-r<minX-1):
        predX=(2/60)*fps
    elif (y+r>prY+1 or y-r<minY-1):
        predY=(2/60)*fps
    if predX>=1:
        pr.create_oval(x-r*deform,y-r/deform, x+r*deform,y+r/deform)
        predX=predX-1
    elif predY>=1:
        pr.create_oval(x-r/deform,y-r*deform, x+r/deform,y+r*deform)
        predY=predY-1
    else: #keď je v pohybe tak tu sa robí deformácia v tom zmysle
        ry=r/(1+abs(fx/60*fps)*0.01)
        rx=r/(1+abs(fy/60*fps)*0.01)
        pr.create_oval(x-rx, y-ry, x+rx, y+ry)

def kolizie():
    global x,r,minX,minY,prX,prY,absorbcia,fx,fy,x,y,prekazky,prekazkaXa,prekazkaYa,prekazkaXb,prekazkaYb
    if x+r>=prX:
        fx=fx*(-1)/(absorbcia)
        x=prX-r
    elif x-r<=minX:
        fx=fx*(-1)/(absorbcia)
        x=r
    if y+r>=prY:
        fy=fy*(-1)/(absorbcia)
        y=prY-r
    elif y-r<=minY:
        fy=fy*(-1)/(absorbcia)
        y=r
    for i in range(0,prekazky):
        if prekazkaXb[i]>=x+r>=prekazkaXa[i] and prekazkaYb[i]>=y>=prekazkaYa[i]:
            fx=fx*(-1)/(absorbcia)
            x=prekazkaXa[i]-r
        if prekazkaXb[i]>=x>=prekazkaXa[i] and prekazkaYb[i]>=y+r>=prekazkaYa[i]:
            fy=fy*(-1)/(absorbcia)
            y=prekazkaYa[i]-r
        if prekazkaXb[i]>=x-r>=prekazkaXa[i] and prekazkaYb[i]>=y>=prekazkaYa[i]:
            fx=fx*(-1)/(absorbcia)
            x=prekazkaXb[i]+r
        if prekazkaXb[i]>=x>=prekazkaXa[i] and prekazkaYb[i]>=y-r>=prekazkaYa[i]:
            fy=fy*(-1)/(absorbcia)
            y=prekazkaYb[i]+r

def prekazkyf():
    global prekazky
    for i in range(0,prekazky):
        pr.create_rectangle(prekazkaXa[i],prekazkaYa[i],prekazkaXb[i],prekazkaYb[i], outline=prekazkaobrys[i])

def L(p):
    global fx
    fx=fx-(so/fps)
def R(p):
    global fx
    fx=fx+(so/fps)
def U(p):
    global fy
    fy=fy-(so/fps)
def D(p):
    global fy
    fy=fy+(so/fps)
def klik(p):
    global x,y,fx,fy, line
    if line==1:
        pr.create_line(x,y,p.x,p.y, tag="track")
    if p.x>x:
        fx=fx+(p.x-x)/(200/60*fps)
    elif p.x<x:
        fx=fx-(x-p.x)/(200/60*fps)
    if p.y>y:
        fy=fy+(p.y-y)/(200/60*fps)
    elif p.y<y:
        fy=fy-(y-p.y)/(200/60*fps)
def oznacenieA(p):
    global prekazkaXa,prekazkaXb
    for i in range(0,prekazky):
        if prekazkaXb[i]+oznacoffset>=p.x>=prekazkaXa[i]-oznacoffset and prekazkaYb[i]+oznacoffset>=p.y>=prekazkaYa[i]-oznacoffset:
            prekazkaXa[i]=p.x
            prekazkaYa[i]=p.y
            
def oznacenieB(p):
    global prekazkaXa,prekazkaXb
    for i in range(0,prekazky):
        if prekazkaXb[i]+oznacoffset>=p.x>=prekazkaXa[i]-oznacoffset and prekazkaYb[i]+oznacoffset>=p.y>=prekazkaYa[i]-oznacoffset:
            prekazkaXb[i]=p.x
            prekazkaYb[i]=p.y

def objekt(p):
    global prekazky,prekazkaXa,prekazkaXb
    prekazkaXa.insert(prekazky,p.x)
    prekazkaYa.insert(prekazky,p.y)
    prekazkaXb.insert(prekazky,p.x+50)
    prekazkaYb.insert(prekazky,p.y+50)
    prekazkaobrys.insert(prekazky,"black")
    prekazky=prekazky+1

def oznacenie(p):
    global prekazkaobrys,defaultobrys
    for i in range(0,prekazky):
        if prekazkaXb[i]+oznacoffset>=p.x>=prekazkaXa[i]-oznacoffset and prekazkaYb[i]+oznacoffset>=p.y>=prekazkaYa[i]-oznacoffset:
            prekazkaobrys[i]=oznacobrys
        else:
            prekazkaobrys[i]=defaultobrys
            
def printit(p):
    print(*prekazkaXa,sep=",")
    print(*prekazkaYa,sep=",")
    print(*prekazkaXb,sep=",")
    print(*prekazkaYb,sep=",")
    print(prekazky)
    
def vymaz(p):
    global prekazky,prekazkaXb,prekazkaXa,prekazkaYb,prekazkaYa,oznacoffset
    for i in range(0,prekazky):
        if prekazkaXb[i]+oznacoffset>=p.x>=prekazkaXa[i]-oznacoffset and prekazkaYb[i]+oznacoffset>=p.y>=prekazkaYa[i]-oznacoffset:
            prekazky-=1
            for o in range(i,prekazky-1):
                prekazkaXa[o]=prekazkaXa[o+1]
                prekazkaYa[o]=prekazkaYa[o+1]
                prekazkaXb[o]=prekazkaXb[o+1]
                prekazkaYb[o]=prekazkaYb[o+1]
    
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

while True:
    lopticka()
    prekazkyf()
    pr.update()
    pr.after(ms)
    fx=fx/(trenie/fps+1)       #trenie
    fy=fy/(trenie/fps+1)
    fy=fy+g/fps              #gravitácia
    kolizie()
    
