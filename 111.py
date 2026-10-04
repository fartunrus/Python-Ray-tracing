import math
#import sys, time
from dataclasses import dataclass
import multiprocessing
from tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk

'''
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
    '''
'''
    def __lt__(self, other): return True if (self.x<other.x and self.y<other.y) else False
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
    def __truediv__(self, other): return Vector3D(self.x/other.x, self.y/other.y, self.z/other.z if other.z>0 else self.z) if type(other)==Vector3D else Vector3D(self.x/other, self.y/other, self.z/other)
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

def clamp(n, m, x): return max(min(n, x), m)
def sign(a): return (0<a) - (a<0)
def step(edge, x): return x>edge
def length(v): return (v.x**2+v.y**2+v.z**2)**0.5
def norm(vec):
    return vec/length(vec) if length(vec)!=0 else Vector3D(1,1,1)
def dot(vec1, vec2): return vec1.x*vec2.x+vec1.y*vec2.y+vec1.z*vec2.z
def absvec(v): return Vector3D(abs(v.x), abs(v.y), abs(v.z))
def signvec(v): return Vector3D(sign(v.x),sign(v.y),sign(v.z))
def stepvec(edge, v): return Vector3D(step(edge.x, v.x),step(edge.y, v.y),step(edge.z, v.z))
def reflect(rd, n): return rd-n*(2*dot(n,rd))

def sphere(camera, spherepos, radius):
    if spherepos.z>camera.z:
        camdis=Vector3D(camera.x, camera.y, spherepos.z-camera.z)
        camdis.x*=camdis.z
        camdis.y*=camdis.z
        a=radius**2-(camdis.x-spherepos.x)**2-(camdis.y-spherepos.y)**2
        if a>=0:
            return Vector3D(camdis.x, camdis.y, camdis.z+camera.z-a**0.5)
    return -1

def nearest(vec1, vec2):
    if(type(vec1)!=int):
        vec=vec1
        if(type(vec2)!=int):
            if(type(vec)!=int):
                if(vec>=vec2):
                    return 1
            else:
                return 1
        else:
            return 0
    else: return 1
def createsphere(x,y,z,zz,zm,xx,xm,yy,ym,radius,cd,intersect, sphpold):
    sphp=Vector3D(x,y,z)
    sphp.z+=abs(math.cos(t*zz)*zm)
    sphp.x+=math.sin(t*xx)*xm
    sphp.y+=math.sin(t*yy)*ym
    intersec=sphere(cd, sphp, radius)
    if(nearest(intersect, intersec)):
        return [intersec, sphp]
    else:
        return [intersect, sphpold]
def plane(cd,intersect,sphpold):
    if(cd.y>0):
        z=1/(cd.y)
        intersec=Vector3D(cd.x*z, -0.5, z)
        if(nearest(intersect, intersec)):
            return[intersec,Vector3D(intersec.x,intersec.y-1,intersec.z)]
    return [intersect, sphpold]
def lightvis(cd,light,intersect,sphpold):
    intersec=sphere(cd, light, 0.2)
    if(nearest(intersect, intersec)):
        return[intersec, light]
    return[intersect, sphpold]

def multiproc(q1,gg):
    imagearr=np.zeros([6,screen_x,3], np.uint8)
    #text=''
    for i in range(gg,gg+6):
        for j in screnarr:
            out_color=(0,0,0)
            #symb="-"
            uv=Vector3D(j, i,0)/Vector3D(screen_x, screen_y,0) * 2 - 1
            uv.x*=screen_ratio#*sym_ratio
            cd=Vector3D(uv.x, uv.y, -1)
            cd.z-=abs(math.sin(t*0.1)*4)
            #cd.x-=abs(math.sin(t*0.1)*1)
            light=Vector3D(0.2, -3, 3)
            light.y+=math.sin(t*0.07)
            light.x+=math.sin(t*0.05)*6
            light.z+=-abs(math.sin(t*0.12)*4)
            g=createsphere(0,1,1,0.04,2,0.06,1.3,0.1,1,radius,cd,0,0)
            g=createsphere(1,2,2,0.06,3,0.03,1.8,0.1,0.5,1,cd,g[0],g[1])
            g=createsphere(1,1,2,0.1,2,0.04,1.3,0.06,0.7,radius,cd,g[0],g[1])
            g=createsphere(1,0.5,1,0.07,1.4,0.06,2,0.02,1.3,1.5,cd,g[0],g[1])
            g=createsphere(-1,1,3,0.03,3.2,0.1,3.2,0.04,2.3,radius,cd,g[0],g[1])
            g=createsphere(-1,0,2.5,0.04,4,0.09,2.5,0.09,3.6,2,cd,g[0],g[1])
            g=createsphere(0,1,3.3,0.02,1.7,0.08,1,0.05,1.8,radius,cd,g[0],g[1])
            g=createsphere(-2,1,2,0.04,1.3,0.1,2.3,0.04,2.7,3,cd,g[0],g[1])
            g=plane(cd,g[0],g[1])
            lighthere=0
            if(light.z>cd.z):
                lightin=sphere(cd,light,0.2)
                if not(nearest(lightin, g[0])):
                    out_color=(255,125,255)
                    lighthere=1
            if(lighthere==0 and type(g[0])!=int):
                color=clamp(cos(g[0]-g[1], light-g[1]),0,1)**4#sphere light=cos
                #symb=gradient[int(color*gradient_size)]
                out_color = (color*255*math.sin(2+color*0.6),color*255*math.sin(3+color*0.1),color*255)
            imagearr[i-gg,j] =out_color
            #text+=symb
            #text+="\n"
    q1.put([int(gg/6),imagearr])

screen_x=700
screen_y=360
screnarr=range(screen_x)
screen_ratio=screen_x/screen_y
#sym_ratio=9/17
sleep=0.00001
frames=50000
gradient=" .,|+i128FP@B"
gradient_size=len(gradient)
radius=0.8
imagearr = np.zeros([screen_y, screen_x, 3], dtype=np.uint8)
imagearr[:,:] = [125, 125, 125]
#img = Image.fromarray(image)
#img.save('teste.png')

root = Tk()     # создаем корневой объект - окно
root.title("3D Graphic")     # устанавливаем заголовок окна
#root.geometry("700x300")    # устанавливаем размеры окна

label = Label(text="tg @Fartunruss") # создаем текстовую метку
label.pack()    # размещаем метку в окне
canvas = Canvas(bg="black", width=screen_x, height=screen_y)
canvas.pack(anchor=CENTER, expand=0)
my_image =  ImageTk.PhotoImage(image=Image.fromarray(imagearr))
#my_image=PhotoImage(file="teste.png")
canvas.create_image(0,0,anchor=NW,image=my_image)
root.update()
#root.mainloop()
if __name__ == '__main__':
    if 1==1:
        with multiprocessing.Pool(processes=120) as pool:
            processes=[]
            imagearr = np.zeros([screen_y,screen_x,3], np.uint8)
            q1 = multiprocessing.Queue()
            for t in range(frames):
                #text=""
                #for i in range(0,screen_y,360):
                #for a in range(24):
                #    sys.stdout.write("\033[A")
                #q1.put(imagearr)
                for a in range(60):
                    processes.append(a)
                    processes[a]= multiprocessing.Process(target=multiproc, args=(q1,a*6))
                for a in range(60):
                    processes[a].start()
                for a in range(60):
                    processes[a].join(sleep)
                rawimage={}
                for a in range(60):
                    b=q1.get()
                    rawimage[b[0]]=b[1]
                for a in range(60):
                    imagearr[a*6:6*(a+1)]=rawimage[a]
                #image[:] = tuple(reversed((255,255,255)))
                #img = Image.fromarray(imagearr)
                #img.save('teste.png')
                my_image=ImageTk.PhotoImage(image=Image.fromarray(np.asarray(imagearr)))
                canvas.create_image(0,0,anchor=NW,image=my_image)
                root.update()
                #text+="by Fartunruss. tg @Fartunruss"
                #sys.stdout.write("\033[A")
                #sys.stdout.write(text)
                #time.sleep(sleep)
