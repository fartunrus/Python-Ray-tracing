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

def sphere(uv, light, spherepos, radius):
    if(length(Vector3D(uv.x,uv.y,0))**2<radius**2):
        return cos(norm(spherepos)-light, Vector3D(uv.x, uv.y, 0)-light)
    return 0

screen_x=120
screen_y=20
screen_ratio=screen_x/screen_y
sym_ratio=9/17
sleep=0.01
frames=500
gradient=" .,;+i128PG@"
gradient_size=len(gradient)-1
radius=0.8

for t in range(frames):
    text=""
    for i in range(screen_y):
        sys.stdout.write("\033[A")
        for j in range(screen_x):
            uv=Vector2D(j, i)/Vector2D(screen_x, screen_y) * 2 - 1
            uv.x*=screen_ratio*sym_ratio
            #uv+=Vector2D(math.sin(t*0.01), math.cos(t*0.01))*0.3
            light=Vector3D(0, 0, 0)
            spherepos=Vector3D(0,0,0)
            #spherepos.z=math.sin(t*0.01)
            sensitivity=sphere(uv, light, spherepos, radius)
            #if(sensitivity!=0):
                #print(sensitivity)
            text+=gradient[int(sensitivity*gradient_size)]
            #else:text+="-"
        text+="\n"
    sys.stdout.write(text)
    time.sleep(sleep)