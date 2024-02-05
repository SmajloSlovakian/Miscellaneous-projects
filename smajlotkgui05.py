from tkinter import Canvas


sphover=-100,-100
shover=-100,-100
spclick=""
sclick=""
sppress=""
spress=""
spscroll=0
sscroll=0
cachepr=None
ids=0
selected=-1
autotime=(0,0,20,5)

class Button:
  """
  Makes up a pretty good and easy to use button.
  It can be only used with one canvas (for now).
  It's made deactivated defaultly.
  To make it activated show up on screen, use .activate() (returns the button)
  Every screen refresh use updatelem() to refresh all the buttons.
  tick is deltatime
  """
  _register=[]

  def update(c,t):
    global shover, sclick
    p=c.ht-c.ct,c.actit,c.x,c.y
    t/=0.008333333333333333333333

    if c.stat==-1:
      # --------Deactivated ticking
      scursor.drop(0,str(c))
      if c.pending: # Activation timer and watch
        if c.timetacti<=0:
          c.stat=0
        else:
          c.timetacti-=1#*t

      if c.actit<1: # Deactivation animation timer
        c.actit=0
      else:
        c.actit/=1.1**t
    else:
      # --------Activated ticking
      if c.actit==0: # Activation animation timer
        c.actit=0.1
      else:
        if c.actit<9:
          c.actit=(c.actit-10)/(1.1**(t))+10
          if c.actit>9:
            c.actit=9
        else:
          c.actit=9
      #deactivation timer and watch je dole
      
      if not c.grey:
        # Not grayed ticking
        # Cursorcheck
        if scursor.holding(1,str(c)) or ((c.my+c.dim[3]>=shover[1]>=c.my+c.dim[1] and c.mx+c.dim[2]>=shover[0]>=c.mx+c.dim[0]) and Mask.check(c.layer)):
          scursor.catch(0,str(c))
        else:
          scursor.drop(0,str(c))

        if(scursor.holding(0,str(c)) or scursor.holding(1,str(c))):
          c.stat=1
        else:
          c.stat=0

        if c.stat==1: # Hover ticking
          # Hover timer
          if c.ht>=c.maxht-1: c.ht=c.maxht
          elif c.ht==0:     c.ht=0.1
          else:
            c.ht=(c.ht-c.maxht)/(1.5**t)+c.maxht
            if c.ht>=c.maxht: c.ht=c.maxht
          c.x=((c.x-shover[0])-(c.mx-shover[0])/2)/(1.5**t)+shover[0]+(c.mx-shover[0])/2
          c.y=((c.y-shover[1])-(c.my-shover[1])/2)/(1.5**t)+shover[1]+(c.my-shover[1])/2
          scursor.catch(1,str(c))
          if scursor.holding(1,str(c)):
            c.stat=2
            if c.ct>=c.maxct: c.ct=c.maxct # Click timer
            elif c.ct==0:     c.ct=0.1
            else:
              c.ct=(c.ct-c.maxct)/(2**t)+c.maxct
              if c.ct>=c.maxct: c.ct=c.maxct
          else:
            if c.ct<1:  c.ct=0
            else:         c.ct/=1.2**t
          if scursor.dropped[0]==str(c) and c.my+c.dim[3]>=shover[1]>=c.my+c.dim[1] and c.mx+c.dim[2]>=shover[0]>=c.mx+c.dim[0]:  c.stat=3
        else: # Unhover ticking
          if c.ct<1:  c.ct=0 # Unclick timer
          else:         c.ct/=1.2**t
          if round(c.x)==round(c.mx): c.x=c.mx # Unhover mover
          else:                       c.x=(c.x-c.mx)/(1.2**t)+c.mx
          if round(c.y)==round(c.my): c.y=c.my
          else:                       c.y=(c.y-c.my)/(1.2**t)+c.my
          # Unhover timer
          if c.ht<1:  c.ht=0
          else:         c.ht/=(1.2**t)
      else:
        if c.ct<1:  c.ct=0 # Unclick timer
        else:         c.ct/=1.2**t
        if round(c.x)==round(c.mx): c.x=c.mx # Unhover mover
        else:                       c.x=(c.x-c.mx)/(1.2**t)+c.mx
        if round(c.y)==round(c.my): c.y=c.my
        else:                       c.y=(c.y-c.my)/(1.2**t)+c.my
        # Unhover timer
        if c.ht<1:  c.ht=0
        else:         c.ht/=(1.2**t)

      if not c.pending: # Deactivation timer and watch
        if c.timetacti<=0:
          c.stat=-1
        else:
          c.timetacti-=1*t
    
      

    pp=c.ht-c.ct,c.actit,c.x,c.y
    ppp=False
    for l in range(len(p)):
      if p[l]!=pp[l]:
        ppp=True
    if ppp:
      c.draw()

  def forget(c):
    c._register.remove(c)
    cachepr.delete("stkgui"+str(c))
    return(c)

  def deactivate(c,time:int=None):
    c.pending=False
    if time==None:
      c.timetacti=c.maxtimetacti
    else:
      c.timetacti=time
    return c
  
  def activate(c,time:int=None):
    c.pending=True
    if time==None:
      c.timetacti=c.maxtimetacti
    else:
      c.timetacti=time
    return c

  def draw(c):
    cachepr.delete("stkgui"+str(c))
    if c.actit>0:
      rect(c,c.x,c.y,c.f,c.ff,c.ht,c.maxht,c.ct,c.grey,c.dim,c.actit,c.actidim,[c.hovXo,c.hovXo],[c.hovYo,c.hovYo],c.tags,(0,0,0),c.backf)
      cachepr.create_text(c.x+((9-c.actit)*c.actidim[4]),c.y+((9-c.actit)*c.actidim[5]),text=c.txt.format(c.dval),tags=["stkgui"+str(c),"stkgui"]+c.tags,fill=rgb(tupleint(tupleinterp((0,0,0),c.backf,c.actit/9))))

  def __init__(c,X,Y,Text="",Color=(128,128,128),FadeColor=(200,200,56),Disabled=False,MaxHoverTick=100,MaxClickTick=20,Dimensions=(-100,-20,100,20),TTA=0,Canvas=cachepr,ActiDim=(-10,0,-10,0,-10,0),HoverXoff=50,HoverYoff=10,DisplayVal="",tags=[],Backcol=(255,255,255),layer=0) -> None:
    global ids
    c._register.append(c)
    c.pr=Canvas
    c.x=X
    c.y=Y
    c.mx=X
    c.my=Y
    c.txt=Text
    c.dval=DisplayVal
    c.f=Color
    c.ff=()
    c.backf=Backcol
    try:
      c.ff=[FadeColor[i]-Color[i] for i in range(3)]
    except: pass
    c.maxht=MaxHoverTick
    c.maxct=MaxClickTick
    c.dim=Dimensions
    if TTA<0:
      c.maxtimetacti=(abs(c.x-autotime[0]))/autotime[2]+(abs(c.y-autotime[1]))/autotime[3]
      c.timetacti=c.maxtimetacti
    else:
      c.maxtimetacti=TTA
      c.timetacti=TTA
    c.grey=Disabled
    c.actidim=ActiDim
    c.hovXo=HoverXoff
    c.hovYo=HoverYoff
    c.id=ids
    ids+=1
    c.tags=tags
    c.ht,c.ct,c.stat,c.actit=0,0,-1,0 # stat - 0=nič, 1=hover, 2=click, 3=unclick, -1=deaktiv
    c.pending=False
    c.layer=layer

