import pygame

# PLAYER SPRITE_SHEET
SPRITE_SHEET = pygame.transform.scale(pygame.image.load('./assets/character-min.png'), (100 * 4, 100 * 4))


class Player:
	"""This class manages the player, for simplicity's sake it will always be drawn in
	the centre of the screen and the display surface will move beneath him."""
	def __init__(self, game):
		self.game = game
		self.frames = SPRITE_SHEET.convert()
		self.sprite = pygame.Surface((self.frames.get_width() / 4, self.frames.get_height()))
		self.frame_w, self.frame_h = self.frames.get_width() / 4, self.frames.get_height() / 4
		self.rect = pygame.Rect(self.game.width / 2, 0, self.frame_w, self.frame_h)
		self.hit_box = pygame.Rect(self.game.width / 2 + self.frame_w / 4, 0, self.frame_w / 2, self.frame_h)

		self.gravity = pygame.Vector2(0, 2)
		self.acceleration = pygame.Vector2(3, 0)
		self.base_speed = 5
		self.speed = self.base_speed
		self.top_speed = 10
		self.location = pygame.Vector2(0, self.game.ground_level - self.rect.height)
		self.velocity = pygame.Vector2(0, 0)
		self.altitude = 0

		self.walk_counter = 0
		self.frame_counter = 0
		self.spritesheet_row = 3
		self.moving_right = False
		self.moving_left = False

	def move_left(self):
		if abs(self.velocity.x) < self.speed:
			self.velocity.x -= self.acceleration.x

	def move_right(self):
		if abs(self.velocity.x) < self.speed:
			self.velocity.x += self.acceleration.x

	def jump(self):
		if self.on_ground():
			self.velocity.y -= 20 + self.speed * 2
			self.velocity.x += self.velocity.x * .3
			self.spritesheet_row = 2  # row 3(2) is jump animations

	def update(self):
		if self.moving_left:
			self.move_left()
		if self.moving_right:
			self.move_right()
		self.location += self.velocity
		self.rect.top = self.location.y
		self.hit_box.top = self.location.y
		self.game.background_scroll(self.velocity.x)
		if self.on_ground():
			self.velocity.x -= self.velocity.x * .2
		self.jump_update()

	def on_ground(self):
		return self.rect.bottom >= self.game.ground_level

	def jump_update(self):
		if not self.on_ground():
			self.velocity += self.gravity
		else:
			self.rect.bottom = self.game.ground_level
			self.hit_box.bottom = self.game.ground_level
			self.velocity.y = 0

	def update_draw_counter(self):
		# If y velocity set jumping animations
		if not self.on_ground():
			# Update jumping sprite frame(0=launch, 1=upward, 2=falling, 3=land)
			self.frame_counter = 0 if self.velocity.y <= 0 else 1
			# To account for different directions
			self.frame_counter += 0 if self.velocity.x >= 0 else 2
			return
		# If going right set right walking animations
		if self.velocity.x > 0.1:
			self.walk_counter += round(abs(self.velocity.x), 2)
			self.spritesheet_row = 0
			if self.walk_counter > 60:
				self.walk_counter = 0
				self.frame_counter += 1 if self.frame_counter < 4 else - 3
			return
		# If going left set left walking animations
		if self.velocity.x < - 0.1:
			self.walk_counter += round(abs(self.velocity.x), 2)
			self.spritesheet_row = 1
			if self.walk_counter > 60:
				self.walk_counter = 0
				self.frame_counter += 1 if self.frame_counter < 4 else - 3
			return
		else:
			self.walk_counter = 0
			self.frame_counter = 0
			self.spritesheet_row = 3

	def draw(self):
		frame = self.frame_counter % 4
		pygame.draw.rect(self.game.screen, [0, 100, 50], self.rect, width=1)
		pygame.draw.rect(self.game.screen, [100, 100, 50], self.hit_box, width=1)

		self.game.screen.blit(self.frames, (
				self.game.width / 2, self.rect.top), (
					frame * self.frame_w, self.spritesheet_row * self.frame_h, self.frame_w, self.frame_h))

	def loop(self):
		self.update()
		self.update_draw_counter()
		self.draw()

