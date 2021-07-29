import pygame


class Ui:
	"""Manages the display at the top of the screen in which the diversity level and the current skills
	are displayed."""
	def __init__(self, game, img):
		self.game = game
		self.screen = game.screen
		self.width = self.game.width * .2
		self.height = self.game.height * .1
		self.rect = pygame.Rect((self.game.width / 2 - self.width / 2, 10), (self.width, self.height))
		self.image = pygame.transform.scale(img, self.rect.size).convert()

		self.skills = 0
		self.diversity = 0

	def add_skill(self):
		self.skills += 1
		if self.skills == 10:
			self.diversity += 1
			self.skills = 0
			self.spawn_new_structure()
		if self.diversity == 3:
			print("winner")

	def spawn_new_structure(self):
		pass

	def draw(self):
		# Draw base bars
		# Draw diversity bar @ 0 - bar_width * div_bar_w
		# Main
		pygame.draw.rect(self.screen, [200, 0, 0], (self.rect.topleft, (
			self.width * self.diversity / 4, self.height * .5)))
		# Outline
		pygame.draw.rect(self.screen, [255, 50, 50], (self.rect.topleft, (
			self.width * self.diversity / 4, self.height * .5)))
		#
		pygame.draw.rect(self.screen, [200, 0, 200], (self.rect.midleft, (
			self.width * self.skills / 10, self.height * .5)))
		pygame.draw.rect(self.screen, [200, 0, 0], (self.rect.topleft, (
			self.width * self.diversity / 4, self.height * .5)))
		self.screen.blit(self.image, self.rect.topleft)

	def loop(self):
		self.draw()