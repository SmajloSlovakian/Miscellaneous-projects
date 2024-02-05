from random import *
from paho.mqtt import client as cl
from time import *
try:
    from sense_hat import SenseHat
    emu=False
except:
    from SenseHatEmu import SenseHat
    emu=True

sh=SenseHat()
minms=1/30
setpixelBuffer=[]


class Animation:
  '''
  func parameter takes a function

  def func(tickNumber:int, params:tuple):
    None
    
  anim=Animation(func, 3)

  tickNumber will be 0, 1, 2
  '''
  _register=[]

  def update():
    o=-1
    for i in Animation._register:
      i:Animation
      o+=1
      if i.mulstat==i.multi:
        i.mulstat=1
        i.func(i.tick,i.params)
        i.tick+=1
      else:
        i.mulstat+=1
      if i.tick==i.length:
        del Animation._register[o]
        del i

  def __init__(c,func,ticklength:int,msMultiplier=1,params:tuple=()):
    Animation._register.append(c)
    c.multi=msMultiplier
    c.mulstat=1
    c.length=ticklength
    c.func=func
    c.params=params
    c.tick=0

def vykrič(č):
    v=0
    for i in range(č):
        v+=i+1
    return v

def výbuch(t,p):
    x,y,f,h=p
    x-=t
    y-=t
    for i in range(t*2):
        if x<8 and y<8 and x>=0 and y>=0:
            setpixelBuffer[x][y]=f
        x+=1
    for i in range(t*2):
        if x<8 and y<8 and x>=0 and y>=0:
            setpixelBuffer[x][y]=f
        y+=1
    for i in range(t*2):
        if x<8 and y<8 and x>=0 and y>=0:
            setpixelBuffer[x][y]=f
        x-=1
    for i in range(t*2):
        if x<8 and y<8 and x>=0 and y>=0:
            setpixelBuffer[x][y]=f
        y-=1
    sh.set_pixels(getcols(h))


def tu(cl,us,ms):
    msg,id=ms.payload.decode().split("#")
    if id==klID or not(protihr in id):
        return
    msg=msg.split(":")
    '''if msg[0]=="ping":
        pinging=False
        print(pingresponse)'''
    for i in lookingfor.keys():
        if i==msg[0]:
            lookingfor[i](msg[1:])

def pošli(typ:str,*hod,top:str="sos-it/loďky"):
    klient.publish(top,typ+":"+":".join(hod)+"#"+klID)

def čakať(**čo):
    global lookingfor
    lookingfor=čo

klID=str(random())
print(klID)
klient=cl.Client(klID)
klient.connect("broker.mqttdashboard.com")
klient.subscribe("sos-it/loďky")
klient.on_message=tu

def pixelbufferclear():
    global setpixelBuffer
    setpixelBuffer=[]
    for i in range(8):
        setpixelBuffer.append([])
        for o in range(8):
            setpixelBuffer[i].append([])
pixelbufferclear()

def getcols(hru):
    l=[]
    for i in range(len(hru)):
        for o in range(len(hru[i])):
            if len(setpixelBuffer[o][i])==3:
                l.append(setpixelBuffer[o][i])
            else:
                l.append(getcol(hru[o][i]))
    pixelbufferclear()
    return l

def getcol(o):
    if o[0] and not o[1]:
        return [255,0,255]
    if not(o[0]) and o[1]:
        return [0,0,255]
    if o[0] and o[1]:
        return [255,0,0]
    return [0,0,0]

def stickupdate():
    global shover, sclick
    for i in sh.stick.get_events():
        if i.action=="pressed":
            if i.direction=="right" and shover[0]<7:
                shover[0]+=1
            if i.direction=="down" and shover[1]<7:
                shover[1]+=1
            if i.direction=="left" and shover[0]>0:
                shover[0]-=1
            if i.direction=="up" and shover[1]>0:
                shover[1]-=1
            if i.direction=="middle":
                sclick=True

def init(s:list): # TODO tu treba veci zmeniť na vyberanie protihráča 
    global state,rad,protihr
    sprava,cislo=s
    if sprava=="1":
        #pošli("init",cislo,klID)
        return
    if sprava==klID:
        pošli("init",cislo,klID)
    else:
        return
    protihr=cislo
    if float(cislo)!=float(klID):
        state="play"
        čakať(strel=odozva)
        if float(cislo)<float(klID):
            rad=True
        else:
            rad=False

def placing(length,rotation:tuple,x,y):
    r=[]
    for i in range(length):
        r.append([x+rotation[0]*i,y+rotation[1]*i])
    return r

def odozva(s:list):
    global hru,hru2,rad,sent,state
    čo,h=s
    x,y=int(h[0]),int(h[1])
    if čo=="shoot":
        hru[x][y][1]=True
        pošli("strel","backfire",h+str(int(hru[x][y][0])))
        if not hru[x][y][0]:
            rad=True
            Animation(výbuch,5,4,(x,y,[0,0,255],hru))
        else:
            Animation(výbuch,5,4,(x,y,[255,0,0],hru))
        sh.set_pixels(getcols(hru))
        spi(20)
    elif čo=="backfire":
        sent=False,None
        hru2[x][y][0]=bool(int(h[2]))
        rad=bool(int(h[2]))
        hru2[x][y][1]=True
        sh.set_pixels(getcols(hru2))
        if hru2[x][y][0]:
            Animation(výbuch,5,4,(x,y,[255,0,0],hru2))
        else:
            Animation(výbuch,5,4,(x,y,[0,0,255],hru2))
        spi(20)
    elif čo=="vyhr":
        for x,y in h.split(","):
            setpixelBuffer[int(x)][int(y)]=[255,255,0]
        sh.set_pixels(getcols(hru2))
        sleep(10)
        sh.clear([50,0,0])
        sleep(2)
        reset()
        

