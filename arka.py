import pygame
from math import *
import random

Vec2 = pygame.Vector2
Vec3 = pygame.Vector3

sprite_back = (160,128,96,128)
win_sz = (720,720)
speed = 1.0
baballes = []
balls_prop = []
class BaBalle(object):
	"Classe qui gere la BaBalle"
	def __init__(self,px,py,vx,vy,r,src_rect):
		"constructeur"
		self.pos=Vec2(px,py)
		self.mov=Vec2(vx,vy)
		self.radius = r
		self.rect = src_rect

	def step(self):
		"avance la balle d'un pas + teste collision bord"
		screen.blit(circles_surf, (int(self.pos.x-self.radius),int(self.pos.y-self.radius)), self.rect)
		self.pos += self.mov * speed
		if ((self.pos.x <= self.radius) or (self.pos.x >= win_sz[0]-self.radius)):
			# ping.play()
			self.mov.x *= -1.0
		if ((self.pos.y < self.radius) or (self.pos.y >= win_sz[1]-self.radius)):
			# ping.play()
			self.mov.y *= -1.0

def compute_circle(R,nb):
	circle = []
	for i in range(0,nb):
		a = (2.0*pi/nb)*i
		circle.append(R*Vec2(cos(a),sin(a)))
	return circle


# def draw_circle(x,y):
# 	local_circle = []
# 	Center = Vec2(x,y)
# 	for v in pre_circle:
# 		local_circle.append(Center+v)
# 	col = pygame.Color(255,255,0)
# 	pygame.draw.lines(screen,col,True,local_circle)


def predraw_one_sphere(surf, radius, color, x, y):
	rad2 = radius*radius
	for r in range(radius,1,-1):
		k = 1.0 - float(r*r)/rad2
		fc = color*k
		col = (int(fc.x),int(fc.y),int(fc.z))
		pygame.draw.circle(surf,col,(x,y),r,0)

def create_baballes_sprites():
	global circles_surf
	circles_surf = pygame.Surface((512,512))
	circles_surf.fill((0,0,0))
	circles_surf.set_colorkey((0,0,0))

	colors = [Vec3(255,0,0),Vec3(0,255,0),Vec3(0,0,255),Vec3(255,255,0),Vec3(255,0,255),Vec3(0,255,255),Vec3(255,255,255)]

	h = 16
	for r in range(16, 5, -1):
		for c in range(0,7):
			k = r/16.0
			predraw_one_sphere(circles_surf,r-1,colors[c]*k,r+c*2*r,h)
		balls_prop.append((r,h-r))
		h += 2*r
	
def create_baballe(r,px,py):
	x = random.uniform(r,win_sz[0]-r)
	y = random.uniform(r,win_sz[1]-r)
	a = random.uniform(0,6.2830)
	vx = cos(a)*(r*r/100.0)
	vy = sin(a)*(r*r/100.0)
	bb = BaBalle(x,y,vx,vy,r,(px,py,int(2*r),int(2*r)))
	baballes.append(bb)

# def move_ball(b,w):
# 	# draw_circle(b[0],b[1])
# 	screen.blit(image, (int(b[0]-b[4]),int(b[1]-b[4])), b[5])
# 	b[0] = b[0] + speed*b[2]
# 	b[1] = b[1] + speed*b[3]
# 	# b[3] += 0.01

# 	if ((b[0] <= b[4]) or (b[0] >= w[0]-b[4])):
# 		# ping.play()
# 		b[2] *= -1.0
# 	if ((b[1] < b[4]) or (b[1] >= w[1]-b[4])):
# 		# ping.play()
# 		b[3] *= -1.0

def draw():
	global ping
	back_y = 0
	while (back_y < win_sz[1]):
		back_x = 0
		while (back_x < win_sz[0]):
			screen.blit(image, (back_x,back_y), sprite_back)    
			back_x += 96
		back_y += 128

	# screen.blit(circles_surf, (0,0), circles_surf.get_rect())    



	for b in baballes:
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
	global ping
	screen = pygame.display.set_mode(win_sz)
	
	image = pygame.image.load("sprites.png")
	create_baballes_sprites();
	image.set_colorkey((0,0,1))
	
	nb = 64
	for k in range(len(balls_prop)-1,-1,-1):
		for j in range(0,7):
			for i in range(0,nb):
				bp = balls_prop[k]
				r = bp[0]
				create_baballe(r,j*r*2,bp[1])
		nb = int(nb/1.25)



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
			
		draw()
		sleeping = last_tick+33-pygame.time.get_ticks()
		if (sleeping>0):
			pygame.time.wait(sleeping)
		last_tick = pygame.time.get_ticks()
		pygame.display.flip()
		# print(sleeping)
 
if __name__ == "__main__":
	main()
