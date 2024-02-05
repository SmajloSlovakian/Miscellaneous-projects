from time import *
from tkinter import *
from random import *
import smajlotkgui05

guii=None
pr=None
apps=()
wintomake=[]

def sor(a:bool,b:bool):
    return a or b
def sand(a:bool,b:bool):
    return a and b
def setup(can:Canvas,smtkgui:smajlotkgui05,*applications):
    global pr,apps,guii
    apps+=applications
    pr=can
    guii=smtkgui

sphover=(0,0)
#########################################################################
test=0
class Window:
    _reg=[]
    clicked=False
    faspeed=0.5
    fasize=32 # 18
    maxpeed=1.3
    topbar=30
    startoffset=40,40
    def updall(t):
        global test,sphover
        t/=0.008333333333333333333333
        Window._reg.sort(key=sorthelp,reverse=True)
        Window.clicked=False
        for i in Window._reg:
            i:Window
            if(not i.updated):
                i.update(t)
        for i in Window._reg:
            i:Window
            i.updated=False
        sphover=guii.shover

    def update(c,t,f=False):
        c.mouse()
        c.mask.layer=len(Window._reg)-Window._reg.index(c)
        c.fadetick+=c.fading*t
        if not c.paused:
            c.app.update(c.clicking,(guii.shover[0]-c.x,guii.shover[1]-c.y-c.topbar),c,t/120)
        if c.fadetick>9:
            c.fading=0
            c.fadetick=9
            f=True
        elif c.fadetick<0:
            Window._reg.remove(c)
            pr.delete("Win"+str(c),"App"+str(c))
            c.mask.forget()
            return
        elif c.fading!=0:
            f=True
        if c.maximised:
            if round(c.x)!=0 or round(c.y)!=0 or round(c.dx)!=pr.winfo_width() or round(c.dy)!=pr.winfo_height():
                c.normalised=False
                f=True
                c.x/=c.maxpeed**t
                c.y/=c.maxpeed**t
                c.dx=(c.dx-pr.winfo_width())/(c.maxpeed**t)+pr.winfo_width()
                c.dy=(c.dy-pr.winfo_height())/(c.maxpeed**t)+pr.winfo_height()
                c.app.moved(c.x,c.y+c.topbar,c.dx,c.dy-c.topbar)
            elif c.x!=0:
                c.x=0
                c.y=0
                c.dx=pr.winfo_width()
                c.dy=pr.winfo_height()
        else:
            if sand(not c.normalised,round(c.x)!=c.prevdim[0] or round(c.y)!=c.prevdim[1] or round(c.dx)!=c.prevdim[2] or round(c.dy)!=c.prevdim[3]):
                f=True
                c.x=(c.x-c.prevdim[0])/(c.maxpeed**t)+c.prevdim[0]
                c.y=(c.y-c.prevdim[1])/(c.maxpeed**t)+c.prevdim[1]
                c.dx=(c.dx-c.prevdim[2])/(c.maxpeed**t)+c.prevdim[2]
                c.dy=(c.dy-c.prevdim[3])/(c.maxpeed**t)+c.prevdim[3]
                c.app.moved(c.x,c.y+c.topbar,c.dx,c.dy-c.topbar)
            else:
                c.normalised=True
        if f:
            c.draw()
        c.mask.dim=[c.x-c.topbar/3,c.y-c.topbar/3,c.x+c.dx+c.topbar/3,c.y+c.dy+c.topbar/3]
        if(c.resizing or c.moving):
            c.mask.dim[0]=None
            c.mask.layer+=1
        c.updated=True
    
    def mouse(c):
        if c.clicking or c.resizing!="":
            c.click()
        '''if c.fading==0 and not Window.clicked:
            if c.dx+c.x>=guii.shover[0]>=c.x:
                if c.dy+c.y>=guii.shover[1]>=c.y:
                    Window.clicked=True
                    c.click()
                    if c.ry<c.topbar:
                        if not c.maximised:
                            c.prevdim=round(c.x),round(c.y),round(c.dx),round(c.dy)
                        c.maximised=not c.maximised
                        c.app.moved(c.x,c.y+c.topbar,c.dx,c.dy-c.topbar)
                        c.draw()'''
        
        if guii.transclick("h1") and not(Window.clicked):
            if not "1" in guii.spclick:
                if c.dx+c.x>guii.shover[0]>c.x:
                    if c.dy+c.y>guii.shover[1]>c.y:
                        c.click()
                        if c.ry>c.topbar:
                            c.app.click(c.rx,c.ry-c.topbar)
                        elif c.rx>c.dx-c.topbar and c.app.deletable:
                            c.fading=-c.faspeed
                        elif c.rx>c.dx-c.topbar*2 and c.app.deletable:
                            if not c.maximised:
                                c.prevdim=round(c.x),round(c.y),round(c.dx),round(c.dy)
                            c.maximised=not c.maximised
                        else:
                            '''if c.maximised or not c.normalised:
                                c.prevdim=guii.shover[0], guii.shover[1], c.prevdim[2], c.prevdim[3]
                                #c.rx=c.dx/2
                                c.maximised=False
                                c.app.moved(c.x,c.y+c.topbar,c.dx,c.dy-c.topbar)
                                c.draw()'''
                            c.moving=True
                        Window.clicked=True
                        c.clicking=True
                if c.y+c.dy+c.topbar/3>guii.shover[1]>c.y-c.topbar/3 and c.resizable:
                    if c.dx+c.x+c.topbar/3>guii.shover[0]>c.x+c.dx:
                        Window.clicked=True
                        c.clicking=True
                        c.resizing+="R"
                        c.click()
                    elif c.x-c.topbar/3<guii.shover[0]<c.x:
                        Window.clicked=True
                        c.clicking=True
                        c.resizing+="L"
                        c.click()
                if c.x+c.dx+c.topbar/3>guii.shover[0]>c.x-c.topbar/3 and c.resizable:
                    if c.dy+c.y+c.topbar/3>guii.shover[1]>c.y+c.dy:
                        Window.clicked=True
                        c.clicking=True
                        c.resizing+="D"
                        c.click()
                    elif c.y-c.topbar/3<guii.shover[1]<c.y:
                        Window.clicked=True
                        c.clicking=True
                        c.resizing+="U"
                        c.click()
        else:
            if guii.shover[1]<=0 and c.moving:
                c.maximised=True
                c.prevdim=round(c.x),round(c.y),round(c.dx),round(c.dy)
            elif c.y<0:
                pr.move("Win"+str(c),0,-1*c.y)
                c.y=0
            c.resizing=""
            c.moving=False
            c.clicking=False
        if "1" in guii.sclick and not("1" in guii.spclick) and not(c.clicking):
            c.infocus=False

    def click(c):
        for i in Window._reg:
            i.infocus=False
        c.infocus=True
        c.draw()
        if c.moving:
            if not(c.normalised) or c.maximised:
                c.maximised=False
                c.prevdim=guii.shover[0]-c.prevdim[2]/2,guii.shover[1]-c.topbar/2,c.prevdim[2],c.prevdim[3]
            else:
                l=c.x,c.y
                c.x=guii.shover[0]-c.rx
                c.y=guii.shover[1]-c.ry
                #pr.moveto("Win"+str(c),c.x-1,c.y-1)
                pr.move("Win"+str(c),c.x-l[0],c.y-l[1])
                pr.move("App"+str(c),c.x-l[0],c.y-l[1])
            c.app.moved(c.x,c.y+c.topbar,c.dx,c.dy-c.topbar)
        elif c.resizing!="":
            if "R" in c.resizing:
                c.dx=guii.shover[0]-c.x
            elif "L" in c.resizing and c.dx+c.x-guii.shover[0]>=c.smallest[0]:
                c.dx+=c.x-guii.shover[0]
                c.x=guii.shover[0]
            if "D" in c.resizing:
                c.dy=guii.shover[1]-c.y
            elif "U" in c.resizing and c.dy+c.y-guii.shover[1]>=c.smallest[1]:
                c.dy+=c.y-guii.shover[1]
                c.y=guii.shover[1]

            if c.dx<c.smallest[0]:
                c.dx=c.smallest[0]
            if c.dy<c.smallest[1]:
                c.dy=c.smallest[1]
            c.draw()
            c.app.moved(c.x,c.y+c.topbar,c.dx,c.dy-c.topbar)
        c.rx=guii.shover[0]-c.x
        c.ry=guii.shover[1]-c.y

    def draw(c):
        l=c.fasize*c.fadetick/9-c.fasize
        pr.delete("Win"+str(c))

        #pr.create_rectangle(c.x-l-3,c.y-l-3,c.dx+c.x+l+3,c.dy+c.y+l+3,fill="black",stipple=guii.trasluc(4)[0],tags=("Win"+str(c),"Win"),width=0)
        #pr.create_rectangle(c.x-l-6,c.y-l-6,c.dx+c.x+l+6,c.dy+c.y+l+6,fill="black",stipple=guii.trasluc(1)[0],tags=("Win"+str(c),"Win"),width=0)
        for x,y,xx,yy in ((4,4,4,4),(2,2,2,2)):
            pr.create_rectangle(c.x-l+x,c.y-l+y,c.dx+c.x+l+xx,c.dy+c.y+l+yy,tags=("Win"+str(c),"Win"))


        for i in guii.trasluc(int(c.fadetick)):
            pr.create_rectangle(c.x-l,c.y-l,c.dx+c.x+l,c.dy+c.y+l,fill="white",tags=("Win"+str(c),"Win"),stipple=i,outlinestipple=i)
        pr.create_line(c.x-l,c.y+c.topbar-l,c.x+c.dx+l,c.y+c.topbar-l,tags=("Win"+str(c),"Win"))
        pr.create_text(c.x+c.dx/2,c.y+c.topbar/2-l,text=c.app.label,tags=("Win"+str(c),"Win"))
        if c.app.deletable:
            pr.create_text(c.x+c.dx-c.topbar*1.3/2+l,c.y+c.topbar/2-l,text="╳",tags=("Win"+str(c),"Win"))
            pr.create_text(c.x+c.dx-c.topbar*1.3*2/2+l,c.y+c.topbar/2-l-3,text="□",font="Arial 20",tags=("Win"+str(c),"Win"))
        c.app.draw()

    def __init__(c,app) -> None:
        for i in Window._reg:
            i.infocus=False
        c.updated=False
        c.infocus=True
        c.rx=0
        c.ry=0
        c.fadetick=0 # 0 - 9 (väčšie je viac živé)
        c.fading=c.faspeed
        c.paused=False
        c.clicking=False
        c.moving=False
        c.maximised=False
        c.normalised=True
        c.resizing=""
        c.app=app([str(c),"App"+str(c)],c)
        c.app:WindowedApp
        c.x,c.y=c.app.placement
        c.y-=c.topbar
        c.dx,c.dy=c.app.dimensions
        c.dy+=c.topbar
        c.prevdim=c.x,c.y,c.dx,c.dy
        l=True
        ll=time()
        while l:
            l=False
            for i in Window._reg:
                if i.x==c.x and i.y==c.y:
                    l=True
                    c.x+=c.startoffset[0]
                    c.y+=c.startoffset[1]
                    if c.y+c.dy/2>pr.winfo_height():
                        c.y=0
                    if c.x+c.dx/2>pr.winfo_width():
                        c.x=0
                    break
            if time()>ll+1:
                c.x=randint(0,pr.winfo_width()-c.dx/2)
                c.y=randint(0,pr.winfo_height()-c.dy/2)
            if time()>ll+3:
                l=False
                break
        c.resizable=c.app.resizable
        c.smallest=c.app.smallest
        c.app.moved(c.x,c.y+c.topbar,c.dx,c.dy-c.topbar)
        Window._reg.insert(0,c)
        c.mask=smajlotkgui05.Mask(c.x,c.y,c.x+c.dx,c.y+c.dy,len(Window._reg))
        c.draw()

