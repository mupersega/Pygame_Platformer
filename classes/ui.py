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
		self.diversity_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height / 2)
		self.skills_rect = pygame.Rect(self.rect.left, self.rect.centery, self.rect.width, self.rect.height / 2)
		self.image = pygame.transform.scale(img, self.rect.size).convert()

		self.skills = 0
		self.diversity = 0
		self.flash_timer = 0

		self.skills_x = self.rect.left + self.width * self.skills / 100
		self.diversity_x = self.rect.left + self.width * self.diversity / 4

	def add_skill(self):
		self.skills += 1
		self.skills_x = self.rect.left + self.width * self.skills / 100
		if self.skills == 100:
			self.diversity += 1
			self.diversity_x = self.rect.left + self.width * self.diversity / 4
			self.skills = 0
			self.spawn_new_structure()
		if self.diversity == 3:
			print("winner")

	def spawn_new_structure(self):
		pass

	def flash(self):
		self.flash_timer += 1

	def draw(self):
		# Background
		pygame.draw.rect(self.screen, [80, 80, 80], self.diversity_rect)
		pygame.draw.rect(self.screen, [122, 25, 100], self.skills_rect)
		# Main
		pygame.draw.rect(self.screen, [200, 0, 0], (self.rect.topleft, (
			self.width * self.diversity / 4, self.height * .5)))
		pygame.draw.rect(self.screen, [255, 50, 200], (self.skills_rect.topleft, (
			self.width * self.skills / 100, self.height * .5)))
		# Line
		pygame.draw.line(self.screen, [255, 100, 100], (
			self.diversity_x, self.diversity_rect.top), (self.diversity_x, self.diversity_rect.bottom), width=1)
		pygame.draw.line(self.screen, [255, 100, 230], (
			self.skills_x, self.skills_rect.top), (self.skills_x, self.skills_rect.bottom), width=1)

		self.screen.blit(self.image, self.rect.topleft)

	def loop(self):
		self.draw()

