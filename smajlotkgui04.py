from tkinter import Canvas


shover=-100,-100
spclick=False
sclick=False
sdouble=False
srelease=False
spclick2=False
sclick2=False
srelease2=False
cachepr=None
ids=0
selected=-1
autotime=(0,0,20,5)
clickbuffer=False, False

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
        if c.my+c.dim[3]>=shover[1]>=c.my+c.dim[1]:
          if c.mx+c.dim[2]>=shover[0]>=c.mx+c.dim[0]:
            c.stat=1
          else: c.stat=0
        else: c.stat=0

        if c.stat==1: # Hover ticking
          # Hover timer
          if c.ht>=c.maxht-1: c.ht=c.maxht
          elif c.ht==0:     c.ht=0.1
          else:
            c.ht=(c.ht-c.maxht)/(1.5**t)+c.maxht
            if c.ht>=c.maxht: c.ht=c.maxht
          c.x=((c.x-shover[0])-(c.mx-shover[0])/2)/(1.5**t)+shover[0]+(c.mx-shover[0])/2
          c.y=((c.y-shover[1])-(c.my-shover[1])/2)/(1.5**t)+shover[1]+(c.my-shover[1])/2
          if sclick:
            c.stat=2
            if c.ct>=c.maxct: c.ct=c.maxct # Click timer
            elif c.ct==0:     c.ct=0.1
            else:
              c.ct=(c.ct-c.maxct)/(2**t)+c.maxct
              if c.ct>=c.maxct: c.ct=c.maxct
          else:
            if c.ct<1:  c.ct=0
            else:         c.ct/=1.2**t
            if srelease:  c.stat=3
        else: # Unhover ticking
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

  def destroy(c):
    for i in range(len(c._register)):
      if c._register[i] is c:
        cachepr.delete("stkgui"+str(c))
        del c._register[i]

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
      rect(c,c.x,c.y,c.f,c.ff,c.ht,c.maxht,c.ct,c.grey,c.dim,c.actit,c.actidim,[c.hovXo,c.hovXo],[c.hovYo,c.hovYo],c.tags)
      if c.actit>3:
        cachepr.create_text(c.x+((9-c.actit)*c.actidim[4]),c.y+((9-c.actit)*c.actidim[5]),text=c.txt.format(c.dval),tags=["stkgui"+str(c),"stkgui"]+c.tags)

  def __init__(c,X,Y,Text="",Color=(128,128,128),FadeColor=(200,200,56),Disabled=False,MaxHoverTick=100,MaxClickTick=20,Dimensions=(-100,-20,100,20),TTA=0,Canvas=cachepr,ActiDim=(-10,0,-10,0,-10,0),HoverXoff=50,HoverYoff=10,DisplayVal="",tags=[]) -> None:
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

class Slider(Button):
  """
  Makes up a pretty good and easy to use slider.
  """
  _register=[]

  def draw(c):
    cachepr.delete("stkgui"+str(c))
    if c.actit>0:
      rect(c,c.x,c.y,c.fl,c.ffl,c.ht,c.maxht,c.ct,c.grey,(c.dim[0],c.dim[1],c.dim[2]*2*c.value-c.dim[2]+(c.mx-c.x),c.dim[3]),c.actit,(c.actidim[0],c.actidim[1],0,c.actidim[3]),[c.hovXo,0],[c.hovYo,c.hovYo],c.tags)
      rect(c,c.x,c.y,c.fr,c.ffr,c.ht,c.maxht,c.ct,c.grey,(-c.dim[0]*2*c.value+c.dim[0]+(c.mx-c.x),c.dim[1],c.dim[2],c.dim[3]),c.actit,(0,c.actidim[1],c.actidim[2],c.actidim[3]),[0,c.hovXo],[c.hovYo,c.hovYo],c.tags)
      if c.actit>3:
        cachepr.create_text(c.x+((9-c.actit)*c.actidim[4]),c.y+((9-c.actit)*c.actidim[5]),text=c.txt.format(c.dval),tag=["stkgui"+str(c),"stkgui"]+c.tags)

  def __init__(c,X,Y,Text="",ColorL=(128,128,128),ColorR=(128,128,128),FadeColorL=(200,200,56),FadeColorR=(56,200,56),DefaultValue=0.5,Disabled=False,MaxHoverTick=100,MaxClickTick=20,Dimensions=(-100,-20,100,20),TTA=0,Canvas=cachepr,ActiDim=(-10,0,-10,0,-10,0),HoverXoff=50,HoverYoff=10,DisplayVal="",Min=0,Max=1,IsInt=False,tags=[]) -> None:
    super().__init__(X, Y, Text, None, None, Disabled, MaxHoverTick, MaxClickTick, Dimensions, TTA, Canvas, ActiDim, HoverXoff, HoverYoff, DisplayVal, tags)
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


def rect(c,x,y,f,ff,ht,maxht,ct,grey,dim,actit,actidim,hovXo,hovYo,tags:tuple):
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
      cachepr.create_rectangle(x+offX1,y+offY1,x+offX2,y+offY2,fill=rgb(farba),tags=["stkgui"+str(c),"stkgui"]+tags,stipple=i,outlinestipple=i)


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

def sorthelp(s):
  return s.ht-s.ct

def hover(s):
  global shover
  shover=s.x,s.y

def click(s):
  global sclick
  sclick=True

def double(s):
  global sdouble
  sdouble=True

def click2(s):
  global sclick2
  sclick2=True

def release(s):
  global srelease, sclick
  sclick=False
  srelease=True

def release2(s):
  global srelease2, sclick2
  sclick2=False
  srelease2=True

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

def setup(pr:Canvas):
  global cachepr
  cachepr=pr
  pr.bind("<Motion>",hover,True)
  pr.bind("<Button-1>",click,True)
  pr.bind("<Double-1>",double,True)
  pr.bind("<ButtonRelease-1>",release,True)
  pr.bind("<Button-3>",click2,True)
  pr.bind("<ButtonRelease-3>",release2,True)
  #pr.bind_all("<Up>",up)
  #pr.bind_all("<Down>",down)

def updatelem(tick:float):
  Button._register.sort(key=sorthelp)
  for i in Button._register:
    i.update(tick)
  for i in Slider._register:
    i:Slider
    i.update(tick)
    if i.stat==2:
      i.value=1-(shover[0]-i.mx+i.dim[0])/(+i.dim[0]-i.dim[2])

      i.conval=i.value*(i.max-i.min)+i.min
      if i.int:
        i.value=round(i.conval-i.min)/(i.max-i.min)
        i.conval=round(i.conval)
  Animation.update()

def updatetools():
  global srelease,srelease2,sclick,sclick2,spclick,spclick2,clickbuffer,sdouble
  srelease=False
  srelease2=False
  sdouble=False
  clickbuffer=sclick, sclick2
  spclick,spclick2=clickbuffer

