from tkinter import Canvas


shover=-100,-100
sclick=False
srelease=False
hovXoffset=50
hovYoffset=10
cachepr=None
ids=0
autotime=(0,0,20,5)

class Button:
  _register=[]

  def deactivate(c):
    c.pending=False
    c.ticktm=c.maxticktm
    return c
  
  def activate(c):
    c.pending=True
    c.ticktm=c.maxticktm

  def draw(c):
    cachepr.delete("GUI"+str(c.id))
    if c.vypt>0:
      if c.f[0]>=0:
        if c.ht!=0 and not c.vyp:
          farba=(int(c.f[0]+c.ff[0]/c.maxht*c.ht),int(c.f[1]+c.ff[1]/c.maxht*c.ht),int(c.f[2]+c.ff[2]/c.maxht*c.ht))
          offX1=-hovXoffset/c.maxht*(c.ht-c.ct)+c.dim[0]+((9-c.vypt)*c.vypdim[0])
          offY1=-hovYoffset/c.maxht*(c.ht-c.ct)+c.dim[1]+((9-c.vypt)*c.vypdim[1])
          offX2=hovXoffset/c.maxht*(c.ht-c.ct)+c.dim[2]+((9-c.vypt)*c.vypdim[2])
          offY2=hovYoffset/c.maxht*(c.ht-c.ct)+c.dim[3]+((9-c.vypt)*c.vypdim[3])
        else:
          if c.vyp:
            farba=(int(c.f[0]+c.ff[0]/-2),int(c.f[1]+c.ff[1]/-2),int(c.f[2]+c.ff[2]/-2))
          else:
            farba=(int(c.f[0]),int(c.f[1]),int(c.f[2]))
          offX1=c.dim[0]+((9-c.vypt)*c.vypdim[0])
          offY1=c.dim[1]+((9-c.vypt)*c.vypdim[1])
          offX2=c.dim[2]+((9-c.vypt)*c.vypdim[2])
          offY2=c.dim[3]+((9-c.vypt)*c.vypdim[3])
        for i in trasluc(int(c.vypt)):
          cachepr.create_rectangle(c.x+offX1,c.y+offY1,c.x+offX2,c.y+offY2,fill=rgb(farba),tag=("GUI"+str(c.id),"GUI"),stipple=i,outlinestipple=i)
      if c.vypt>3:
        cachepr.create_text(c.x+((9-c.vypt)*c.vypdim[4]),c.y+((9-c.vypt)*c.vypdim[5]),text=c.txt,tag=("GUI"+str(c.id),"GUI"))

  def __init__(self,X,Y,Text="",Color=(128,128,128),FadeColor=(200,200,56),Disabled=False,MaxHoverTick=100,MaxClickTick=20,Dimensions=(-100,-20,100,20),TTA=0,Canvas=cachepr,ActiDim=(-10,0,-10,0,-10,0)) -> None:
    global ids
    self._register.append(self)
    self.pr=Canvas
    self.x=X
    self.y=Y
    self.mx=X
    self.my=Y
    self.txt=Text
    self.f=Color
    self.ff=()
    for i in range(3):
      self.ff+=FadeColor[i]-Color[i],
    self.maxht=MaxHoverTick
    self.maxct=MaxClickTick
    self.dim=Dimensions
    if TTA<0:
      self.maxticktm=(abs(self.x-autotime[0]))/autotime[2]+(abs(self.y-autotime[1]))/autotime[3]
      self.ticktm=self.maxticktm
    else:
      self.maxticktm=TTA
      self.ticktm=TTA
    self.vyp=Disabled
    self.vypdim=ActiDim
    self.id=ids
    ids+=1
    self.ht,self.ct,self.stat,self.vypt=0,0,-1,0 # stat - 0=nič, 1=hover, 2=click, 3=unclick, -1=deaktiv
    self.pending=True
    self.draw()


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
    p=i.ht-i.ct,i.vypt,i.x,i.y

    if i.stat==-1:
      # --------Deactivated ticking
      if i.pending: # Activation timer and watch
        if i.ticktm<=0:
          i.stat=0
        else:
          i.ticktm-=1
      if i.vypt<0.1: # Activation animation timer
        i.vypt=0
      else:
        i.vypt/=1.1
    else:
      # --------Activated ticking
      if i.vypt==0: # Deactivation animation timer
        i.vypt=0.1
      else:
        if i.vypt<9:
          i.vypt*=1.1
        else:
          i.vypt=9
      
      if not i.vyp:
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
        if i.ticktm<=0:
          i.stat=-1
        else:
          i.ticktm-=1

    pp=i.ht-i.ct,i.vypt,i.x,i.y
    ppp=False
    for l in range(len(p)):
      if p[l]!=pp[l]:
        ppp=True
    if ppp:
      i.draw()
    
  srelease=False


