import pygame
from pygame.locals import *
import sys
from math import atan2, pi, degrees, sin, cos, sqrt

class Gamespace(object):
	def main(self):

		#initialize
		pygame.init()
		self.size = width, height = 640, 480
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

		self.deathstar = Deathstar(self)
		self.earth = Earth(self)
		#list of lasers
		self.lasers = [] 
		self.explosion = None

		while 1:
			#click tick
			self.clock.tick(60)

			#handle events
			self.handle_events()

			#tick updates
			self.ticks()

			#draw images
			self.draw_images()


	def draw_images(self):
		#black screen
		black = 0, 0, 0
		self.screen.fill(black)

		#draw earth
		self.screen.blit(self.earth.image, self.earth.rect)

		#draw deathstar
		self.screen.blit(self.deathstar.image, self.deathstar.rect)

		#draw lasers
		for laser in self.lasers:
			self.screen.blit(laser.image, laser.rect)

		if self.explosion:
			self.screen.blit(self.explosion.image, self.explosion.rect)

		pygame.display.flip()

	def ticks(self):

		self.earth.tick()
		self.deathstar.tick()
		
		for laser in self.lasers:
			laser.tick()

		if self.explosion:
			self.explosion.tick()
			
		
	def handle_events(self):

		for event in pygame.event.get():

			#quit game
			if event.type == QUIT:
				sys.exit()

			if event.type == MOUSEBUTTONDOWN:
				self.deathstar.is_firing = True
				mx, my = pygame.mouse.get_pos()
				self.xfire = mx
				self.yfire = my

			if event.type == MOUSEBUTTONUP:
				self.deathstar.is_firing = False
			
			if event.type == KEYDOWN:
				#if arrow pressed, change velocity of deathstar
				if event.key == pygame.K_DOWN:
					self.deathstar.is_moving = True
					self.deathstar.velocity = 0, 10
				if event.key == pygame.K_UP:
					self.deathstar.is_moving = True
					self.deathstar.velocity = 0, -10
				if event.key == pygame.K_RIGHT:
					self.deathstar.is_moving = True
					self.deathstar.velocity = 10, 0
				if event.key == pygame.K_LEFT:
					self.deathstar.is_moving = True
					self.deathstar.velocity = -10, 0

			# if arrow is not being pressed anymore, stop deathstar from moving
			if event.type == KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == K_LEFT: 
					self.deathstar.is_moving = False


class Deathstar(pygame.sprite.Sprite):

	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("media/deathstar.png")
		self.rect = self.image.get_rect()
		self.rect.center = 100, 100

		self.orig_image = self.image
		self.orig_rect = self.image.get_rect()

		# deathstar velocity
		self.is_moving = False
		self.velocity = 0, 0

		self.is_firing = False

	def tick(self):
		if self.is_firing:
			new_laser = Laser(self.gs)
			self.gs.lasers.append(new_laser)

		# if deathstar is not firing, then rotate it and check if it should be moving
		else:
			#get mouse position
			mx, my = pygame.mouse.get_pos()

			#get center coordinates
			cx = self.rect.centerx
			cy = self.rect.centery

			#calculate slope
			angle = atan2(my - cy, mx - cx)

			#rotate image
			self.image = pygame.transform.rotate(self.orig_image, (degrees(angle) + 45) * -1)
			self.rect = self.image.get_rect(center = self.rect.center)

			#move deathstar by adding velocity
			if self.is_moving:
				self.rect = self.rect.move(self.velocity[0], self.velocity[1])



class Earth(pygame.sprite.Sprite):

	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("media/globe.png")
		self.rect = self.image.get_rect()
		self.rect.center = 600, 400
		self.radius = self.rect.height / 2 - 15
		self.hitpoints = 40
		self.explodingpoints = 5

		self.exploding = False

	def tick(self):

		if not self.exploding:
			#for each laser, check if collided with earth
			i = 0
			while i < len(self.gs.lasers):
				x, y = self.gs.lasers[i].rect.center
				gx, gy = self.rect.center
				d = sqrt((x-gx)*(x-gx) + (y-gy)*(y-gy))
				if self.radius > d:
					self.hitpoints = self.hitpoints - 1

					#remove laser from vector
					del self.gs.lasers[i]
				else:
					i = i + 1

			if self.hitpoints == 20:
				self.image = pygame.image.load("media/globe_red100.png")

			if self.hitpoints == 0:
				self.image = pygame.image.load("media/empty.png")
				self.exploding = True
				self.gs.explosion = Explosion()
				self.sound = pygame.mixer.Sound("media/explode.wav")
				self.sound.play()

class Laser(pygame.sprite.Sprite):

	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("media/laser.png")
		self.rect = self.image.get_rect()
		self.rect.center = gs.deathstar.rect.center
		cx, cy = gs.deathstar.rect.center

		#calculate change in x and y
		velocity = 7
		angle = atan2(self.gs.yfire - cy, self.gs.xfire - cx)
		self.dx = velocity * cos(angle)
		self.dy = velocity * sin(angle)

		self.rect = self.rect.move(self.dx * 7, self.dy * 7)

	def tick(self):
		self.rect = self.rect.move(self.dx, self.dy)

class Explosion(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.images = ["media/explosion/frames015a.png", "media/explosion/frames015a.png", "media/explosion/frames014a.png", "media/explosion/frames013a.png", "media/explosion/frames012a.png", "media/explosion/frames011a.png", "media/explosion/frames010a.png", "media/explosion/frames009a.png", "media/explosion/frames008a.png", "media/explosion/frames007a.png", "media/explosion/frames006a.png", "media/explosion/frames005a.png", "media/explosion/frames004a.png", "media/explosion/frames003a.png", "media/explosion/frames002a.png", "media/explosion/frames001a.png", "media/explosion/frames000a.png"]
		self.image = pygame.image.load(self.images[-1])
		self.rect = self.image.get_rect()
		self.rect.center = 600, 400

	def tick(self):
		if len(self.images) >= 2:
			del self.images[-1]
			self.image = pygame.image.load(self.images[-1])
