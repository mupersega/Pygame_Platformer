import pygame
import random


class ScrollingObject:
	def __init__(self, game, image, location):
		self.game = game
		self.screen = game.screen
		self.player = game.player
		self.image = image
		self.location = pygame.Vector2(location.x, location.y - self.image.get_height())
		self.rect = pygame.Rect(self.location, self.image.get_size())

	def update_rect(self):
		self.rect.topleft = (self.location.x - self.player.location.x, self.location.y)

	def on_screen(self):
		# Distance from player.
		dfp = self.location.distance_to(self.player.location) - self.rect.width
		return dfp <= self.game.width

	def scale_image(self, img, amt):
		w, h = img.get_size()
		return pygame.transform.scale(img, (w * amt, h * amt))

	def draw(self):
		draw_x = self.location.x - self.player.location.x
		self.screen.blit(self.image, self.rect.topleft)
		pygame.draw.rect(self.screen, [0, 100, 100], self.rect, width=1)


class Structure(ScrollingObject):
	def __init__(self, game, image, location):
		super().__init__(game, image, location)
		self.image = image.convert()
		self.image = self.scale_image(self.image, 5)
		self.location = pygame.Vector2(location.x, location.y - self.image.get_height())
		self.rect = pygame.Rect(self.location, self.image.get_size())
		self.loot = []

	def setup(self):
		# Set new loot
		pass

	def loop(self):
		if self.on_screen():
			self.update_rect()
			self.draw()


class Skill(ScrollingObject):
	def __init__(self, game, image, location):
		super().__init__(game, image, location)

	def check_collision(self):
		if self.rect.colliderect(self.player.hit_box):
			self.spawn_particles()
			self.update_progress()
			self.kill()

	def update_progress(self):
		self.game.ui.add_skill()

	def spawn_particles(self):
		for _ in range(random.randint(10, 15)):
			self.game.particles.append(
				Particle(
					self.game, pygame.Surface((5, 5)), pygame.Vector2(self.location), self.player.velocity))
			self.game.particles.append(
				SkillDust(
					self.game, pygame.Surface((5, 5)), pygame.Vector2(self.location), self.player.velocity))

	def kill(self):
		if self in self.game.skills.copy():
			self.game.skills.remove(self)

	def cleanup(self):
		if self.location.distance_to(self.player.location) > 5000:
			self.kill()

	def loop(self):
		if self.on_screen():
			self.update_rect()
			self.draw()
			self.check_collision()


class Obstacle(ScrollingObject):
	def __init__(self, game, image, location):
		super().__init__(game, image, location)

	def check_collision(self):
		if self.rect.colliderect(self.player.hit_box):
			bounce_vec = pygame.Vector2(pygame.Vector2(self.player.hit_box.center) - self.rect.center).normalize()
			self.player.velocity += bounce_vec * 5

	def draw(self):
		draw_x = self.location.x - self.player.location.x
		self.screen.blit(self.image, (draw_x, self.location.y))
		pygame.draw.rect(self.screen, [0, 100, 100], self.rect, width=1)

	def kill(self):
		if self in self.game.obstacles.copy():
			self.game.obstacles.remove(self)

	def cleanup(self):
		if self.location.distance_to(self.player.location) > 5000:
			self.kill()

	def loop(self):
		self.cleanup()
		if self.on_screen():
			self.update_rect()
			self.draw()
			self.check_collision()


class Particle(ScrollingObject):
	def __init__(self, game, image, location, vel):
		super().__init__(game, image, location)
		self.size = random.randint(2, 4)
		self.life = random.randint(100, 200)
		self.rgb = random.choice([(255, 255, 0), (255, 220, 150), (180, 180, 0)])
		# Vectors.
		self.inherited_velocity = pygame.Vector2(vel) * .5
		self.velocity = pygame.Vector2(
			random.uniform(-4, 4) * self.size, random.uniform(-2, -4) * self.size) + self.inherited_velocity
		self.gravity = pygame.Vector2(
			0, random.uniform(1, 2))

	def kill(self):
		if self in self.game.particles.copy():
			self.game.particles.remove(self)

	def update(self):
		if self.rect.bottom >= self.game.ground_level:
			self.velocity.y *= -.6
		self.velocity += self.gravity
		self.location += self.velocity
		self.life -= 1
		if self.life <= 0:
			self.kill()

	def draw(self):
		pygame.draw.rect(self.screen, self.rgb, self.rect)

	def loop(self):
		self.update_rect()
		self.update()
		self.draw()


class SkillDust(Particle):
	def __init__(self, game, image, location, vel):
		super().__init__(game, image, location, vel)
		self.gravity = pygame.Vector2(0, random.uniform(-1, -.5))
		self.direction = pygame.Vector2(self.location - self.player.location).normalize()
		self.velocity = pygame.Vector2(
			random.uniform(-3, 3) * self.size, random.uniform(3, 10) * self.size) - self.inherited_velocity
		self.rgb = random.choice([(255, 0, 150), (255, 100, 255), (200, 50, 255)])

	def arrive(self):
		if self.rect.colliderect(self.game.ui.rect):
			self.game.ui.add_skill()
			self.game.ui.flash()
			self.kill()

	def update(self):
		self.arrive()
		self.direction = pygame.Vector2(
			self.location - pygame.Vector2(
				self.player.location.x + self.game.width / 2 + self.player.velocity.x * 10, self.game.ui.rect.bottom))
		pygame.draw.circle(self.screen, [200, 0, 0], self.player.location, 10)
		if self.rect.bottom >= self.game.ground_level:
			self.velocity.y *= -.6
		# self.velocity += self.gravity
		self.velocity -= self.direction * .004
		self.location += self.velocity
		self.velocity *= .95
		self.life -= 1
		if self.life <= 0:
			self.kill()