##############################################################

class WindowedApp:
    label="An App"
    deletable=True
    resizable=True
    placement=(500,500)
    dimensions=(400,300)
    smallest=(100,50)
    def icon(c,x,y,tags):
        pr.create_text(x,y,text="A",font="Consolas 25",tags=tags)
    def update(c,clicking,hover,v:Window,t):
        for i in c.guielements:
            pr.tag_raise("stkgui"+str(i),"Win"+str(v))
            i.layer=v.mask.layer
            if v.fading<0:
                i.deactivate()
                if v.fadetick<0:
                    i.forget()
    def draw(c):
        for i in c.guielements:
            i.draw()
        pr.tag_raise("App"+str(c.win),"Win"+str(c.win))
    def click(c,rx,ry):
        c.rx=rx
        c.ry=ry
    def moved(c,x,y,dx,dy):
        #rx,ry,rdx,rdy=x-c.x,y-c.y,dx-c.dx,dy-c.dy
        px,py,pdx,pdy=c.x,c.y,c.dx,c.dy
        c.x=x
        c.y=y
        c.dx=dx
        c.dy=dy
        for i in c.guielements:
            pgx,pgy=i.x,i.y
            i.x=(i.x-px)/pdx*dx+x
            i.y=(i.y-py)/pdy*dy+y
            i.mx+=i.x-pgx
            i.my+=i.y-pgy
            #i.draw()
            
    def __init__(c,tags,window:Window) -> None:
        c.x,c.y=c.placement
        c.dx,c.dy=c.dimensions
        c.rx=0
        c.ry=0
        c.tags=tags
        c.win=window
        c.guielements:list[smajlotkgui05.Button]=[]


