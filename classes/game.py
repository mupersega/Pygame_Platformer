import pygame
import random
import sys
import time

from classes.background import Background
from classes.player import Player
from classes.scrolling_object import Structure, Obstacle, Skill
from classes.ui import Ui
from classes.banner import Banner
from utilities.skills import skills_info

pygame.init()

# IMAGES
# - Backgrounds - #
grass_bg = pygame.image.load('./assets/full_bg_grass-min.png')
sky_bg = pygame.image.load('./assets/full_bg_sky-min.png')
trees_bg = pygame.image.load('./assets/full_bg_trees-min.png')
shrubs_bg = pygame.image.load('./assets/full_bg_shrubs-min.png')
# - Player - #
player_spritesheet = pygame.transform.scale(pygame.image.load('./assets/character-min.png'), (100 * 4, 100 * 4))
# - Structures - #
excel_temple_img = pygame.image.load('./assets/excel_temple_outer-min.png')
# - Obstacles - #
rocks = [
	pygame.image.load('./assets/rock_1-min.png'),
	pygame.image.load('./assets/rock_2-min.png')
]
# - UI - #
ui_img = pygame.image.load('./assets/ui-min.png')
# - Banners - #
banners = [
	pygame.image.load('./assets/banner-min.png'),
]


class Game:
	"""The main class overseeing all other classes. Player, structures, enemies, and
	display surfaces."""
	def __init__(self, width, height):
		self.width, self.height = width, height
		self.screen = pygame.display.set_mode((width, height))

		# Game Settings
		self.ground_level = int(self.height * .90)
		self.fps = 90
		# Different states and their accompanying information
		self.state = 0
		self.state_dict = skills_info[self.state]

		# Spawn timing.
		self.spawn_time = time.time()
		self.skill_spawn_spacing = 3
		self.skill_spawn_timer = self.skill_spawn_spacing
		self.obstacle_spawn_spacing = 3
		self.obstacle_spawn_timer = self.obstacle_spawn_spacing

		# Classes
		self.player = Player(self, player_spritesheet.convert())

		self.backgrounds = [
			# Background(self, 7, sky_bg.convert()),
			Background(self, 3, trees_bg.convert())
			# Background(self, 1, grass_bg.convert())
		]
		self.foregrounds = [
			Background(self, 1, grass_bg.convert())
		]

		self.ui = Ui(self, ui_img, len(skills_info))
		self.banner_font = pygame.font.Font('./assets/hellovetica.ttf', 20)

		self.scrolling_objects = []
		self.structures = []
		self.skills = []
		self.obstacles = []
		self.triggers = []
		self.particles = []
		self.banners = []
		self.setup_on_start()

	def setup_on_start(self):
		new_vec = pygame.Vector2(random.randint(600, 1000),  self.ground_level - random.randint(40, 400))
		self.skills.append(
			Skill(self, random.choice(rocks), new_vec))

	def background_scroll(self, amt):
		for i in self.backgrounds:
			i.scroll(amt)
		for i in self.foregrounds:
			i.scroll(amt)

	def spawn_skill(self):
		max_skills = 5
		if len(self.skills) < max_skills:
			rand_x_offset = random.randint(self.width, self.width * 2)
			rand_y_offset = random.choice([50, 200, 400])
			new_vec = pygame.Vector2(self.player.location.x + rand_x_offset, self.ground_level - rand_y_offset)
			self.skills.append(
				Skill(self, random.choice(rocks), new_vec))

	def spawn_obstacle(self):
		max_obstacles = 10
		if len(self.obstacles) < max_obstacles:
			rand_x_offset = random.randint(self.width, self.width * 2)
			new_vec = pygame.Vector2(
				self.player.location.x + rand_x_offset, self.ground_level + random.randint(5, 10))
			self.obstacles.append(
				Obstacle(self, random.choice(rocks), new_vec))

	def spawn(self):
		if self.spawn_time < time.time():
			print("spawning")
			self.spawn_time += 1
			# Spawn a skill off screen
			if random.randint(0, self.skill_spawn_timer) < 2:
				self.spawn_skill()
			if random.randint(0, self.obstacle_spawn_timer) < 2:
				self.spawn_obstacle()

	def diversity_lvl_up(self):
		self.state += 1
		self.state_dict = skills_info[self.state]
		for i in self.banners:
			i.y_offset += i.rect.height
		self.banners.append(Banner(self, self.state_dict["text"]))
		if skills_info[self.state]["structure"] != "None":
			img = globals()[f"{skills_info[self.state]['structure']}_img"]
			self.structures.append(Structure(self, img, (
				pygame.Vector2(self.player.location.x + self.width * 2, self.ground_level + 20
			))))

	def update_backgrounds(self):
		for i in self.backgrounds:
			i.loop()

	@staticmethod
	def run_loops(*lists):
		for each_list in lists:
			for i in each_list:
				i.loop()

	@staticmethod
	def run_loop(obj):
		obj.loop()

	def mainloop(self):
		while True:
			# quit events.
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					pygame.quit()
					sys.exit()
				# Player Control Events
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.player.moving_left = True
					if event.key == pygame.K_RIGHT:
						self.player.moving_right = True
					if event.key == pygame.K_t:
						self.player.speed = self.player.top_speed
					if event.key == pygame.K_SPACE:
						self.player.jump()
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT:
						self.player.moving_left = False
					if event.key == pygame.K_RIGHT:
						self.player.moving_right = False
					if event.key == pygame.K_t:
						self.player.speed = self.player.base_speed

			# Spawning
			self.spawn()
			# Drawing and loops
			self.screen.fill([0, 0, 0])
			self.run_loops(self.backgrounds)
			# pygame.draw.line(self.screen, [100, 0, 0], (0, self.ground_level), (self.width, self.ground_level))
			self.run_loops(self.structures, self.particles, self.obstacles, self.skills)
			self.run_loop(self.player)
			self.run_loops(self.foregrounds)
			self.run_loops(self.banners)
			self.run_loop(self.ui)
			pygame.display.update()
			pygame.time.Clock().tick(self.fps)

