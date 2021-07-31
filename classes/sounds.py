import pygame


class Sounds:
	"""Settings class to hold all sounds for reference via game class."""
	def __init__(self, game):
		self.game = game
		# Sounds
		self.walk_sounds = [
			pygame.mixer.Sound('./assets/walk_1.wav'),
			pygame.mixer.Sound('./assets/walk_2.wav'),
			pygame.mixer.Sound('./assets/walk_3.wav')
		]
		self.dust_sound = pygame.mixer.Sound('./assets/dust.wav')
		self.jump_sound = pygame.mixer.Sound('./assets/jump.wav')
		self.skill_grab_sound = pygame.mixer.Sound('./assets/skill_grab.wav')
		self.diversity_up_sound = pygame.mixer.Sound('./assets/diversity_up.wav')
		self.hit_sound = pygame.mixer.Sound('./assets/oof.wav')

		self.setup_volumes()

	def setup_volumes(self):
		self.dust_sound.set_volume(.05)
		self.hit_sound.set_volume(.05)
		self.jump_sound.set_volume(.3)
		self.skill_grab_sound.set_volume(.1)
		for i in self.walk_sounds:
			i.set_volume(.2)

