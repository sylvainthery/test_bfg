import pygame
from math import *
import random

Vec2 = pygame.Vector2
Vec3 = pygame.Vector3

sprite_back = (160,128,96,128)
win_sz = (720,720)
speed = 1.0
baballes = []
shadow_angle = -0.77
shadow_rad = 12

scroll = -127
speed_scroll = 1

class BaBalle(object):
	"Classe qui gere la BaBalle"
	def __init__(self,px,py,vx,vy,r,src_rect,sh_rect,ci):
		"constructeur"
		self.pos=Vec2(px,py)
		self.mov=Vec2(vx,vy)
		self.radius = r
		self.rect = src_rect
		self.rect_shadow = sh_rect
	def draw(self):
		screen.blit(circles_surf, (int(self.pos.x-self.radius),int(self.pos.y-self.radius)), self.rect)

	def draw_shadow(self,shift):
		screen.blit(circles_surf, (int(self.pos.x-self.radius)+shift[0],int(self.pos.y-self.radius)+shift[1]), self.rect_shadow, pygame.BLEND_SUB)

	def step(self):
		"avance la balle d'un pas + teste collision bord"
		self.pos += self.mov * speed
		if ((self.pos.x <= self.radius) or (self.pos.x >= win_sz[0]-self.radius)):
			# ping.play()
			self.mov.x *= -1.0
		if ((self.pos.y < self.radius) or (self.pos.y >= win_sz[1]-self.radius)):
			# ping.play()
			self.mov.y *= -1.0

def predraw_one_sphere(surf, radius, color, x, y):
	rad2 = radius*radius
	for r in range(radius,1,-1):
		k = 1.0 - float(r*r)/rad2
		fc = color * k
		col = (int(fc.x),int(fc.y),int(fc.z),255)
		pygame.draw.circle(surf,col,(x,y),r,0)
	# pygame.draw.circle(surf,(55,55,55,64),(x,y+2*radius),int(0.9*radius),0)
	# pygame.draw.circle(surf,(55,55,55,96),(x,y+2*radius),int(0.7*radius),0)
	# pygame.draw.circle(surf,(55,55,55,128),(x,y+2*radius),int(0.5*radius),0)

def predraw_one_shadow_sphere(surf, radius, x, y):
	pygame.draw.circle(surf,(75,75,75),(x,y),int(0.9*radius),0)
	pygame.draw.circle(surf,(95,95,95),(x,y),int(0.7*radius),0)
	pygame.draw.circle(surf,(105,125,125),(x,y),int(0.5*radius),0)


def create_baballes_sprites(r):
	global circles_surf
	circles_surf = pygame.Surface((512,512))
	circles_surf.fill((0,0,0,0))
	circles_surf.set_colorkey((0,0,0))
	colors = [Vec3(255,0,0),Vec3(0,255,0),Vec3(0,0,255),Vec3(255,255,0),Vec3(255,0,255),Vec3(0,255,255),Vec3(255,255,255)]
	for i in range(0,7):
		predraw_one_sphere(circles_surf,r-1,colors[i],3*r+2*i*r,r)
	predraw_one_shadow_sphere(circles_surf,r,r,r)
	
def create_baballe(r,ci):
	rm = r-1
	x = random.uniform(rm,win_sz[0]-rm)
	y = random.uniform(rm,win_sz[1]-rm)
	a = random.uniform(0,6.2830)
	vx = cos(a)
	vy = sin(a)
	d = 2*r
	bb = BaBalle(x,y,vx,vy,9,(ci*d,0,d,d),(0,0,d,d),ci)
	baballes.append(bb)
	
def draw():
	global scroll
	back_y = scroll
	while (back_y < win_sz[1]):
		back_x = 0
		while (back_x < win_sz[0]):
			screen.blit(image, (back_x,back_y), sprite_back)    
			back_x += 96
		back_y += 128
	scroll = scroll + speed_scroll
	if (scroll >= 0):
		scroll = -127

	# screen.blit(circles_surf, (0,0), circles_surf.get_rect())    

	shift = (int(shadow_rad*cos(shadow_angle)),int(shadow_rad*sin(shadow_angle)))

	for b in baballes:
		b.draw_shadow(shift)

	for b in baballes:
		b.draw()
		b.step()

	# screen.blit(surface,surface.get_rect())
	

def main():
	# pygame.mixer.pre_init()
	# 44100, -16, 2, 512
	pygame.init()
	# pygame.mixer.fadeout(250)
	pygame.display.set_caption("PyGame_First_Test")
	global sprite_ball
	global screen
	global image
	global speed
	global shadow_angle
	global shadow_rad
	screen = pygame.display.set_mode(win_sz)
	
	image = pygame.image.load("sprites2.png")

	rad = 16
	create_baballes_sprites(rad);
	image.set_colorkey((0,0,1))
	
	for i in range(0,20):
		create_baballe(rad,1+i%7)


	# ping = pygame.mixer.Sound("crystal.wav")


	running = True
	last_tick = pygame.time.get_ticks()

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		all_keys = pygame.key.get_pressed()
		if all_keys[pygame.K_SPACE]:
			ping.play()
		if all_keys[pygame.K_ESCAPE]:
			running = False
		if (all_keys[pygame.K_PLUS] or all_keys[pygame.K_KP_PLUS]):
			speed *= 1.01
		if (all_keys[pygame.K_MINUS] or all_keys[pygame.K_KP_MINUS]):
			speed /= 1.01
		
		if (all_keys[pygame.K_e]):
			shadow_angle += 0.1
		if (all_keys[pygame.K_r]):
			shadow_rad +=1
		if (all_keys[pygame.K_t]):
			shadow_rad -=1

			
		draw()
		sleeping = last_tick+33-pygame.time.get_ticks()
		if (sleeping>0):
			pygame.time.wait(sleeping)
		last_tick = pygame.time.get_ticks()
		pygame.display.update()
		# print(sleeping)
 
if __name__ == "__main__":
	main()