class appdrawer(WindowedApp):
    label="App Drawer"
    deletable=False
    smallest=0,0
    
    def moved(c, x, y, dx, dy):
        super().moved(x, y, dx, dy)
        c.draw()
    
    def update(c,clicking,hover:tuple,v:Window,t):
        c.lastclick+=t
        if "1" in guii.sclick and not("1" in guii.spclick) and v.infocus:
            if c.lastclick<0.5:
                c.lastclick=100
                x=0
                y=1
                for i in apps:
                    x+=1
                    if x*c.scale>c.dx-10:
                        x=1
                        y+=1.5
                    if x*c.scale+c.scale/2>hover[0]>x*c.scale-c.scale/2 and y*c.scale+c.scale/2>hover[1]>y*c.scale-c.scale/2:
                        Window(app=i)
                        break
            else:
                c.lastclick=0

    def click(c, rx, ry):
        super().click(rx,ry)
        c.draw()

    def draw(c):
        x=0
        y=1
        pr.delete(str(c))
        for i in apps:
            x+=1
            if x*c.scale>c.dx-10:
                x=1
                y+=1.5
            if x*c.scale+c.scale/2>c.rx>x*c.scale-c.scale/2 and y*c.scale+c.scale/2>c.ry>y*c.scale-c.scale/2:
                pr.create_rectangle(c.x+x*c.scale+c.scale/2,c.y+y*c.scale-c.scale/2,c.x+x*c.scale-c.scale/2,c.y+y*c.scale+c.scale/2,fill="blue",tags=c.tags+[str(c)])
            pr.create_text(c.x+x*c.scale,c.y+y*c.scale+c.scale/2+len(splitter(i.label,7).splitlines())*5,text=splitter(i.label,7),font="Consolas 6",tags=c.tags+[str(c)])
            i.icon(i,c.x+x*c.scale,c.y+y*c.scale,c.tags+[str(c)])

    def __init__(c,tags,window):
        super().__init__(tags,window)
        c.scale=50
        c.lastclick=100

