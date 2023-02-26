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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173,216,230)
YELLOW = (255,255,0)
PURPLE = (203, 195, 227)
GRAY = (169,169,169)
DIM_GRAY = (16,16,16)
ORANGE = (255,165,0)

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

def updateBodies(bodies):

    for body1 in bodies : 

        body1.reset_force()

        for body2 in bodies :

            if _magnitude(_positionvector(body1.position,body2.position)) != 0 :

                body1.add_force(_force(body1.position,body2.position,body1.mass,body2.mass))

        body1.move()

def init() :

    sun = Body(YELLOW,20,(np.array([0,0,0])*AU),np.array([0,0,0]),1.98892e30)
    mercury = Body(GRAY,6,(np.array([0.387,0,0])*AU),np.array([0,-47.3e3,0]),3.3e23)
    venus = Body(ORANGE,8,np.array([0.783,0,0])*AU,np.array([0,-35.02e3,0]),4.8685e24)
    earth = Body(LIGHT_BLUE,8,(np.array([-1,0,0])*AU),np.array([0,29.783e3,0]),5.9742e24)
    mars = Body(RED,7,(np.array([-1.524,0,0])*AU),np.array([0,24.077e3,0]),6.39e23)


    return [sun,mercury,venus,earth,mars]

# Setup Classes -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Body : 

    def __init__(self,color,radius,position,velocity, mass) :
        self.color = color
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.force = np.array([0, 0, 0])
        self.mass = mass
        self.thickness = 0

    def draw(self, surface) :

        if self.velocity[0] < 0 :
            angle = (np.arctan(self.velocity[1]/self.velocity[0])+np.pi)
        else :
            angle = np.arctan(self.velocity[1]/self.velocity[0])

        L=30

        draw_arrow(WINDOW, WHITE, (self.position[0]*SCALE+WIDTH/2,self.position[1]*SCALE+HEIGHT/2), (L*np.cos(angle)+self.position[0]*SCALE+WIDTH/2,
                  L*np.sin(angle)+self.position[1]*SCALE+HEIGHT/2),5,140)

        gfx.aacircle(surface, int(self.position[0]*SCALE+WIDTH/2), int(self.position[1]*SCALE+HEIGHT/2), self.radius, self.color)
        gfx.filled_circle(surface, int(self.position[0]*SCALE+WIDTH/2), int(self.position[1]*SCALE+HEIGHT/2), self.radius, self.color)

    def draw_particles(self, surface) :

        if _magnitude(self.velocity) > 1000 :

            particle = Particle(np.array([self.position[0]*SCALE+WIDTH/2,self.position[1]*SCALE+HEIGHT/2]),-self.velocity,0.02,random.randint(int(self.radius*2/6),int(self.radius*2/3)),self.color)
            
            particles.append(particle)
            
            for particle in particles :
             
                particle.draw(surface)
                particle.move()
                particle.update(particles)


    def add_force(self, force_array) :
        self.force = self.force + force_array

    def reset_force(self) :
        self.force = np.array([0,0,0])

    def move(self) :
        self.velocity = self.velocity + (self.force / self.mass) *  TIMESKIP # a=F/m
        self.position = self.position + (self.velocity) * TIMESKIP #d = d_0 + v/t

class Particle() :
    def __init__(self,position,velocity,shrinkrate,size,color) :
        self.position = position
        self.velocity = velocity
        self.shrinkrate = shrinkrate
        self.size = size
        self.color = color     

    def update(self,particles) :

        self.size = self.size - self.shrinkrate

        colors = list(self.color)
        colors = [colors[0]-1.5,colors[1]-1.5,colors[2]-1.5]

        if colors[0] < 0 :
            colors [0] = 0
        if colors[1] < 0 :
            colors [1] = 0
        if colors[2] < 0 :
            colors [2] = 0

        self.color = tuple(colors)

        if self.size <= 0 or _magnitude(list(self.color)) == 0:
            particles.remove(self)
        
    def draw(self,surface) :
        py.draw.circle(surface,self.color,(self.position[0],self.position[1]),self.size)

    def move(self) :

        self.position[0] += random.randint(-10,10)/25
        self.position[1] += random.randint(-10,10)/25 

        


# Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def main() :

    global SCALE
    SCALER = 200

    bodies = init()

    prev_time = time.time()

    running = True
    while running :

        CLOCK.tick(FPS)

        mousex,mousey = py.mouse.get_pos()

        prev_time,dt = _deltatime(prev_time)

        for event in py.event.get() :
            if event.type == py.QUIT :
                running = False
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    running = False   
                if event.key == py.K_UP:
                    SCALER += 50
                    SCALE = SCALER/AU
                if event.key == py.K_DOWN:
                    SCALER -= 50
                    SCALE = SCALER/AU
                if event.key == py.K_r:
                    running = False
                    main()

        # Update 
        KEYS_PRESSED = py.key.get_pressed()

        updateBodies(bodies)                          

        py.display.update()

        # Render
        WINDOW.fill(DIM_GRAY)
        
        for body in bodies :

            body.draw_particles(WINDOW)
            body.draw(WINDOW)  

        #py.draw.rect(WINDOW,WHITE, py.Rect(0+PADDING,0+PADDING,WIDTH/2-PADDING,HEIGHT/2-PADDING))
    
    return 0

if __name__ == '__main__' :
    main()