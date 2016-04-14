import pygame
from pygame.locals import *
import sys
from math import atan2, pi, degrees, sin, cos

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

		pygame.display.flip()

	def ticks(self):

		self.earth.tick()
		self.deathstar.tick()
		
		for laser in self.lasers:
			laser.tick()
			
		
	def handle_events(self):

		for event in pygame.event.get():

			#quit game
			if event.type == QUIT:
				sys.exit()

			if event.type == MOUSEBUTTONDOWN:
				mx, my = pygame.mouse.get_pos()
				cx, cy = self.deathstar.rect.center
				new_laser = Laser(cx, cy, mx, my, self)
				self.lasers.append(new_laser)

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

	def tick(self):
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

		self.exploding = False

	def tick(self):

		pass

class Laser(pygame.sprite.Sprite):

	def __init__(self, cx, cy, x, y, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("media/laser.png")
		self.rect = self.image.get_rect()
		self.rect.center = cx, cy
		self.velocity = 5
		self.angle = atan2(y - cy, x - cx)
		self.dx = self.velocity * cos(self.angle)
		self.dy = self.velocity * sin(self.angle)

	def tick(self):
		self.rect = self.rect.move(self.dx*self.velocity, self.dy*self.velocity)