def dirtran(o):
    if o==0:
        return 1,0
    elif o==1:
        return 0,1
    elif o==2:
        return -1,0
    elif o==3:
        return 0,-1

def spi(t):
    global slep
    slep+=t

def reset():
    global sent,lookingfor,hru,hru2,state,položiť,klID,protihr
    protihr=""
    klID=str(random())
    sent=False,None
    lookingfor={}
    hru=[] # 0 = loď:bool; 1 = trafené:bool
    hru2=[] # 0 = loď:bool; 1 = trafené:bool
    for i in range(8):
        hru.append([])
        hru2.append([])
        for o in range(8):
            hru[i].append([False,False])
            hru2[i].append([False,False])
    state="place"
    položiť=bomby

pingtimer=0
pingresponse=0
pinging=False
protihr=""
sent=False,None
lookingfor={}
shover=[0,0]
sclick=False
hru=[] # 0 = loď:bool; 1 = trafené:bool
hru2=[] # 0 = loď:bool; 1 = trafené:bool
state="place"
placeloď=False
rad=None
bomby=6
položiť=bomby
otoč=dirtran(randint(0,3))
for i in range(8):
    hru.append([])
    hru2.append([])
    for o in range(8):
        hru[i].append([False,False])
        hru2[i].append([False,False])
slep=0
tick=time()

try:
    while True:
        Animation.update()
        t=minms-(time()-tick)
        if t>0:
            sleep(t)
        tick=time()

        '''if not pinging:
            if time()-pingtimer>3:
                print("lala")
                pošli("ping")
                pinging=True
                pingtimer=time()
                pingresponse=0
        else:
            pingresponse+=1
            if pingresponse>60:
                klient.disconnect()
                klient.connect("broker.mqttdashboard.com")'''

        if slep!=0:
            slep-=1
        else:
            sclick=False
            if state=="place":
                stickupdate()
                inbound=False
                while not inbound:
                    inbound=True
                    placeloď=False
                    for x,y in placing(položiť,otoč,shover[0],shover[1]):
                        if x>7:
                            shover[0]-=x-7
                            inbound=False
                            break
                        elif x<0:
                            shover[0]-=x
                            inbound=False
                            break
                        if y>7:
                            shover[1]-=y-7
                            inbound=False
                            break
                        elif y<0:
                            shover[1]-=y
                            inbound=False
                            break
                        if hru[x][y][0]:
                            placeloď=True
                for x,y in placing(položiť,otoč,shover[0],shover[1]):
                    if not placeloď:
                        setpixelBuffer[x][y]=[255,255,0]
                    else:
                        setpixelBuffer[x][y]=[255,0,0]
                    if sclick and not placeloď:
                        hru[x][y][0]=True
                if sclick and not placeloď:
                    otoč=dirtran(randint(0,3))
                    položiť-=1
                if položiť==0:
                    čkm=Animation(výbuch,8,1,(0,0,[255,255,0],hru))
                    state="init"
                sh.set_pixels(getcols(hru))
            elif state=="init":
                if čkm.tick==čkm.length:
                    čkm=Animation(výbuch,8,1,(0,0,[255,255,0],hru))
                pošli("init","1",klID)
                čakať(init=init)
                sleep(0.5)
            elif state=="play":
                if rad:
                    stickupdate()
                    setpixelBuffer[shover[0]][shover[1]]=[255,255,255]
                    if sclick and not(hru2[shover[0]][shover[1]][1]) and not(sent[0]):
                        pošli("strel","shoot",str(shover[0])+str(shover[1]))
                        sent=True,shover
                    elif sent[0] and sclick:
                        pošli("strel","shoot",str(sent[1][0])+str(sent[1][1]))
                    poč=0
                    for i in hru2:
                        for b,o in i:
                            if b and o:
                                poč+=1
                    if poč==vykrič(bomby):
                        pošli("strel","vyhr",",".join([str(x)+str(y) for y in range(8) for x in range(8) if hru[x][y][0] and not hru[x][y][1]]))
                        reset()
                        state="vyhr"
                        vyhr=Animation(výbuch,8,3,(randint(0,7),randint(0,7),[randint(0,255),randint(0,255),randint(0,255)],hru))
                        vyhrtime=time()
                    sh.set_pixels(getcols(hru2))
                else:
                    sh.set_pixels(getcols(hru))
            elif state=="vyhr":
                if vyhr.tick==vyhr.length:
                    vyhr=Animation(výbuch,8,3,(randint(0,7),randint(0,7),[randint(0,255),randint(0,255),randint(0,255)],hru))
                if time()-vyhrtime>10:
                    state="place"
            klient.loop_read()
            klient.loop_write()
            klient.loop_misc()
except Exception as e:
    print(e)
    input("Enter to continue")