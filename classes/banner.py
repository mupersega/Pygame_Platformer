import pygame


class Banner:
	"""A class that manages the display of a banner with text."""
	def __init__(self, game, text):
		self.game = game
		self.screen = game.screen
		self.text = text
		self.render = game.banner_font.render(self.text, True, (255, 240, 230))
		self.rect = pygame.Rect(
			(self.game.width / 2 - self.render.get_width() / 2, self.game.ui.rect.bottom + 10), self.render.get_size())
		self.life = 400
		self.y_offset = 0

	def update(self):
		self.rect.bottom = self.game.player.rect.top - 20 - self.y_offset
		self.rect.centerx = self.game.player.rect.centerx
		self.life -= 1
		if self.life < 60:
			self.y_offset += 1
		if self.life <= 0:
			self.kill()

	def draw(self):
		self.screen.blit(self.render, self.rect.topleft)

	def kill(self):
		if self in self.game.banners.copy():
			self.game.banners.remove(self)

	def loop(self):
		self.update()
		self.draw()

