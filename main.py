# Setup Modules ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import pygame as py 
from pygame import gfxdraw as gfx
import time 
import random
import os 
import numpy as np
import math

py.init()
py.font.init()

# Setup Constants ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
WHITE = np.array([255, 255, 255])
BLACK = np.array([0, 0, 0])
RED = np.array([255, 0, 0])
GREEN = np.array([0, 255, 0])
BLUE = np.array([0, 0, 255])
LIGHT_BLUE = np.array([173,216,230])
YELLOW = np.array([255,255,0])
PURPLE = np.array([203, 195, 227])
GRAY = np.array([169,169,169])
DIM_GRAY = np.array([16,16,16])
ORANGE = np.array([255,165,0])
BROWN = np.array([222,184,135])

# Facts https://nssdc.gsfc.nasa.gov/planetary/planetfact.html , https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/ , https://ssd.jpl.nasa.gov/horizons/app.html#/

WIDTH = 1080
HEIGHT = 1080
PADDING = 10
FPS = 60
TIMESKIP = (3.154e+7) * 1/(8*FPS)

G = 6.67430e-11
AU = 1.496e11

global SCALE
SCALE = 200/AU

particles = []

X_AXIS = np.array([1,0,0])
Y_AXIS = np.array([0,1,0])
Z_AXIS = np.array([0,0,1])

WINDOW = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Newtonian Simulator')
CLOCK = py.time.Clock()

# Setup Functions ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def _magnitude(arr) :
    return np.sqrt(np.power(arr[0],2)+np.power(arr[1],2)+np.power(arr[2],2))

def _positionvector(arr_p,arr_s) :
    return arr_s - arr_p

def _unitvector(arr) :
    magnitude = _magnitude(arr)
    return arr * 1/magnitude

def _crossproduct(arr1,arr2) :
    return np.cross(arr1,arr2)

def _dotproduct(arr1,arr2) :
    return np.dot(arr1,arr2)

def _angle(arr1,arr2) :
    return np.arccos(_dotproduct(arr1,arr2)/(_magnitude(arr1)*_magnitude(arr2))) * 180/np.pi

def _force(arr_p,arr_s,mass_p,mass_s) :
    return (
        G * mass_p * mass_s / pow(_magnitude(_positionvector(arr_p,arr_s)),2) * _unitvector(_positionvector(arr_p,arr_s)) 
    )

def _acceleration(arr_p,arr_s,mass_s) : 
    return (
        (G * mass_s) / (pow(_magnitude(_positionvector(arr_p,arr_s)),3)) * _positionvector(arr_p,arr_s)
    )

def _deltatime(prev_time):
    now = time.time()
    dt = now-prev_time
    prev_time = now

    if dt > 0.5 :
        dt = 0.5

    return prev_time,dt

def draw_arrow(surface, colour, start, end,r,angle):

    py.draw.line(surface,colour,start,end,2)

    rotation = np.degrees(np.arctan2(start[1]-end[1], end[0]-start[0]))+90

    py.draw.polygon(surface, WHITE, ((end[0]+r*np.sin(np.radians(rotation)), 
                                            end[1]+r*np.cos(np.radians(rotation))), 
                                            (end[0]+r*np.sin(np.radians(rotation-angle)), 
                                            end[1]+r*np.cos(np.radians(rotation-angle))), 
                                            (end[0]+r*np.sin(np.radians(rotation+angle)), 
                                            end[1]+r*np.cos(np.radians(rotation+angle)))))

def updateBodies(bodies) : # Working as intended , loses accuracy over time.

    for body1 in bodies :

        body1.reset_acceleration()

        for body2 in bodies :
            if _magnitude(_positionvector(body1.position,body2.position)) != 0 :
                body1.add_acceleration(_acceleration(body1.position,body2.position,body2.mass))

        body1.move()

