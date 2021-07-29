import pygame


class Background:
	"""This is the class to manage the current display surface and it will ALWAYS
	be centred on the player for simplicity's sake."""
	def __init__(self, game, z, image):
		self.game = game
		self.player = game.player
		self.z = z
		self.x = 0
		self.bg_img = pygame.transform.scale(
			image, self.game.screen.get_size())
		self.surface = pygame.Surface(self.game.screen.get_size())
		self.positions = [- self.surface.get_width(), 0, self.surface.get_width()]

	def scroll(self, amt):
		self.x -= amt / self.z

	def loop(self):
		new_join = self.x % self.game.width
		self.game.screen.blit(self.bg_img, (new_join, 0))
		self.game.screen.blit(self.bg_img, (new_join - self.game.width, 0))

