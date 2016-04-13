import pygame
from pygame.locals import *
import sys

class Gamespace(object):
	def main(self):

		#initialize
		pygame.init()
		self.size = width, height = 640, 480
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

		black = 0, 0, 0

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

			#black screen
			self.screen.fill(black)

			#tick updates
			self.earth.tick()

			#display images
			self.screen.blit(self.earth.image, self.earth.rect)

			pygame.display.flip()

class Deathstar(pygame.sprite.Sprite):

	#pass in gamespace as argument
	def __init__(self, gs=None):
		pass

class Earth(pygame.sprite.Sprite):

	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("globe.bmp")
		self.rect = self.image.get_rect()
		self.rect.center = 600, 400

		self.orig_image = self.image

		self.exploding = False

	def tick(self):

		pass