def updateBodiesLeapfrog(bodies): # Working as intended (?) , terrible at bodies close to one another.

    for body1 in bodies : 
                                                                                                            
        body1.reset_force()

        for body2 in bodies :
            if _magnitude(_positionvector(body1.position,body2.position)) != 0 :

                body1.add_force(_force(body1.position,body2.position,body1.mass,body2.mass))

        body1.halfvelocity = body1.velocity + (body1.force/body1.mass) * TIMESKIP / 2

        body1.position = body1.position + body1.halfvelocity * TIMESKIP

        body1.reset_force()

        for body2 in bodies :
            if _magnitude(_positionvector(body1.position,body2.position)) != 0 :

                body1.add_force(_force(body1.position,body2.position,body1.mass,body2.mass))   

        body1.velocity = body1.halfvelocity + (body1.force/body1.mass) * TIMESKIP / 2   

        body1.orbit_points.append((body1.position[0],body1.position[1])) 


def f(t,x,v) :
    return v

def g(t,x,v) :
    return G*M/pow(_magnitude(_positionvector(p1,p2)),3) * _positionvector(p1,p2)

def updateBodiesRungeKutta(bodies) : # Hard to implement

    arr = [0 for i in range(2*len(bodies))] 

    for i,body in enumerate(bodies) :
        length = len(bodies)
        arr[i] = body.position
        arr[i+length] = body.velocity

    arr = np.array(arr).ravel()
    
    t = 0

    for i,body in enumerate(bodies) :

        k1x = f(t,arr[3*i:3*(i+1)],arr[3*i+3*len(bodies):3*(i+1)+3*len(bodies)])
        print(i,body.name)

def updateColor(color) :
    if color[0] < 0 :
        color[0] = 0
    if color[1] < 0 :
        color[1] = 0
    if color[2] < 0 :
        color[2] = 0

def init() :

    sun = Body(YELLOW,2,np.array([-8.974133574359094E-03, -4.482427452346882E-04,  2.127030817970091E-04],dtype=np.float64)*AU,np.array([2.943740906566515E-00, -1.522269030106718E+01,  5.405294312927581E-02],dtype=np.float64),1.98892e30, 'sun', [''], ['mercury','venus','earth','mars','jupiter','saturn','uranus','neptune'])
    mercury = Body(GRAY,1,np.array([2.149048126431211E-01, -3.703275102221233E-01, -5.054911078568054E-02],dtype=np.float64)*AU,np.array([3.194733455939798E+04,  2.760819992651870E+04, -6.726501719165086E+02],dtype=np.float64),3.3e23, 'mercury', ['sun'] , [''])
    venus = Body(ORANGE,1,np.array([3.767586589387518E-01,  6.096285845914635E-01, -1.366913498677996E-02],dtype=np.float64)*AU,np.array([-2.970885187788254E+04,  1.854691206999238E+04,  1.969344555554133E+03],dtype=np.float64),4.8685e24, 'venus', ['sun'],[''])
    earth = Body(LIGHT_BLUE,1,np.array([-9.505921700191389E-01,  3.087952119351821E-01,  1.989011142050173E-04],dtype=np.float64)*AU,np.array([-9.765270895434471E+03, -2.842566374064967E+04,  1.340272026562062E-00],dtype=np.float64),5.9742e24, 'earth', ['sun'] , ['moon'])
    moon = Body(GRAY,1,np.array([-9.516099449755469E-01,  3.112973301473198E-01,  4.330394864078491E-04],dtype=np.float64)*AU,np.array([-1.066377823007508E+04, -2.878353621791489E+04,  2.165227437387784E+01]),7.346e22, 'moon', ['earth'], [''])
    mars = Body(RED,1,np.array([-7.405291211708632E-01,  1.452944259261813E+00,  4.861778406962673E-02],dtype=np.float64)*AU,np.array([-2.072274803097698E+04, -8.848861397338558E+03,  3.233078954361095E+02],dtype=np.float64),6.39e23, 'mars', ['sun'] , [''])
    jupiter = Body(BROWN,1,np.array([4.704772918851717E+00,  1.511365399792853E+00, -1.115289067637071E-01],dtype=np.float64)*AU,np.array([-4.142495775785003E+03,  1.305304733174904E+04,  3.854785819752404E+01],dtype=np.float64),1.898e27, 'jupiter', ['sun'] , [''])
    saturn = Body(BROWN,1,np.array([8.305195501443066E+00, -5.220660638189502E+00, -2.398939811841545E-01],dtype=np.float64)*AU,np.array([4.600536590796957E+03,  8.158326300996555E+03, -3.244831811891196E+02],dtype=np.float64),5.683e26, 'saturn', ['sun'] , [''])
    uranus = Body(BLUE,1,np.array([1.318193324076657E+01,  1.457795067541527E+01, -1.166313290118892E-01],dtype=np.float64)*AU,np.array([-5.100987027758054E+03,  4.250202813282490E+03,  8.207046388370087E+01],dtype=np.float64),8.6811e24, 'uranus', ['sun'] , [''])
    neptune = Body(BLUE,1,np.array([2.976877605000455E+01, -2.750966044048722E+00, -6.294024336722218E-01],dtype=np.float64)*AU,np.array([4.643812712803050E+02,  5.444339754400878E+03, -1.230818583920708E+02],dtype=np.float64),1.02409e26, 'neptune', ['sun'] , ['']) 
    pluto = Body(GRAY,1,np.array([1.634165701841916E+01, -3.059305947768982E+01, -1.453331982012886E+00],dtype=np.float64)*AU,np.array([4.939775926882488E+03,  1.393967470123350E+03, -1.560052632054384E+03],dtype=np.float64),1.02409e26, 'neptune', ['sun'] , [''])
    ceres1 = Body(WHITE,1,np.array([-2.520166209594838E+00,  1.981777425761302E-01,  4.690652595690624E-01],dtype=np.float64)*AU,np.array([-2.087658705414134E+03, -1.918397099983357E+04, -2.209470431651512E+02],dtype=np.float64),9.3835e20, 'ceres', ['sun'] , ['']) 
    
    return [sun,mercury,venus,moon,earth,mars,jupiter,saturn,uranus,neptune,pluto,ceres1] 
    #return [sun,venus]

