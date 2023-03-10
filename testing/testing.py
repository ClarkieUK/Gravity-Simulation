import pygame as py
import sys
from random import randint

class Tree(py.sprite.Sprite) :
    def __init__(self,pos,group) :
        super().__init__(group)
        self.image = py.image.load('D:\\Tools\\VSC\\Code\\Physics-Simulations\\Gravity Simulation\\testing\graphics\\tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
	
class Player(py.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = py.image.load('D:\\Tools\\VSC\\Code\\Physics-Simulations\\Gravity Simulation\\testing\\graphics\\player.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.direction = py.math.Vector2()
		self.speed = 5

	def input(self):
		keys = py.key.get_pressed()

		if keys[py.K_UP]:
			self.direction.y = -1

		elif keys[py.K_DOWN]:
			self.direction.y = 1

		else:
			self.direction.y = 0

		if keys[py.K_RIGHT]:
			self.direction.x = 1
			
		elif keys[py.K_LEFT]:
			self.direction.x = -1

		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed

class CameraGroup(py.sprite.Group) :
	def __init__ (self) :
		super().__init__()
		self.display_surface = py.display.get_surface()

	def custom_draw(self) :
	    for sprite in self.sprites():
		    self.display_surface.blit(sprite.image,sprite.rect)

py.init()
screen = py.display.set_mode((1280,720))
clock = py.time.Clock()

camera_group = CameraGroup()
Player((640,360),camera_group)

for i in range(20) :
    random_x = randint(0,1000)
    random_y = randint(0,1000)
    Tree((random_x,random_y),camera_group)

while True :
    for event in py.event.get():
        if event.type == py.QUIT :
            py.quit()
            sys.exit()

        screen.fill('#71ddee')

        camera_group.update()
        camera_group.custom_draw()

        py.display.update()
        clock.tick(60)