class Slider(Button):
  """
  Makes up a pretty good and easy to use slider.
  """

  def update(c, t):
    super().update(t)
    if(c.stat>=1):
      c.value+=sscroll*((c.max-c.min)/100)
    if c.stat==2:
      c.value=limit(1-(shover[0]-c.mx+c.dim[0])/(+c.dim[0]-c.dim[2]))
      c.conval=c.value*(c.max-c.min)+c.min
      if c.int:
        c.value=round(c.conval-c.min)/(c.max-c.min)
        c.conval=round(c.conval)

  def draw(c):
    cachepr.delete("stkgui"+str(c))
    if c.actit>0:
      rect(c,c.x,c.y,c.fl,c.ffl,c.ht,c.maxht,c.ct,c.grey,(c.dim[0],c.dim[1],c.dim[2]*2*c.value-c.dim[2]+(c.mx-c.x),c.dim[3]),c.actit,(c.actidim[0],c.actidim[1],0,c.actidim[3]),[c.hovXo,0],[c.hovYo,c.hovYo],c.tags,(0,0,0),c.backf)
      rect(c,c.x,c.y,c.fr,c.ffr,c.ht,c.maxht,c.ct,c.grey,(-c.dim[0]*2*c.value+c.dim[0]+(c.mx-c.x),c.dim[1],c.dim[2],c.dim[3]),c.actit,(0,c.actidim[1],c.actidim[2],c.actidim[3]),[0,c.hovXo],[c.hovYo,c.hovYo],c.tags,(0,0,0),c.backf)
      cachepr.create_text(c.x+((9-c.actit)*c.actidim[4]),c.y+((9-c.actit)*c.actidim[5]),text=c.txt.format(c.dval),tag=["stkgui"+str(c),"stkgui"]+c.tags,fill=rgb(tupleint(tupleinterp((0,0,0),c.backf,c.actit/9))))

  def __init__(c,X,Y,Text="",ColorL=(128,128,128),ColorR=(128,128,128),FadeColorL=(200,200,56),FadeColorR=(56,200,56),DefaultValue=0.5,Disabled=False,MaxHoverTick=100,MaxClickTick=20,Dimensions=(-100,-20,100,20),TTA=0,Canvas=cachepr,ActiDim=(-10,0,-10,0,-10,0),HoverXoff=50,HoverYoff=10,DisplayVal="",Min=0,Max=1,IsInt=False,tags=[],Backcol=(255,255,255),layer=0) -> None:
    super().__init__(X, Y, Text, None, None, Disabled, MaxHoverTick, MaxClickTick, Dimensions, TTA, Canvas, ActiDim, HoverXoff, HoverYoff, DisplayVal, tags, Backcol,layer)
    c.fl=ColorL
    c.fr=ColorR
    c.ffl=()
    c.ffr=()
    try:
      c.ffl=[FadeColorL[i]-ColorL[i] for i in range(3)]
      c.ffr=[FadeColorR[i]-ColorR[i] for i in range(3)]
    except: pass
    c.value=(DefaultValue-Min)/Max
    c.conval=DefaultValue
    c.min=Min
    c.max=Max
    c.int=IsInt
    if IsInt:
      round(c.conval)

