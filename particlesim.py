# Setup Modules ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import pygame as py 
from pygame import gfxdraw as gfx
import time 
import random 
import numpy as np
py.init()
py.font.init()

# Setup Constants ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 1080
HEIGHT = 1080
FPS = 60
TIMESKIP = (3.154e+7) * 1/4

G = 6.67430e-11

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

def filled_circle(screen, colour, loc, radius):
	py.gfxdraw.aacircle(screen, int(loc[0]), int(loc[1]), radius, colour)
	py.gfxdraw.filled_circle(screen, int(loc[0]), int(loc[1]), radius, colour)

# Setup Classes -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Body : 
    def __init__(self,position,velocity, mass) :
        self.velocity = velocity
        self.force = np.array([0, 0, 0])
        self.mass = mass
        self.position = position
        self.color = WHITE
        self.radius = 10
        self.thickness = 10

    def draw(self, surface) :

        py.draw.circle(surface, self.color, (self.position[0],self.position[1]), self.radius, self.thickness)
        
        if self.velocity[0] < 0 :
            angle = (np.arctan(self.velocity[1]/self.velocity[0])+np.pi)
        else :
            angle = np.arctan(self.velocity[1]/self.velocity[0])

        py.draw.line(surface,WHITE,(self.position[0],self.position[1]),
                     (np.log2(3*_magnitude(self.velocity)+2)*20*np.cos(angle)+self.position[0],np.log2(3*_magnitude(self.velocity)+2)*20*np.sin(angle)+self.position[1]),2)


    def add_force(self, force_array) :
        self.force = self.force + force_array

    def reset_force(self) :
        self.force = np.array([0,0,0])

    def move(self) :
        
        self.velocity = self.velocity + ((self.force / self.mass)) * 5# * TIMESKIP * dt # a=F/m
        self.position = self.position + (self.velocity) * 5 # * TIMESKIP * dt # d = d_0 + v/t

class particle() :
    def __init__(self,position,velocity,age,size) :
        self.position = position
        self.velocity = velocity
        self.size = size
        self.age = age

# Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def init() :
    star = Body(np.array([400,400,0]),np.array([0,0,0]),6.5*pow(10,10))
    body = Body(np.array([350,650,0]),np.array([0.04,0.03,0]),6.5*pow(10,8))
    body2 = Body(np.array([750,950,0]),np.array([0.0,-0.04,0]),6.5*pow(10,8))
    body3 = Body(np.array([750,150,0]),np.array([0.0,0.04,0]),6.5*pow(10,8))

    return [star,body,body2,body3]


# [loc , velocity, timer]
particles = []


def main() :

    bodies = init()



    running = True
    while running :


        mouse = py.mouse.get_pos()

        #particles.append([[mouse[0],mouse[1]], [random.randint(0,20)/10,random.randint(0,20)/10], random.randint(4 , 6)])
        particles.append([[mouse[0],mouse[1]], [random.randint(-20,20)/10,random.randint(-20,20)/10], random.randint(4 , 6)])

        for particle in particles :
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1


            py.draw.circle(WINDOW, (random.randint(200,255),random.randint(0,255),random.randint(0,255)),(int(particle[0][0]),int(particle[0][1])),int(particle[2]))
            if particle[2] <= 0 :
                particles.remove(particle)



        CLOCK.tick(FPS)



        for event in py.event.get() :
            if event.type == py.QUIT :
                running = False
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    running = False
                if event.key == py.K_r:
                    running = False
                    main() 
        # Update 
        for body1 in bodies :
            body1.reset_force()
            for body2 in bodies :
                if _magnitude(_positionvector(body1.position,body2.position)) != 0 :
                    body1.add_force(_force(body1.position,body2.position,body1.mass,body2.mass))

            body1.move()
            
            

            
        py.display.update()

        # Render
        WINDOW.fill(BLACK)
        
        for body in bodies :
            body.draw(WINDOW)

        
    

    return 0

if __name__ == '__main__' :
    main()
