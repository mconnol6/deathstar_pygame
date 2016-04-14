import pygame
from pygame.locals import *
import sys
from math import atan2, pi, degrees

class Gamespace(object):
	def main(self):

		#initialize
		pygame.init()
		self.size = width, height = 640, 480
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

		self.deathstar = Deathstar(self)
		self.earth = Earth(self)

		while 1:
			#click tick
			self.clock.tick(60)

			#handle events
			for event in pygame.event.get():

				#quit game
				if event.type == QUIT:
					sys.exit()

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

		pygame.display.flip()

	def ticks(self):

		self.earth.tick()
		self.deathstar.tick()
		

class Deathstar(pygame.sprite.Sprite):

	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("media/deathstar.png")
		self.rect = self.image.get_rect()
		self.rect.center = 100, 100

		self.orig_image = self.image
		self.orig_rect = self.image.get_rect()

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
		self.rect = self.image.get_rect()
		self.rect.center = self.orig_rect.center

class Earth(pygame.sprite.Sprite):

	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("media/globe.png")
		self.rect = self.image.get_rect()
		self.rect.center = 600, 400

		self.orig_image = self.image

		self.exploding = False

	def tick(self):

		pass
