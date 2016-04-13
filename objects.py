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

			pygame.display.flip()

class Deathstar(pygame.sprite.Sprite):

	#pass in gamespace as argument
	def __init__(self, gs):
		pass