class msg(WindowedApp):
    dimensions=200,100
    def draw(c):
        super().draw()
        pr.delete(str(c))
        if c.msglvl==1:
            pr.create_oval(c.x+10,c.y+10,c.x+30,c.y+30,fill="blue",tags=c.tags+[str(c)])
            pr.create_text(c.x+50,c.y+10,text=c.text)
        if c.msglvl==3:
            pr.create_oval(c.x+10,c.y+10,c.x+50,c.y+50,fill="red",tags=c.tags+[str(c)])
            pr.create_text(c.x+30,c.y+30,text="X",fill="white",font="Arial 15",tags=c.tags+[str(c)])
            pr.create_text(c.x+130,c.y+30,text=c.text,tags=c.tags+[str(c)])
    def __init__(c, tags, window: Window) -> None:
        super().__init__(tags, window)
        c.label=""
        c.text=""
        c.msglvl=0


def splitter(string:str,maxline:int):
    r=""
    for i in range(len(string)):
        '''if (i+1)%maxline==0:
            r+="\n"'''
        if string[i]==" ":
            r+="\n"
        else:
            r+=string[i]
    return r

def spliter(string:str,maxline:int):
    r=""
    for i in string.split(" "):
        4

def sorthelp(s:Window):
    if s.fading<0:
        return 2
    return int(s.clicking)

def focused():
    "Returns instance of a focused window. If no focused windows are present, returns None."
    for i in Window._reg:
        if i.infocus:
            return i
        return
