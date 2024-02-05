#Nastavenia-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from time import *
from math import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mbox
from random import *
import winsound as ws
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
x=600
y=0
skóre=0
dvdx=[]
dvdy=[]
dvdXrych=[]
dvdYrych=[]

vhre=False
menu1=True
tlpress=0
tlhover=0
tlhoverp=0
warn=True

tlr=128
tlg=128
tlb=128
tldef=128


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
        return 1/(time()-tick)
    except:
        return 1000

def pozadie():
    global dvdx,dvdy,dvdXrych,dvdYrych
    for i in range(len(dvdx)):
      dvdx[i]+=dvdXrych[i]
      dvdy[i]+=dvdYrych[i]
      if dvdx[i]>prX or dvdx[i]<0:
          dvdXrych[i]/=-1
      if dvdy[i]>prY or dvdy[i]<0:
          dvdYrych[i]/=-1
      pr.create_oval(dvdx[i]-100,dvdy[i],dvdx[i]+100,dvdy[i]+40,fill="black")
      pr.create_oval(dvdx[i]-25,dvdy[i]+15,dvdx[i]+25,dvdy[i]+25,fill="white")
      pr.create_text(dvdx[i],dvdy[i]-20,text="DVD",font="Arial 32")

def menu1f1(s):
  global tlpress
  if prX/2+100>=s.x>=prX/2-100 and prY/2+40>=s.y>=prY/2:
    tlpress=1
  if prX/2+100>=s.x>=prX/2-100 and prY/2+90>=s.y>=prY/2+50:
    tlpress=2

def menu1f2():
  pr.create_text(prX/2,20,text="Predchádzajúce skóre: "+str(skóre))
  if tlhover==1 or tlhoverp==1:
    pr.create_rectangle(prX/2-100-tlhovertick,prY/2-tlhovertick,prX/2+100+tlhovertick,prY/2+40+tlhovertick,fill=rgb((tlr,tlg,tlb)),outline=rgb((tlr,tlg,tlb)))
  else:
    pr.create_rectangle(prX/2-100,prY/2,prX/2+100,prY/2+40,fill=rgb((tlr,tlg,tlb)),outline=rgb((tlr,tlg,tlb)))
    
  if tlhover==2 or tlhoverp==2:
    pr.create_rectangle(prX/2-100-tlhovertick,prY/2+50-tlhovertick,prX/2+100+tlhovertick,prY/2+90+tlhovertick,fill=rgb((tlr,tlg,tlb)),outline=rgb((tlr,tlg,tlb)))
    pass
  else:
    pr.create_rectangle(prX/2-100,prY/2+50,prX/2+100,prY/2+90,fill=rgb((tlr,tlg,tlb)),outline=rgb((tlr,tlg,tlb)))
  pr.create_text(prX/2,prY/2+20,text="Hraj",font="Arial 15")
  pr.create_text(prX/2,prY/2+70,text="Odíď",font="Arial 15")

def menu1f3(s):
  global tlhover,tlr,tlg,tlb,tlhoverp
  tlhover=0
  if prX/2+100>=s.x>=prX/2-100 and prY/2+40>=s.y>=prY/2:
    tlhoverp=1
    tlhover=1
  elif prX/2+100>=s.x>=prX/2-100 and prY/2+90>=s.y>=prY/2+50:
    tlhoverp=2
    tlhover=2

def rgb(rgb):
    return "#"+'%02x%02x%02x' % rgb

#Prostredie-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
tk=Tk()
tk.title("SmajloSlovakian™")
pr=Canvas(tk,height=prY,width=prX,bg=prBG)
tk.protocol("WM_DELETE_WINDOW",koniec)
pr.grid()

#Setup------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
tlhovertick=0


start=time()
tick=time()
#Loop-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
while áno:
  if menu1:
    pr.bind("<Button-1>",menu1f1)
    pr.bind("<Motion>",menu1f3)
    menu1f2()
    if tlhover>0:
        tlhovertick*=1.5
        if tlhovertick>50:
          tlhovertick=50
    else:
        tlhovertick/=1.5
        if tlhovertick<0.1:
          tlhovertick=0.1
    if tlhoverp==1:
      tlg=tldef+int(tlhovertick)
      tlr=tldef-int(tlhovertick)
      tlb=tldef-int(tlhovertick)
    elif tlhoverp==2:
      tlr=tldef+int(tlhovertick)
      tlg=tldef-int(tlhovertick)
      tlb=tldef-int(tlhovertick)
    if tlpress==1:
        pr.unbind("<Button-1>")
        pr.unbind("<Motion>")
        menu1=False
        vhre=True
        tlpress=0
        dvdx=[]
        dvdy=[]
        dvdXrych=[]
        dvdYrych=[]
        y=0
        skóre=0
        en0=ttk.Entry()
        en0.grid()
        slová=["dvd","ahoj","hello","guten tag","slovo","hlas","hruška","jablko","čokoláda","tlačidlo","trieda","krieda","lopata","krompáč","železo","zlato","rozhlas","ovocie","číslo","sekera","obesenec"]
        text=choice(slová)
        censored="-"*(len(text)+1)
        ws.PlaySound(MEDIA+"Speech On.wav",1)
    if tlpress==2:
        koniec()


  if vhre:
    y+=0.25+0.05*skóre
    pozadie()
    pr.create_text(x,y,text=censored,font="Arial 20")
    for o in en0.get():
      if text.find(o)>=0:
        b=""
        for i in range(len(text)):
          if text[i]==o:
            b+=text[i]
          else:
            b+=censored[i]
        censored=b
    if en0.get()==text:
      ws.PlaySound(MEDIA+"Windows Print complete.wav",1)
      text=slová[randint(0,len(slová)-1)]
      censored="-"*len(text)
      y=0
      skóre+=1
      dvdx.append(randint(0,prX))
      dvdy.append(randint(0,prY))
      dvdXrych.append(randrange(-200,200)/100)
      dvdYrych.append(randrange(-200,200)/100)
      en0.delete(0,len(en0.get()))
    if y>prY+10:
      pr.create_text(prX/2,prY/2,text="Počet bodov: "+str(skóre),font="Arial 50",fill="green")
      vhre=False
      menu1=True
      en0.destroy()
      pr.update()
      ws.PlaySound(MEDIA+"tada.wav",10)

    if y>prY-200:
      warn+=1
    else:
      warn=0
    if warn==1:
      try:
        ws.PlaySound(MEDIA+"Ring01.wav",1)
      except:
        print("Príliš nízko!!")

    if tick-start>=timeout and timeout>=0:
      áno=False
  
  tk.update() #simple 120hz lock VV
  psleep(nonneg(minms-(time()-tick)))
  print(fps(tick),end="\r")
  tick=time()
  pr.delete("all")

#Koniec-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("program končí")
ws.PlaySound(MEDIA+"tada.wav",10)
tk.update()