# Setup Classes -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Body : 

    def __init__(self,color,radius,position,velocity, mass, name, parents, sons) :

        # colors and shape
        self.radius = radius
        self.color = color
        self.orbit_color = np.array([
            self.color[0]-75,
            self.color[1]-75,
            self.color[2]-75
        ])
        updateColor(self.orbit_color)

        # physical properties
        self.position = position
        self.nextposition = np.array([0,0,0])
        self.velocity = velocity
        self.halfvelocity = np.array([0,0,0])
        self.force = np.array([0, 0, 0])
        self.mass = mass
        self.acceleration = np.array([0,0,0])

        # orbits
        self.orbit_points = []

        # family
        self.name = name
        self.parents = parents
        self.sons = sons

    def draw(self, surface, offset) :

        if self.velocity[0] < 0 :
            angle = (np.arctan(self.velocity[1]/self.velocity[0])+np.pi)
        else :
            angle = np.arctan(self.velocity[1]/self.velocity[0])

        L=30

        # draw_arrow(WINDOW, WHITE, (self.position[0]*SCALE+WIDTH/2+offset[0],self.position[1]*SCALE+HEIGHT/2+offset[1]), (L*np.cos(angle)+self.position[0]*SCALE+WIDTH/2+offset[0],
        #           L*np.sin(angle)+self.position[1]*SCALE+HEIGHT/2+offset[1]),5,140)

        if len(self.orbit_points) > 2 :
            updated_points = []
            for point in self.orbit_points :
                if (len(updated_points)) > 500 :
                    updated_points.pop(0)

                x,y = point
                x = x * SCALE + WIDTH/2 + offset[0]
                y = y * SCALE + HEIGHT/2 + offset[1]

                updated_points.append((x,y))

            py.draw.aalines(WINDOW,self.orbit_color,False,updated_points,2)
    
        self.position[np.isnan(self.position)] = 0

        gfx.aacircle(surface, int(self.position[0]*SCALE+WIDTH/2+offset[0]), int(self.position[1]*SCALE+HEIGHT/2+offset[1]), int(self.radius), self.color)
        gfx.filled_circle(surface, int(self.position[0]*SCALE+WIDTH/2+offset[0]), int(self.position[1]*SCALE+HEIGHT/2+offset[1]), int(self.radius), self.color)

    def draw_particles(self, surface, offset) :

        if _magnitude(self.velocity) > 1000 :

            particle = Particle(np.array([self.position[0]*SCALE+WIDTH/2,self.position[1]*SCALE+HEIGHT/2]),-self.velocity,0.02,random.randint(int(self.radius*2/6),int(self.radius*2/3)),self.color)
            
            particles.append(particle)
            
            for particle in particles :
             
                particle.draw(surface,offset)
                particle.move()
                particle.update(particles)

    def add_force(self, force_array) :

        self.force = self.force + force_array

    def reset_force(self) :

        self.force = np.array([0,0,0])

    def add_acceleration(self, acceleration_array) :

        self.acceleration = self.acceleration + acceleration_array

    def reset_acceleration(self) :

        self.acceleration = np.array([0,0,0])

    def move(self) :

        self.velocity = self.velocity + self.acceleration *  TIMESKIP # ms-1 = ms-1 + s(ms^-2) or 
        self.position = self.position + (self.velocity) * TIMESKIP #d = d + d/t * t

        self.orbit_points.append((self.position[0],self.position[1]))

