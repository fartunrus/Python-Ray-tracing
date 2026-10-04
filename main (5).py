import time, sys, math
from dataclasses import dataclass



@dataclass
class Vector2D:
    x : float=0
    y : float=0
    def __str__(self):
        return "x: "+str(self.x)+"; y: "+str(self.y)
    def __format__(self):
        return "Vector2D"
    def __lt__(self, other): return True if (self.x<other.x and self.y<other.y) else False
    def __le__(self, other): return True if (self.x<=other.x and self.y<=other.y) else False
    def __eq__(self, other): return True if (self.x==other.x and self.y==other.y) else False
    def __ne__(self, other): return True if (self.x!=other.x and self.y!=other.y) else False
    def __gt__(self, other): return True if (self.x>other.x and self.y>other.y) else False
    def __ge__(self, other): return True if (self.x>=other.x and self.y>=other.y) else False
    def __bool__(self): return True if self.x!=0 and self.y!=0 else False
    def __add__(self, other): return Vector2D(self.x+other.x, self.y+other.y) if type(other)==Vector2D else Vector2D(self.x+other, self.y+other)
    def __sub__(self, other): return Vector2D(self.x-other.x, self.y-other.y) if type(other)==Vector2D else Vector2D(self.x-other, self.y-other)
    def __mul__(self, other): return Vector2D(self.x*other.x, self.y*other.y) if type(other)==Vector2D else Vector2D(self.x*other, self.y*other)
    def __truediv__(self, other): return Vector2D(self.x/other.x, self.y/other.y) if type(other)==Vector2D else Vector2D(self.x/other, self.y/other)

@dataclass
class Vector3D:
    x : float=0
    y : float=0
    z : float=0
    def __str__(self):
        return "x: "+str(self.x)+"; y: "+str(self.y)+"; z: "+str(self.z)
    def __format__(self):
        return "Vector3D"
    def __lt__(self, other): return True if (self.x<other.x and self.y<other.y and self.z<other.z) else False
    def __le__(self, other): return True if (self.x<=other.x and self.y<=other.y and self.z<=other.z) else False
    def __eq__(self, other): return True if (self.x==other.x and self.y==other.y and self.z==other.z) else False
    def __ne__(self, other): return True if (self.x!=other.x and self.y!=other.y and self.z!=other.z) else False
    def __gt__(self, other): return True if (self.x>other.x and self.y>other.y and self.z>other.z) else False
    def __ge__(self, other): return True if (self.x>=other.x and self.y>=other.y and self.z>=other.z) else False
    def __bool__(self): return True if self.x!=0 and self.y!=0 and self.z!=0 else False
    def __add__(self, other): return Vector3D(self.x+other.x, self.y+other.y, self.z+other.z) if type(other)==Vector3D else Vector3D(self.x+other, self.y+other, self.z+other)
    def __sub__(self, other): return Vector3D(self.x-other.x, self.y-other.y, self.z-other.z) if type(other)==Vector3D else Vector3D(self.x-other, self.y-other, self.z-other)
    def __mul__(self, other): return Vector3D(self.x*other.x, self.y*other.y, self.z*other.z) if type(other)==Vector3D else Vector3D(self.x*other, self.y*other, self.z*other)
    def __truediv__(self, other): return Vector3D(self.x/other.x, self.y/other.y, self.z/other.z) if type(other)==Vector3D else Vector3D(self.x/other, self.y/other, self.z/other)        
    
def pos(n): return n*(-1) if n<0 else n
def norm(vec): 
    if type(vec)==Vector2D: 
        if length(vec)!=0: 
            return Vector2D(vec.x/length(vec), vec.y/length(vec))
        else: return Vector2D(1,1)
    elif length(vec)!=0:
            return Vector3D(vec.x/length(vec), vec.y/length(vec), vec.z/length(vec))
    else: return Vector3D(1,1,1)
def dot(vec1, vec2): return vec1.x*vec2.x+vec1.y*vec2.y+(vec1.z*vec2.z if type(vec1)==Vector3D and type(vec2)==Vector3D else 0)
def length(v): return (v.x**2+v.y**2+(v.z**2 if type(v)==Vector3D else 0))**0.5
def clamp(n, m, x): return max(min(n, x), m)
def cos(vec1, vec2):
    if(length(vec1)*length(vec2))!=0: return (dot(vec1, vec2)/(length(vec1)*length(vec2)))
    else: return 1

def sphere(camdis, spherepos, radius):
    camdis=cd
    if(camdis.z+spherepos.z<-1):return Vector2D(-1,-1)
    camdis.z+=spherepos.z
    camdis.x*=(camdis.z+1)
    camdis.y*=(camdis.z+1)
    if((camdis.x-spherepos.x)**2+(camdis.y-spherepos.y)**2<radius**2):
        return Vector2D(camdis.x, camdis.y)
    return Vector2D(-1,-1)

def sphereLight(cd, spherepos, light):
    a=cos(spherepos-cd, light-cd)
    return a

screen_x=220
screen_y=50
screen_ratio=screen_x/screen_y
sym_ratio=9/17
sleep=0.0001
frames=5000
gradient=" .,|+i128FPB@"
gradient_size=len(gradient)-1
radius=0.8
for t in range(frames):
    text=""
    for i in range(screen_y):
        #sys.stdout.write("\033[A")
        for j in range(screen_x):
            symb="-"
            uv=Vector2D(j, i)/Vector2D(screen_x, screen_y) * 2 - 1
            uv.x*=screen_ratio*sym_ratio
            cd=Vector3D(uv.x, uv.y, -1)
            if(uv.y<0.3): symb=" "
            light=Vector3D(0, 0, 0)
            light.y+=math.sin(t*0.07)*3
            sphp=Vector3D(0,0,1)
            sphp.z+=pos(math.cos(t*0.01))
            sphp.x+=math.sin(t*0.03)*2
            sphp.y+=math.cos(t*0.02)
            intersec=sphere(cd, sphp, radius)
            if(intersec!=Vector2D(-1,-1)):
                shade=sphereLight(cd, sphp, light)
                color=-((shade-1)/2)**2
                symb=gradient[int(-color*gradient_size)]
            text+=symb
        text+="\n"
    sys.stdout.write(text)
    time.sleep(sleep)