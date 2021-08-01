import pygame


class Ui:
	"""Manages the display at the top of the screen in which the diversity level and the current skills
	are displayed."""
	def __init__(self, game, img, levels):
		self.game = game
		self.screen = game.screen
		self.width = self.game.width * .2
		self.height = self.game.height * .1
		self.rect = pygame.Rect((self.game.width / 2 - self.width / 2, 10), (self.width, self.height))
		self.diversity_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width - 2, self.rect.height / 2 - 2)
		self.skills_rect = pygame.Rect(self.rect.left, self.rect.centery, self.rect.width - 2, self.rect.height / 2 - 2)
		self.image = pygame.transform.scale(img, self.rect.size).convert()
		self.image.set_colorkey((0, 0, 0))

		self.skilldust_this_lvl = int(self.game.state_dict["skill_dust"])
		self.skills = 0
		self.total_diversity = levels
		self.diversity = 70
		self.flash_timer = 0

		self.skills_x = self.rect.left + self.width * self.skills / self.skilldust_this_lvl
		self.diversity_x = self.rect.left + self.width * self.diversity / self.total_diversity

	def add_skill_dust(self):
		self.skills += 1
		self.skills_x = self.rect.left + self.width * self.skills / self.skilldust_this_lvl
		if self.skills == self.skilldust_this_lvl:
			self.game.diversity_lvl_up(self.diversity)
			self.skills = 0
			if self.diversity < self.total_diversity - 1:
				self.diversity += 1
				self.diversity_x = self.rect.left + self.width * self.diversity / self.total_diversity
			elif not self.game.free_play:
				self.game.game_finish()

	def draw(self):
		# Background
		pygame.draw.rect(self.screen, [100, 20, 0], self.diversity_rect)
		pygame.draw.rect(self.screen, [122, 25, 100], self.skills_rect)
		# Main
		pygame.draw.rect(self.screen, [255, 100, 0], (self.rect.topleft, (
			self.width * self.diversity / self.total_diversity, self.height * .5)))
		pygame.draw.rect(self.screen, [255, 50, 200], (self.skills_rect.topleft, (
			self.width * self.skills / self.skilldust_this_lvl, self.height * .5)))
		# Line
		pygame.draw.line(self.screen, [255, 150, 150], (
			self.diversity_x, self.diversity_rect.top), (self.diversity_x, self.diversity_rect.bottom), width=1)
		pygame.draw.line(self.screen, [255, 100, 230], (
			self.skills_x, self.skills_rect.top), (self.skills_x, self.skills_rect.bottom), width=1)

		self.screen.blit(self.image, self.rect.topleft)

	def loop(self):
		self.draw()

