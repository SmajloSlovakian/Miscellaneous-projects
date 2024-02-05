import math
from typing import Optional

class bunka:
    stav:int=0 # 0: priestor, 1: prekážka, 2: začiatok, 3: koniec
    x:int
    y:int
    camefrom:"bunka"
    gscore:float=math.inf
    fscore:float=math.inf
    def __init__(c,x:int,y:int) -> None:
        c.x=x
        c.y=y
        c.camefrom=c
    def __str__(c) -> str:
        return f"{c.x},{c.y},{c.stav}"

class mriežka:
    def __str__(c) -> str:
        ret:str
        for i in c.bunky:
            ret+="\n"
            for o in i:
                if(o.stav==0):
                    ret+=" "
                elif(o.stav==1):
                    ret+="#"
                elif(o.stav==2):
                    ret+="+"
                elif(o.stav==3):
                    ret+="O"
        return ret

    def __init__(c,x:int,y:int) -> None:
        c.xx:int=x
        c.yy:int=y
        c.bunky:list[list[bunka]]=[]
        for i in range(x):
            c.bunky.append([])
            for o in range(y):
                c.bunky[i].append(bunka(i,o))
                
    def neighs(c,d) -> list[bunka]:
        ret:list[bunka]=[]
        if(d.x+1<c.xx):
            ret.append(c.bunky[d.x+1][d.y])
        if(d.y+1<c.yy):
            ret.append(c.bunky[d.x][d.y+1])
        if(d.x-1>=0):
            ret.append(c.bunky[d.x-1][d.y])
        if(d.y-1>=0):
            ret.append(c.bunky[d.x][d.y-1])
        return ret

    def find(c) -> list[bunka]:
        zač:list[bunka]=[]
        fin:list[bunka]=[]
        for i in c.bunky:
            for o in i:
                if(o.stav==3):
                    fin.append(o)
                elif(o.stav==2):
                    zač.append(o)
        ret:list[list[bunka]]=[]
        for i in zač:
            for o in fin:
                ret.append(c.makeone(i,o))
        rett:list[bunka]=[]
        for i in ret:
            if(i!=None):
                if(rett==[] or len(rett)>len(i)):
                    rett=i
        return rett

    def makeone(c,zač:bunka,fin:bunka) -> Optional[list[bunka]]:
        bun:list[bunka]=[]
        if(zač==None or fin==None):
            return None
        for ú in c.bunky:
            for ô in ú:
                ô.gscore=math.inf
                ô.fscore=math.inf
                ô.camefrom=ô
        zač.gscore=0
        zač.fscore=abs(zač.x-fin.x)+abs(zač.y-fin.y)
        bun.append(zač)
        
        while(len(bun)>0):
            cur:Optional[bunka]=None
            curr:float=math.inf
            for i in bun:
                if(i.fscore<curr):
                    curr=i.fscore
                    cur=i
            if(cur==fin):
                lo:bunka=cur
                le:list[bunka]=[]
                while True:
                    le.append(lo)
                    if(lo.camefrom==lo):
                        return le
                    else:
                        lo=lo.camefrom
            bun.remove(cur)
            for i in c.neighs(cur):
                tent:float=cur.gscore+1
                if(tent<i.gscore and i.stav!=1):
                    i.camefrom=cur
                    i.gscore=tent
                    i.fscore=tent+abs(i.x-fin.x)+abs(i.y-fin.y)
                    if(i not in bun):
                        bun.append(i)
        return None

def debugstring(lis:list[bunka]):
    ret=""
    for i in lis:
        ret+=f"{i.x},{i.y}"