class Animation:
  '''
  func parameter takes a function

  def func(tickNumber:int, params:tuple):
    pass
    
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

class Mask:
  _register=[]
  blocked=[]
  def forget(c):
    return Mask._register.pop(Mask._register.index(c))
  def check(layer):
    for i in Mask.blocked:
      if(layer<int(i)):
        return False
    return True
  def update(c):
    if(c.dim[0]==None or (c.dim[2]>shover[0]>c.dim[0] and c.dim[3]>shover[1]>c.dim[1])):
      Mask.blocked+=[str(c.layer)]
  def __init__(c,x,y,x2,y2,layer) -> None:
    c.dim=[x,y,x2,y2]
    c.layer=layer
    Mask._register+=[c]


def limit(var,min=0,max=1):
  if(var>max):
    return(max)
  if(var<min):
    return(min)
  return(var)
def rect(c,x,y,f,ff,ht,maxht,ct,grey,dim,actit,actidim,hovXo,hovYo,tags:tuple,out,back):
  if f[0]>=0:
    if ht!=0 and not grey:
      farba=(int(f[0]+ff[0]/maxht*ht),int(f[1]+ff[1]/maxht*ht),int(f[2]+ff[2]/maxht*ht))
      offX1=-hovXo[0]/maxht*(ht-ct)+dim[0]+((9-actit)*actidim[0])
      offY1=-hovYo[0]/maxht*(ht-ct)+dim[1]+((9-actit)*actidim[1])
      offX2=hovXo[1]/maxht*(ht-ct)+dim[2]+((9-actit)*actidim[2])
      offY2=hovYo[1]/maxht*(ht-ct)+dim[3]+((9-actit)*actidim[3])
    else:
      if grey:
        farba=(int(f[0]+ff[0]/-2),int(f[1]+ff[1]/-2),int(f[2]+ff[2]/-2))
      else:
        farba=(int(f[0]),int(f[1]),int(f[2]))
      offX1=dim[0]+((9-actit)*actidim[0])
      offY1=dim[1]+((9-actit)*actidim[1])
      offX2=dim[2]+((9-actit)*actidim[2])
      offY2=dim[3]+((9-actit)*actidim[3])
    for i in trasluc(int(actit)):
      cachepr.create_rectangle(x+offX1,y+offY1,x+offX2,y+offY2,fill=rgb(farba),tags=["stkgui"+str(c),"stkgui"]+tags,stipple=i,outline=rgb(tupleint(tupleinterp(out,back,actit/9))))

def trasluc(typ=9):
  if typ==0:
    return []
  elif typ==1:
    return ["gray12"]
  elif typ==2:
    return ["gray25"]
  elif typ==3:
    return ["gray25","gray12"]
  elif typ==4:
    return ["gray50"]
  elif typ==5:
    return ["gray50","gray25"]
  elif typ==6:
    return ["gray75"]
  elif typ==7:
    return ["gray75","gray12"]
  elif typ==8:
    return ["gray75","gray50"]
  else:
    return [""]

def redraw():
  cachepr.delete("stkgui")
  for i in Button._register:
    i.draw()

def rgb(rgb):
  rgb=list(rgb)
  for i in range(len(rgb)):
    if rgb[i]>255:
      rgb[i]=255
    elif rgb[i]<0:
      rgb[i]=0
  rgbb=(rgb[0],rgb[1],rgb[2])
  return "#"+'%02x%02x%02x' % rgbb

def revrgb(rgb):
  return(int(rgb[1:3],16),int(rgb[3:5],16),int(rgb[5:7],16))

def tupleinterp(tup1,tup2,ratio=0.5):
  ret=()
  for i in range(len(tup1)):
    ret+=(tup1[i]-tup2[i])*ratio+tup2[i],
  return(ret)

def tupleint(tup):
  ret=()
  for i in tup:
    ret+=int(i),
  return(ret)

def sortbyhovt(s):
  return -s.ht
def sortbylay(s):
  return -s.layer

def transclick(t):
  if(t[0]=="p"):
    if(t[1::] in sclick and not t[1::] in spclick):
      return(True)
  if(t[0]=="h"):
    if(t[1::] in sclick):
      return(True)
  if(t[0]=="r"):
    if(t[1::] in spclick and not t[1::] in sclick):
      return(True)
  return(False)

def transpress(t):
  if(t[0]=="p"):
    if(t[1::] in spress and not t[1::] in sppress):
      return(True)
  if(t[0]=="h"):
    if(t[1::] in spress):
      return(True)
  if(t[0]=="r"):
    if(t[1::] in sppress and not t[1::] in spress):
      return(True)
  return(False)
  
def hover(s):
  global shover
  shover=s.x,s.y
def scroll(s):
  global sscroll
  sscroll=s.delta/120

def click(s):
  global sclick
  sclick+="1"
def click2(s):
  global sclick
  sclick+="2"
def click3(s):
  global sclick
  sclick+="3"
def keypress(s):
  global spress
  spress+=s.char

def release(s):
  global sclick
  sclick=sclick.replace("1","")
def release2(s):
  global sclick
  sclick=sclick.replace("2","")
def release3(s):
  global sclick
  sclick=sclick.replace("3","")
def keyrelease(s):
  global spress
  spress=spress.replace(s.char,"")

def up(s):
  global shover,selected
  for i in Button._register:
    i:Button
    if i.stat==1:
      dirselect(i,1)
      return
    elif i.id==selected:
      dirselect(i,1)
  for i in Slider._register:
    i:Slider
    if i.stat==1:
      dirselect(i,1)
      return
    elif i.id==selected:
      dirselect(i,1)

def down(s):
  global shover,selected
  for i in Button._register:
    i:Button
    if i.stat==1:
      dirselect(i,-1)
      return
    elif i.id==selected:
      dirselect(i,-1)
  for i in Slider._register:
    i:Slider
    if i.stat==1:
      dirselect(i,-1)
      return
    elif i.id==selected:
      dirselect(i,-1)

def dirselect(i,u):
  global selected,shover
  for o in Button._register:
    if o.id==i.id+u:
      selected=o.id
      shover=o.mx,o.my
  for o in Slider._register:
    if o.id==i.id+u:
      selected=o.id
      shover=o.mx,o.my

class Cursor:
  def update(c):
    c.dropped=["","",""]
    if(not("1" in sclick)):c.dropped[0],c.dragging[0]=c.dragging[0],""
    if(not("2" in sclick)):c.dropped[1],c.dragging[1]=c.dragging[1],""
    if(not("3" in sclick)):c.dropped[2],c.dragging[2]=c.dragging[2],""
    c.hovering=""
  def catch(c,typ:int,id:str):
    if(typ==0):
      if(c.hovering==""):
        c.hovering=id
    elif(str(typ) in sclick and c.dragging[typ-1]==""):
      c.dragging[typ-1]=id
  def drop(c,typ:int,id:str):
    if(typ==0):
      if(c.hovering==id):
        c.hovering=""
    elif(c.dragging[typ-1]==id):
      c.dragging[typ-1]=""
  def holding(c,typ,id):
    if(typ==0):
      return(id==c.hovering)
    return(id==c.dragging[typ-1])
  def __init__(c) -> None:
    c.hovering=""
    c.dragging=["","",""]
    c.dropped=["","",""]

def setup(pr:Canvas):
  global cachepr,scursor
  cachepr=pr
  pr.bind("<Motion>",hover,True)
  pr.bind("<Button-1>",click,True)
  pr.bind("<ButtonRelease-1>",release,True)
  pr.bind("<Button-2>",click2,True)
  pr.bind("<ButtonRelease-2>",release2,True)
  pr.bind("<Button-3>",click3,True)
  pr.bind("<ButtonRelease-3>",release3,True)
  pr.bind_all("<KeyPress>", keypress,True)
  pr.bind_all("<KeyRelease>", keyrelease,True)
  pr.bind_all("<MouseWheel>",scroll,True)

def updatelem(tick:float):
  Button._register.sort(key=sortbyhovt)
  Button._register.sort(key=sortbylay)
  Mask.blocked=[]
  for i in Mask._register:
    i.update()
  for i in Button._register:
    i:Button
    i.update(tick)
  Animation.update()

def updatetools():
  global spclick,sppress,sphover,sscroll,spscroll
  spclick=sclick
  sppress=spress
  sphover=shover
  spscroll=sscroll
  sscroll=0
  scursor.update()


scursor=Cursor()