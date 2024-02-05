from time import *
from tkinter import *
from random import *
import smajlotkgui04

guii=None
pr=None
apps=()

def sor(a:bool,b:bool):
    return a or b
def sand(a:bool,b:bool):
    return a and b
def setup(can:Canvas,smtkgui:smajlotkgui04,*applications):
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
    def updall(t):
        global test,sphover
        t/=0.008333333333333333333333
        Window._reg.sort(key=sorthelp,reverse=True)
        Window.clicked=False
        for i in Window._reg:
            i:Window
            try:
                if i.infocus:
                    pr.tag_raise("Win"+str(i))
                    pr.tag_raise("App"+str(i),"Win"+str(i))
                i.update(t)
            except Exception as e:
                p=Window(msg)
                p.app.label="An error occured"
                p.app.text=e.args[0]
                p.app.msglvl=3
                i.paused=True
        sphover=guii.shover

    def update(c,t,f=False):
        c.mouse()
        c.fadetick+=c.fading*t
        if not c.paused:
            c.app.update(c.clicking,(guii.shover[0]-c.x,guii.shover[1]-c.y-c.topbar),c,t)
        if c.fadetick>9:
            c.fading=0
            c.fadetick=9
            f=True
        elif c.fadetick<0:
            Window._reg.remove(c)
            pr.delete("Win"+str(c))
            return
        elif c.fading!=0:
            f=True
        if c.maximised:
            if round(c.x)!=0 or round(c.y)!=0 or round(c.dx)!=pr.winfo_width()-4 or round(c.dy)!=pr.winfo_height()-4:
                c.normalised=False
                f=True
                c.x/=2**t
                c.y/=2**t
                c.dx=(c.dx-pr.winfo_width())/(2**t)+pr.winfo_width()-3
                c.dy=(c.dy-pr.winfo_height())/(2**t)+pr.winfo_height()-3
                c.app.moved(c.x,c.y+c.topbar,c.dx,c.dy-c.topbar)
            elif c.x!=0:
                c.x=0
                c.y=0
                c.dx=pr.winfo_width()
                c.dy=pr.winfo_height()
        else:
            if sand(not c.normalised,round(c.x)!=c.prevdim[0] or round(c.y)!=c.prevdim[1] or round(c.dx)!=c.prevdim[2] or round(c.dy)!=c.prevdim[3]):
                f=True
                c.x=(c.x-c.prevdim[0])/(2**t)+c.prevdim[0]
                c.y=(c.y-c.prevdim[1])/(2**t)+c.prevdim[1]
                c.dx=(c.dx-c.prevdim[2])/(2**t)+c.prevdim[2]
                c.dy=(c.dy-c.prevdim[3])/(2**t)+c.prevdim[3]
                c.app.moved(c.x,c.y+c.topbar,c.dx,c.dy-c.topbar)
            else:
                c.normalised=True
        if f:
            c.draw()
    
    def mouse(c):
        if c.clicking or c.resizing!="":
            c.click()
        if guii.sdouble and c.fading==0 and not Window.clicked:
            if c.dx+c.x>=guii.shover[0]>=c.x:
                if c.dy+c.y>=guii.shover[1]>=c.y:
                    Window.clicked=True
                    c.click()
                    if c.ry<c.topbar:
                        if not c.maximised:
                            c.prevdim=round(c.x),round(c.y),round(c.dx),round(c.dy)
                        c.maximised=not c.maximised
                        c.app.moved(c.x,c.y+c.topbar,c.dx,c.dy-c.topbar)
                        c.draw()
                    
        if guii.sclick and not(Window.clicked):
            if not guii.spclick:
                if c.dx+c.x>guii.shover[0]>c.x:
                    if c.dy+c.y>guii.shover[1]>c.y:
                        c.click()
                        if c.ry>c.topbar:
                            c.app.click(c.rx,c.ry-c.topbar)
                        elif c.rx>c.dx-c.topbar and c.deletable:
                            c.fading=-c.faspeed
                        elif c.rx>c.dx-c.topbar*2 and c.deletable:
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
        if guii.sclick and not(guii.spclick) and not(c.clicking):
            c.infocus=False

    def click(c):
        for i in Window._reg:
            i.infocus=False
        c.infocus=True
        if c.moving:
            if not(c.normalised) or c.maximised:
                c.maximised=False
                c.prevdim=guii.shover[0]-c.prevdim[2]/2,guii.shover[1]-c.topbar/2,c.prevdim[2],c.prevdim[3]
            else:
                #pr.move("Win"+str(c),guii.shover[0]-(c.rx+c.x),guii.shover[1]-(c.ry+c.y))
                #pr.move("Win"+str(c),guii.shover[0]-(c.rx+c.x)+(guii.shover[0]-sphover[0]),guii.shover[1]-(c.ry+c.y)+(guii.shover[1]-sphover[1]))
                c.x=guii.shover[0]-c.rx
                c.y=guii.shover[1]-c.ry
                #pr.moveto("Win"+str(c),c.x-1+guii.shover[0]-sphover[0],c.y-1+guii.shover[1]-sphover[1])
                pr.moveto("Win"+str(c),c.x-1,c.y-1)
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
        pr.delete("Win"+str(c))
        for i in guii.trasluc(int(c.fadetick)):
            pr.create_rectangle(c.x+18-c.fadetick*2,c.y+18-c.fadetick*2,c.dx+c.x-18+c.fadetick*2,c.dy+c.y-18+c.fadetick*2,fill="white",tags=("Win"+str(c),"Win"),stipple=i,outlinestipple=i)
        pr.create_line(c.x+18-c.fadetick*2,c.y+c.topbar+18-c.fadetick*2,c.x+c.dx-18+c.fadetick*2,c.y+c.topbar+18-c.fadetick*2,tags=("Win"+str(c),"Win"))
        pr.create_text(c.x+c.dx/2,c.y+c.topbar/2+18-c.fadetick*2,text=c.app.label,tags=("Win"+str(c),"Win"))
        if c.deletable:
            pr.create_text(c.x+c.dx-c.topbar*1.3/2-18+c.fadetick*2,c.y+c.topbar/2+18-c.fadetick*2,text="╳",tags=("Win"+str(c),"Win"))
            pr.create_text(c.x+c.dx-c.topbar*1.3*2/2-18+c.fadetick*2,c.y+c.topbar/2+18-c.fadetick*2-3,text="□",font="Arial 20",tags=("Win"+str(c),"Win"))
        c.app.draw()
        pr.tag_raise("App"+str(c),"Win"+str(c))

    def __init__(c,app) -> None:
        c.topbar=30
        for i in Window._reg:
            i.infocus=False
        c.infocus=True
        c.rx=0
        c.ry=0
        c.fadetick=0
        c.fading=c.faspeed
        c.paused=False
        c.clicking=False
        c.moving=False
        c.maximised=False
        c.normalised=True
        c.resizing=""
        c.app=app(["Win"+str(c),str(c),"App"+str(c)],c)
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
                    c.x+=40
                    c.y+=40
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
        c.deletable=c.app.deletable
        c.resizable=c.app.resizable
        c.smallest=c.app.smallest
        c.app.moved(c.x,c.y+c.topbar,c.dx,c.dy-c.topbar)
        Window._reg.append(c)
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
    def update(c,clicking,hover,v,t):
        pass
    def draw(c):
        pr.tag_raise(c.tags[2])
    def click(c,rx,ry):
        c.rx=rx
        c.ry=ry
    def moved(c,x,y,dx,dy):
        c.x=x
        c.y=y
        c.dx=dx
        c.dy=dy
    def __init__(c,tags,window:Window) -> None:
        c.x,c.y=c.placement
        c.dx,c.dy=c.dimensions
        c.rx=0
        c.ry=0
        c.tags=tags
        c.win=window


