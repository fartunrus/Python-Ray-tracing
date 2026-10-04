import time, sys, math
from dataclasses import dataclass
from multiprocessing import Process



@dataclass
class Vector2D:
    x : float=0
    y : float=0
    def __str__(self):
        return "x: "+str(self.x)+"; y: "+str(self.y)
    def __format__(self):
        return "Vector2D"
    def __add__(self, other): return Vector2D(self.x+other.x, self.y+other.y) if type(other)==Vector2D else Vector2D(self.x+other, self.y+other)
    def __sub__(self, other): return Vector2D(self.x-other.x, self.y-other.y) if type(other)==Vector2D else Vector2D(self.x-other, self.y-other)
    def __mul__(self, other): return Vector2D(self.x*other.x, self.y*other.y) if type(other)==Vector2D else Vector2D(self.x*other, self.y*other)
    def __truediv__(self, other): return Vector2D(self.x/other.x, self.y/other.y) if type(other)==Vector2D else Vector2D(self.x/other, self.y/other)
    '''def __lt__(self, other): return True if (self.x<other.x and self.y<other.y) else False
    def __le__(self, other): return True if (self.x<=other.x and self.y<=other.y) else False
    def __eq__(self, other): return True if (self.x==other.x and self.y==other.y) else False
    def __ne__(self, other): return True if (self.x!=other.x and self.y!=other.y) else False
    def __gt__(self, other): return True if (self.x>other.x and self.y>other.y) else False
    def __ge__(self, other): return True if (self.x>=other.x and self.y>=other.y) else False
    def __bool__(self): return True if self.x!=0 and self.y!=0 else False'''

@dataclass
class Vector3D:
    x : float=0
    y : float=0
    z : float=0
    def __str__(self):
        return "x: "+str(self.x)+"; y: "+str(self.y)+"; z: "+str(self.z)
    def __format__(self):
        return "Vector3D"
    def __add__(self, other): return Vector3D(self.x+other.x, self.y+other.y, self.z+other.z) if type(other)==Vector3D else Vector3D(self.x+other, self.y+other, self.z+other)
    def __sub__(self, other): return Vector3D(self.x-other.x, self.y-other.y, self.z-other.z) if type(other)==Vector3D else Vector3D(self.x-other, self.y-other, self.z-other)
    def __mul__(self, other): return Vector3D(self.x*other.x, self.y*other.y, self.z*other.z) if type(other)==Vector3D else Vector3D(self.x*other, self.y*other, self.z*other)
    def __truediv__(self, other): return Vector3D(self.x/other.x, self.y/other.y, self.z/other.z) if type(other)==Vector3D else Vector3D(self.x/other, self.y/other, self.z/other)
    def __le__(self, other):
        if type(other)==Vector3D:
            return True if self.z<=other.z else False
        return True
    def __ge__(self, other):
        if type(other)==Vector3D:
            return True if other.z<=self.z else False
        return True
    '''def __lt__(self, other): return True if (self.x<other.x and self.y<other.y and self.z<other.z) else False
    def __eq__(self, other): return True if (self.x==other.x and self.y==other.y and self.z==other.z) else False
    def __ne__(self, other): return True if (self.x!=other.x and self.y!=other.y and self.z!=other.z) else False
    def __gt__(self, other): return True if (self.x>other.x and self.y>other.y and self.z>other.z) else False
    def __bool__(self): return True if self.x!=0 and self.y!=0 and self.z!=0 else False  '''
    
def pos(n): return n*(-1) if n<0 else n
def norm(vec): 
    a=length(vec)
    if type(vec)==Vector2D:
        if a!=0:
            return Vector2D(vec.x/a, vec.y/a)
        else: return Vector2D(1,1)
    elif a!=0:
            return Vector3D(vec.x/a, vec.y/a, vec.z/a)
    else: return Vector3D(1,1,1)

def dot(vec1, vec2): return vec1.x*vec2.x+vec1.y*vec2.y+(vec1.z*vec2.z if type(vec1)==Vector3D and type(vec2)==Vector3D else 0)

def length(v): return (v.x**2+v.y**2+(v.z**2 if type(v)==Vector3D else 0))**0.5

def clamp(n, m, x): return max(min(n, x), m)

def cos(vec1, vec2):
    a=length(vec1)*length(vec2)
    if a!=0: return dot(vec1, vec2)/a
    return 1

def sphere(camera, sphp, radius):
    camdis=Vector3D(camera.x, camera.y, camera.z)
    if sphp.z>camdis.z:
        camdis.z+=sphp.z+1
        camdis.x*=camdis.z
        camdis.y*=camdis.z
        a=(radius**2-(camdis.x-sphp.x)**2-(camdis.y-sphp.y)**2)
        if a>=0:
            return Vector3D(camdis.x, camdis.y, camdis.z-1-a**0.5)
    return -1

def sphereLight(intersec, sphp, light):
    a=cos(intersec-sphp, light-sphp)
    return a

screen_x=220
screen_y=49
screen_ratio=screen_x/screen_y
sym_ratio=9/17
sleep=0.00001
frames=50000
gradient=" .,|+i128FPB@"
gradient_size=len(gradient)
radius=0.8
for t in range(frames):
    text=""
    for i in range(screen_y):
        sys.stdout.write("\033[A")
        for j in range(screen_x):
            symb="-"
            uv=Vector2D(j, i)/Vector2D(screen_x, screen_y) * 2 - 1
            uv.x*=screen_ratio*sym_ratio
            cd=Vector3D(uv.x, uv.y, -1)
            if(uv.y<0.3): symb=" "
            light=Vector3D(1, 0, 0)
            light.y+=math.sin(t*0.07)*3
            light.x+=math.sin(t*0.05)*6
            light.z+=math.sin(t*0.05)*2
            sphp1=Vector3D(0,0,2)
            sphp1.z+=pos(math.cos(t*0.03))
            sphp1.x+=math.sin(t*0.09)
            sphp1.y+=math.cos(t*0.04)
            sphp=sphp1
            intersec=sphere(cd, sphp, radius)
            sphp2=Vector3D(0,0,3)
            sphp2.z+=pos(math.sin(t*0.024))
            sphp2.x+=math.sin(t*0.04)
            sphp2.y+=math.cos(t*0.07)
            intersec1=sphere(cd,sphp2,radius)
            if(type(intersec)!=int):
                color=clamp(sphereLight(intersec, sphp, light),0,1)
                symb=gradient[int(color*gradient_size)]
            text+=symb
        text+="\n"
    text+="by Fartunruss. tg @Fartunruss"
    sys.stdout.write("\033[A")
    sys.stdout.write(text)
    time.sleep(sleep)