class Particle() :
    def __init__(self,position,velocity,shrinkrate,size,color) :
        
        # colors and shape
        self.shrinkrate = shrinkrate
        self.size = size
        self.color = color     

        # physical properties
        self.position = position
        self.velocity = velocity

    def update(self,particles) :

        self.size = self.size - self.shrinkrate

        self.color = [self.color[0]-1.5,self.color[1]-1.5,self.color[2]-1.5]

        updateColor(self.color)

        if self.size <= 0 or _magnitude(self.color) == 0:
            particles.remove(self)   
        
    def draw(self,surface,offset) :

        py.draw.circle(surface,self.color,(self.position[0]+offset[0],self.position[1]+offset[1]),self.size)

    def move(self) :

        self.position[0] += random.randint(-10,10)/25
        self.position[1] += random.randint(-10,10)/25 

# Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def main() :

    global SCALE
    global SCALER
    global orbits
    SCALER = 200

    bodies  = init()

    oldmousex = 0
    oldmousey = 0

    offset = np.array([0,0])
    offsetting = False

    sim = True
    running = True
    while running :

        CLOCK.tick(FPS)

        mousex,mousey = py.mouse.get_pos()

        for event in py.event.get() :
            if event.type == py.QUIT :
                running = False

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    running = False   
                    
                if event.key == py.K_UP:
                    SCALER += 25
                    if SCALER > 1000 :
                        SCALER = 1000
                    SCALE = SCALER/AU
                    
                if event.key == py.K_DOWN:
                    SCALER -= 25
                    if SCALER < 1 :
                        SCALER = 1
                    SCALE = SCALER/AU

                if event.key == py.K_r:
                    running = False
                    main()

                if event.key == py.K_SPACE:
                    if sim == True :
                        sim = False
                    else :
                        sim = True

            if event.type == py.MOUSEWHEEL :
                if event.y < 0 :
                    SCALER -= 1
                    if SCALER < 1 :
                        SCALER = 1
                    SCALE = SCALER / AU
                    
                if event.y > 0 :
                    SCALER += 1
                    if SCALER > 1000 :
                        SCALER = 1000
                    SCALE = SCALER / AU

            if event.type == py.MOUSEBUTTONDOWN :
                offsetting = True

            if event.type == py.MOUSEBUTTONUP :
                offsetting = False

        if offsetting == True :
            offset[0] = offset[0] + (mousex - oldmousex)
            offset[1] = offset[1] + (mousey - oldmousey)

        oldmousex = mousex
        oldmousey = mousey

        # Update    
        if sim :

            updateBodies(bodies)
  
            #updateBodiesLeapfrog(bodies) 

            #updateBodiesRungeKutta(bodies)

        py.display.update()

        # Render
        WINDOW.fill(DIM_GRAY)
        
        for body in bodies :

            body.draw_particles(WINDOW,offset)

            body.draw(WINDOW,offset)  

    return 0

if __name__ == '__main__' :
    main()