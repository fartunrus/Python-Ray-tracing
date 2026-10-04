import time, sys, math
from dataclasses import dataclass
import multiprocessing



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

def sphere(camera, spherepos, radius):
    camdis=Vector3D(camera.x, camera.y, camera.z)
    if spherepos.z>camdis.z:
        camdis.z+=spherepos.z+1
        camdis.x*=camdis.z
        camdis.y*=camdis.z
        a=(radius**2-(camdis.x-spherepos.x)**2-(camdis.y-spherepos.y)**2)
        if a>=0:
            return Vector3D(camdis.x, camdis.y, camdis.z-1-a**0.5)
    return -1

def sphereLight(intersection, light, sphp):
    a=cos(intersection-sphp, light-sphp)#intersec=Vector3D(x*z,y*z,cd.z+1+sphp.z)
    return a

def nearest(vec1, vec2):
    if(type(vec1)!=int):
        vec=vec1
        if(type(vec2)!=int):
            if(type(vec)!=int):
                if(vec>=vec2):
                    return 1
                else:
                    return 0
            else:
                return 1
        else:
            return 0
    else: return 1
def createsphere(x,y,z,zz,zm,xx,xm,yy,ym,radius,cd,intersect, intersecold, sphpold):
    sphp=Vector3D(x,y,z)
    sphp.z+=pos(math.cos(t*zz)*zm)
    sphp.x+=math.sin(t*xx)*xm
    sphp.y+=math.sin(t*yy)*ym
    intersec=sphere(cd, sphp, radius)
    if(nearest(intersect, intersec)):
        return [intersec, sphp]
    else:
        return [intersecold, sphpold]

screen_x=220
screen_y=49
screen_ratio=screen_x/screen_y
sym_ratio=9/17
sleep=0.00001
frames=50000
gradient=" .,|+i128FP@B"
gradient_size=len(gradient)
radius=0.8
with multiprocessing.Pool(8) as pool:
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
                #light.y+=math.sin(t*0.07)*3
                #light.x+=math.sin(t*0.05)*6
                #light.z+=math.sin(t*0.05)*2
                g=createsphere(0,1,1,0.04,2,0.06,1.3,0.1,1,radius,cd,0,0,0)
                intersec=g[0]
                sphp=g[1]
                intersecold=intersec
                sphpold=sphp
                g=createsphere(1,2,2,0.06,3,0.03,1.8,0.1,0.5,radius,cd,intersec,intersecold,sphpold)
                intersec=g[0]
                sphp=g[1]
                intersecold=intersec
                sphpold=sphp
                g=createsphere(1,1,2,0.1,2,0.04,1.3,0.06,0.7,radius,cd,intersec,intersecold,sphpold)
                intersec=g[0]
                sphp=g[1]
                intersecold=intersec
                sphpold=sphp
                if(type(intersec)!=int):
                    color=clamp(sphereLight(intersec, light, sphp),0,1)
                    symb=gradient[int(color*gradient_size)]
                text+=symb
            text+="\n"
        text+="by Fartunruss. tg @Fartunruss"
        sys.stdout.write("\033[A")
        sys.stdout.write(text)
        time.sleep(sleep)
