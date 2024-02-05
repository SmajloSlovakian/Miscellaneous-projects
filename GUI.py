

tldemo=[["0x","1y","2text","3farba","4fadefarba","5hovertick","6status","7maxhovertick","8ID","9dimension","10clicktick","11maxclicktick"]]
tl=[]
shover=-100,-100
sclick=False
srelease=False
hovXoffset=50
hovYoffset=10
id=0
cachepr=None

def rgb(rgb):
  rgb=list(rgb)
  for i in range(len(rgb)):
    if rgb[i]>255:
      rgb[i]=255
    elif rgb[i]<0:
      rgb[i]=0
  rgbb=(rgb[0],rgb[1],rgb[2])
  return "#"+'%02x%02x%02x' % rgbb

def tlačidlo(x,y,t="",f=(128,128,128),ff=(72,72,-72),maxht=100,dimension=(-100,-20,100,20),maxct=20):
  global tl, id
  tl.append([x,y,t,f,ff,0,0,maxht,id,dimension,0,maxct])
  id+=1
  redraw()
  return id-1

def update(multiplier=1):
  global tl, shover, sclick, srelease
  tl.sort(key=sorthelp)
  for i in tl:
    p=i[5]
    pp=i[10]
    if i[0]+i[9][2]>=shover[0]>=i[0]+i[9][0] and i[1]+i[9][3]>=shover[1]>=i[1]+i[9][1]:
      i[6]=1
      if i[5]==0:
        i[5]=0.1
      i[5]*=2*multiplier
      if i[5]>i[7]:
        i[5]=i[7]
    else:
      i[6]=0
      try:
        i[5]/=1.2*multiplier
      except:
        pass
      if i[5]<0.1:
        i[5]=0

    if sclick and i[6]==1:
      i[6]=2
      if i[10]==0:
        i[10]=0.1
      i[10]*=2*multiplier
      if i[10]>i[11]:
        i[10]=i[11]
    else:
      try:
        i[10]/=1.2*multiplier
      except:
        pass
      if i[10]<0.1:
        i[10]=0

    if srelease and i[6]==1:
      i[6]=3

    if p!=i[5] or pp!=i[10]:
      draw(i)

  srelease=False

def sorthelp(s):
  return s[5]

def redraw():
  cachepr.delete("GUI")
  for i in tl:
    draw(i)

def draw(i):
  cachepr.delete("GUI"+str(i[8]))
  if i[3][0]>=0:
    farba=(int(i[3][0]+i[4][0]/i[7]*i[5]),int(i[3][1]+i[4][1]/i[7]*i[5]),int(i[3][2]+i[4][2]/i[7]*i[5]))
    offX1=-hovXoffset/i[7]*(i[5]-i[10])+i[9][0]
    offY1=-hovYoffset/i[7]*(i[5]-i[10])+i[9][1]
    offX2=hovXoffset/i[7]*(i[5]-i[10])+i[9][2]
    offY2=hovYoffset/i[7]*(i[5]-i[10])+i[9][3]
    cachepr.create_rectangle(i[0]+offX1,i[1]+offY1,i[0]+offX2,i[1]+offY2,fill=rgb(farba),tag=("GUI"+str(i[8]),"GUI"))
    cachepr.create_text(i[0],i[1],text=i[2],tag=("GUI"+str(i[8]),"GUI"))

def reset():
  global tl,id
  tl=[]
  id=0
  redraw()

def terminate(n):
  r=tl.pop(idtoindex(n))
  redraw()
  return r

def idtoindex(n):
  for i in range(len(tl)):
    if tl[i][8]==n:
      return i

def hover(s):
  global shover
  shover=s.x,s.y

def click(s):
  global sclick
  sclick=True

def release(s):
  global srelease, sclick
  if sclick:
    sclick=False
    srelease=True

def setpr(pr):
  global cachepr
  cachepr=pr
  pr.bind("<Motion>",hover)
  pr.bind("<Button-1>",click)
  pr.bind("<ButtonRelease-1>",release)

def modify(ID, key, value):
  tl[idtoindex(ID)][key]=value
  draw(tl[idtoindex(ID)])

def status(n):
  try:
    return tl[idtoindex(n)][6]
  except:
    return -1