class appdrawer(WindowedApp):
    label="App Drawer"
    deletable=False
    smallest=0,0
    
    def moved(c, x, y, dx, dy):
        super().moved(x, y, dx, dy)
        c.draw()
    
    def update(c,clicking,hover:tuple,v:Window,t):
        if v.fadetick>9:
            c.draw()
        if guii.sdouble and v is Window._reg[0]:
            x=0
            y=1
            for i in apps:
                x+=1
                if x*c.scale>c.dx-10:
                    x=1
                    y+=1
                if x*c.scale+c.scale/2>hover[0]>x*c.scale-c.scale/2 and y*c.scale+c.scale/2>hover[1]>y*c.scale-c.scale/2:
                    Window(app=i)
                    break

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
                y+=1
            if x*c.scale+c.scale/2>c.rx>x*c.scale-c.scale/2 and y*c.scale+c.scale/2>c.ry>y*c.scale-c.scale/2:
                pr.create_rectangle(c.x+x*c.scale+c.scale/2,c.y+y*c.scale-c.scale/2,c.x+x*c.scale-c.scale/2,c.y+y*c.scale+c.scale/2,fill="blue",tags=c.tags+[str(c)])
            pr.create_text(c.x+x*c.scale,c.y+y*c.scale+c.scale/2+len(splitter(i.label,7).splitlines())*5,text=splitter(i.label,7),font="Consolas 6",tags=c.tags+[str(c)])
            i.icon(i,c.x+x*c.scale,c.y+y*c.scale,c.tags+[str(c)])

    def __init__(c,tags,window):
        super().__init__(tags,window)
        c.scale=50

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
    if s.fading>0:
        return 2
    return int(s.clicking)

def focused():
    "Returns instance of a focused window. If no focused windows are present, returns None."
    for i in Window._reg:
        if i.infocus:
            return i
        return
