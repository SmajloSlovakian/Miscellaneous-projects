shover=-100,-100
sclick=False
srelease=False
hovXoffset=50
hovYoffset=10
cachepr=None
ids=0

class Button:
    _register=[]

    def terminate(c):
        for i in range(len(Button._register)):
            if Button._register[i] is c:
                del Button._register[i]
                del c
        redraw()

    def draw(c):
        cachepr.delete("GUI"+str(c.id))
        if c.f[0]>=0:
            farba=(int(c.f[0]+c.ff[0]/c.maxht*c.ht),int(c.f[1]+c.ff[1]/c.maxht*c.ht),int(c.f[2]+c.ff[2]/c.maxht*c.ht))
            offX1=-hovXoffset/c.maxht*(c.ht-c.ct)+c.dim[0]
            offY1=-hovYoffset/c.maxht*(c.ht-c.ct)+c.dim[1]
            offX2=hovXoffset/c.maxht*(c.ht-c.ct)+c.dim[2]
            offY2=hovYoffset/c.maxht*(c.ht-c.ct)+c.dim[3]
            cachepr.create_rectangle(c.x+offX1,c.y+offY1,c.x+offX2,c.y+offY2,fill=rgb(farba),tag=("GUI"+str(c.id),"GUI"))
            cachepr.create_text(c.x,c.y,text=c.txt,tag=("GUI"+str(c.id),"GUI"))

    def __init__(self,X,Y,Text="",Color=(128,128,128),FadeColor=(72,72,-72),MaxHoverTick=100,MaxClickTick=20,Dimensions=(-100,-20,100,20),Canvas=cachepr) -> None:
        global ids
        self._register.append(self)
        self.pr=Canvas
        self.x=X
        self.y=Y
        self.txt=Text
        self.f=Color
        self.ff=FadeColor
        self.maxht=MaxHoverTick
        self.maxct=MaxClickTick
        self.dim=Dimensions
        self.id=ids
        ids+=1
        self.ht,self.ct,self.stat=0,0,0
        redraw()

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

def setup(pr):
  global cachepr
  cachepr=pr
  pr.bind("<Motion>",hover)
  pr.bind("<Button-1>",click)
  pr.bind("<ButtonRelease-1>",release)

def update(multiplier=1):
  global shover, sclick, srelease
  Button._register.sort(key=sorthelp)
  for i in Button._register:
    p=i.ht-i.ct
    if i.x+i.dim[2]>=shover[0]>=i.x+i.dim[0] and i.y+i.dim[3]>=shover[1]>=i.y+i.dim[1]:
      i.stat=1
      if i.ht==0:
        i.ht=0.1
      i.ht*=2*multiplier
      if i.ht>i.maxht:
        i.ht=i.maxht
    else:
      i.stat=0
      try:
        i.ht/=1.2*multiplier
      except:
        pass
      if i.ht<0.1:
        i.ht=0

    if sclick and i.stat==1:
      i.stat=2
      if i.ct==0:
        i.ct=0.1
      i.ct*=2*multiplier
      if i.ct>i.maxct:
        i.ct=i.maxct
    else:
      try:
        i.ct/=1.2*multiplier
      except:
        pass
      if i.ct<0.1:
        i.ct=0

    if srelease and i.stat==1:
      i.stat=3

    if p!=i.ht-i.ct:
      i.draw()

  srelease=False

def reset():
  for i in Button._register:
    i.terminate()
  redraw()

