from tkinter import *


def rgb(rgb):
  rgb=list(rgb)
  for i in range(len(rgb)):
    if rgb[i]>255:
      rgb[i]=255
    elif rgb[i]<0:
      rgb[i]=0
  rgbb=(rgb[0],rgb[1],rgb[2])
  return "#"+'%02x%02x%02x' % rgbb

class SHStickEvent:
    def __init__(c,act,dir) -> None:
        c.action=act
        c.direction=dir

class SHStick:
    def _upp(c,s):
        c.events.append(["up","pressed"])
    def _downp(c,s):
        c.events.append(["down","pressed"])
    def _leftp(c,s):
        c.events.append(["left","pressed"])
    def _rightp(c,s):
        c.events.append(["right","pressed"])
    def _middlep(c,s):
        c.events.append(["middle","pressed"])
        
    def get_events(c):
        r=[]
        for i in range(len(c.events)):
            r.append(SHStickEvent(c.events[i][1],c.events[i][0]))
        c.events=[]
        return r
    
    def __init__(c) -> None:
        c.events=[]

class SenseHat:
    def refresh(c):
        c.pr.delete("pixels")
        for i in range(len(c.array)):
            for o in range(len(c.array[i])):
                c.pr.create_rectangle(i*20+10,o*20+10,(i+1)*20+10,(o+1)*20+10,fill=rgb(c.array[i][o]),tags="pixels")
        c.tk.update()

    def set_pixels(c,pixel_list):
        row=-1
        for i in range(len(pixel_list)):
            if i%8==0:
                row+=1
            c.array[i%8][row]=pixel_list[i]
        c.refresh()

    def set_pixel(c,x,y,*pixel):
        if len(pixel)==1:
            c.array[x][y]=pixel[0]
        elif len(pixel)==3:
            c.array[x][y]=pixel
        c.refresh()

    def clear(c,*colour):
        c.array=[]
        for i in range(8):
            c.array.append([])
            for o in range(8):
                if len(colour)==1:
                    c.array[i].append(colour[0])
                elif len(colour)==3:
                    c.array[i].append(colour)
        c.refresh()

    def __init__(c) -> None:
        c.tk=Tk()
        c.pr=Canvas()
        c.pr.grid()
        c.clear([0,0,0])
        c.stick=SHStick()
        c.pr.bind_all("<KeyPress-Up>",c.stick._upp)
        c.pr.bind_all("<KeyPress-Down>",c.stick._downp)
        c.pr.bind_all("<KeyPress-Right>",c.stick._rightp)
        c.pr.bind_all("<KeyPress-Left>",c.stick._leftp)
        c.pr.bind_all("<KeyPress-Return>",c.stick._middlep)
        
