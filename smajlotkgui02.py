from tkinter import Canvas


shover=-100,-100
sclick=False
srelease=False
cachepr=None
ids=0
autotime=(0,0,20,5)

class Button:
  """
  Makes up a pretty good and easy to use button.
  It can be only used with one canvas (for now).
  It's made deactivated defaultly.
  To make it activated show up on screen, use .activate() (returns the button)
  Every screen refresh, use update() to refresh all the buttons.\n
  Use 120hz for the best looking animations - timing is frame dependant!
  """
  _register=[]

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
    cachepr.delete("GUI"+str(c.id))
    if c.actit>0:
      if c.f[0]>=0:
        if c.ht!=0 and not c.grey:
          farba=(int(c.f[0]+c.ff[0]/c.maxht*c.ht),int(c.f[1]+c.ff[1]/c.maxht*c.ht),int(c.f[2]+c.ff[2]/c.maxht*c.ht))
          offX1=-c.hovXo/c.maxht*(c.ht-c.ct)+c.dim[0]+((9-c.actit)*c.actidim[0])
          offY1=-c.hovYo/c.maxht*(c.ht-c.ct)+c.dim[1]+((9-c.actit)*c.actidim[1])
          offX2=c.hovXo/c.maxht*(c.ht-c.ct)+c.dim[2]+((9-c.actit)*c.actidim[2])
          offY2=c.hovYo/c.maxht*(c.ht-c.ct)+c.dim[3]+((9-c.actit)*c.actidim[3])
        else:
          if c.grey:
            farba=(int(c.f[0]+c.ff[0]/-2),int(c.f[1]+c.ff[1]/-2),int(c.f[2]+c.ff[2]/-2))
          else:
            farba=(int(c.f[0]),int(c.f[1]),int(c.f[2]))
          offX1=c.dim[0]+((9-c.actit)*c.actidim[0])
          offY1=c.dim[1]+((9-c.actit)*c.actidim[1])
          offX2=c.dim[2]+((9-c.actit)*c.actidim[2])
          offY2=c.dim[3]+((9-c.actit)*c.actidim[3])
        for i in trasluc(int(c.actit)):
          cachepr.create_rectangle(c.x+offX1,c.y+offY1,c.x+offX2,c.y+offY2,fill=rgb(farba),tag=("GUI"+str(c.id),"GUI"),stipple=i,outlinestipple=i)
      if c.actit>3:
        cachepr.create_text(c.x+((9-c.actit)*c.actidim[4]),c.y+((9-c.actit)*c.actidim[5]),text=c.txt,tag=("GUI"+str(c.id),"GUI"))

  def __init__(c,X,Y,Text="",Color=(128,128,128),FadeColor=(200,200,56),Disabled=False,MaxHoverTick=100,MaxClickTick=20,Dimensions=(-100,-20,100,20),TTA=0,Canvas=cachepr,ActiDim=(-10,0,-10,0,-10,0),HoverXoff=50,HoverYoff=10) -> None:
    global ids
    c._register.append(c)
    c.pr=Canvas
    c.x=X
    c.y=Y
    c.mx=X
    c.my=Y
    c.txt=Text
    c.f=Color
    c.ff=()
    try:
      for i in range(3): c.ff+=FadeColor[i]-Color[i],
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
    c.ht,c.ct,c.stat,c.actit=0,0,-1,0 # stat - 0=nič, 1=hover, 2=click, 3=unclick, -1=deaktiv
    c.pending=False


def trasluc(typ=9):
  if typ==0:
    return []
  if typ==1:
    return ["gray12"]
  elif typ==2:
    return ["gray25"]
  elif typ==3:
    return ["gray12","gray25"]
  elif typ==4:
    return ["gray50"]
  elif typ==5:
    return ["gray50","gray25"]
  elif typ==6:
    return ["gray75"]
  elif typ==7:
    return ["gray12","gray75"]
  elif typ==8:
    return ["gray75","gray50"]
  else:
    return [""]

def redraw():
  cachepr.delete("GUI")
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

def release(s):
  global srelease, sclick
  sclick=False
  srelease=True

def setup(pr:Canvas):
  global cachepr
  cachepr=pr
  pr.bind("<Motion>",hover)
  pr.bind("<Button-1>",click)
  pr.bind("<ButtonRelease-1>",release)

def update():
  global shover, sclick, srelease
  Button._register.sort(key=sorthelp)
  for i in Button._register:
    i:Button
    p=i.ht-i.ct,i.actit,i.x,i.y

    if i.stat==-1:
      # --------Deactivated ticking
      if i.pending: # Activation timer and watch
        if i.timetacti<=0:
          i.stat=0
        else:
          i.timetacti-=1
      if i.actit<0.1: # Activation animation timer
        i.actit=0
      else:
        i.actit/=1.1
    else:
      # --------Activated ticking
      if i.actit==0: # Deactivation animation timer
        i.actit=0.1
      else:
        if i.actit<9:
          i.actit*=1.1
          if i.actit>9:
            i.actit=9
        else:
          i.actit=9
      
      if not i.grey:
        # Not grayed ticking
        # Cursorcheck
        if i.mx+i.dim[2]>=shover[0]>=i.mx+i.dim[0]:
          if i.my+i.dim[3]>=shover[1]>=i.my+i.dim[1]:
            i.stat=1
          else: i.stat=0
        else: i.stat=0

        if i.stat==1: # Hover ticking
          # Hover timer
          if i.ht>=i.maxht: i.ht=i.maxht
          elif i.ht==0:     i.ht=0.1
          else:
            i.ht*=2
            if i.ht>=i.maxht: i.ht=i.maxht
          i.x=i.x-(i.x-((shover[0]-i.mx)/2+i.mx))/5 # Hover mover
          i.y=i.y-(i.y-((shover[1]-i.my)/2+i.my))/5
          if sclick:
            i.stat=2
            if i.ct>=i.maxct: i.ct=i.maxct # Click timer
            elif i.ct==0:     i.ct=0.1
            else:
              i.ct*=2
              if i.ct>=i.maxct: i.ct=i.maxct
          else:
            if i.ct<0.1:  i.ct=0
            else:         i.ct/=1.2
            if srelease:  i.stat=3
        else: # Unhover ticking
          if round(i.x)==round(i.mx): i.x=i.mx # Unhover mover
          else:                       i.x=i.x-(i.x-i.mx)/5
          if round(i.y)==round(i.my): i.y=i.my
          else:                       i.y=i.y-(i.y-i.my)/5
          # Unhover timer
          if i.ht<0.1:  i.ht=0
          else:         i.ht/=1.2
      
      if not i.pending: # Deactivation timer and watch
        if i.timetacti<=0:
          i.stat=-1
        else:
          i.timetacti-=1

    pp=i.ht-i.ct,i.actit,i.x,i.y
    ppp=False
    for l in range(len(p)):
      if p[l]!=pp[l]:
        ppp=True
    if ppp:
      i.draw()
    
  srelease=False


