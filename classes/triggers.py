import pygame
import random


class Trigger:
	"""This class manages the trigger for a single event. It will look for certain
	conditions at which time it will take actions."""
	def __init__(self, game, attr, condition):
		self.game = game
		self.attr = attr
		self.condition = condition

	def loop(self):
		pass

