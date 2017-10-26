import constants

import pygame
from pygame.locals import *

import random

class Position:
	"""Class which manages the elements' position in the labyrinth"""
	def __init__(self, row, column):
		self.row = row
		self.column = column
		#Position in pixels
		self.x = self.column * constants.sprite_size
		self.y = self.row * constants.sprite_size

class Maze:
	"""Class which initializes and displays the labyrinth on the screen"""

	LAB_STRUCTURE = [] #Class attribute initialized as an empty list to save the maze stucture

	def __init__(self):
		"""Method whic opens the labyrinth from an external file"""
		with open("labyrinth.txt", "r") as labyrinth:

			#Save the maze structure as a list in LAB_STRUCTURE list
			self.LAB_STRUCTURE = [
									[char for char in row if char != "\n"]
									for row in labyrinth
								]


	def show(self, window):
		"""Method which shows the maze on the screen"""
		wall_image = pygame.image.load(constants.wall).convert()
		floor_image = pygame.image.load(constants.floor).convert()
		for o, row in enumerate(self.LAB_STRUCTURE):
			for h, column in enumerate(row):
				position = Position(o,h)
				if self.LAB_STRUCTURE[o][h] == constants.wall_symbol:
					window.blit(wall_image,(position.x, position.y))
				else:
					self.LAB_STRUCTURE[o][h] == constants.floor_symbol
					window.blit(floor_image,(position.x, position.y))
		#Display inventory bar on the screen
		inventory = pygame.font.SysFont("objects", 25, False, True)
		mytext = "objects:".rjust(3) #to justify the text
		window.blit(inventory.render(mytext, True,(255,255,255)),(5,610))


class Characters:
	"""Class which creates MacGyver and the guard and manages their position"""
	def __init__(self, position):
		self.image = pygame.image.load(constants.guard).convert_alpha() #Image in transparency
		self.position = position


class Guard(Characters):
	"""Class which create the guard and manage his starting position"""


class Hero(Characters):
	"""Class which creates MacGyver, manages his initial position, his movements
		and his inventory
	"""

	def __init__(self, position):
		"""Method that created MacGyver in his initial position"""
		self.image = pygame.image.load(constants.macgyver).convert_alpha()
		self.position = position
		self.objects_num = 0 #MacGyver starts with 0 objects

	def move(self, direction, maze):
		"""Method that manages MacGyver's movements in the maze"""
		if direction == "right":
			if self.position.column < len(maze.LAB_STRUCTURE) -1:
				if maze.LAB_STRUCTURE[self.position.row][self.position.column +1] != constants.wall_symbol:
					self.position.column += 1
					self.position = Position(self.position.row, self.position.column)

		if direction == "left":
			if self.position.column > 0:
				if maze.LAB_STRUCTURE[self.position.row][self.position.column -1] != constants.wall_symbol:
					self.position.column -= 1
					self.position = Position(self.position.row, self.position.column)

		if direction == "up":
			if self.position.row > 0:
				if maze.LAB_STRUCTURE[self.position.row -1][self.position.column] != constants.wall_symbol:
					self.position.row -= 1
					self.position = Position(self.position.row, self.position.column)

		if direction == "down":
			if self.position.row < len(maze.LAB_STRUCTURE) -1:
				if maze.LAB_STRUCTURE[self.position.row +1][self.position.column] != constants.wall_symbol:
					self.position.row += 1
					self.position = Position(self.position.row, self.position.column)


	def take_object(self, *objects):
		"""Method that allows MacGyver to take the objects in the maze"""
		for item in objects:
			if(item.position.row, item.position.column) == (self.position.row, self.position.column):
				self.objects_num += 1
				if self.objects_num == 1:
					item.position = Position(15, 2)
				elif self.objects_num == 2:
					item.position = Position(15, 3)
				else:
					item.position = Position(15, 4)



class Item:
	"""Class that creates the objects to defeat the guard and provides to
		place them randomly in the maze
	"""

	def _place_random(self, maze):
		"""Method that place randomly the objects"""
		rand_pos_column = random.randint(0, len(maze.LAB_STRUCTURE) -1)
		rand_pos_row = random.randint(0, len(maze.LAB_STRUCTURE) -1)

		#Check if the case is free to allow the objects positioning
		while maze.LAB_STRUCTURE[rand_pos_row][rand_pos_column] != constants.floor_symbol:
			rand_pos_column = random.randint(0, len(maze.LAB_STRUCTURE) -1)
			rand_pos_row = random.randint(0, len(maze.LAB_STRUCTURE) -1)
		maze.LAB_STRUCTURE[rand_pos_row][rand_pos_column] = constants.object_symbol
		return Position(rand_pos_row, rand_pos_column)


class Ether(Item):
	"""Class which creates the ether object"""
	def __init__(self, maze):
		self.image = pygame.image.load(constants.ether).convert_alpha()
		self.position = self._place_random(maze)


class Needle(Item):
	"""Class which creates the needle"""
	def __init__(self, maze):
		self.image = pygame.image.load(constants.needle).convert_alpha()
		self.position = self._place_random(maze)


class Tube(Item):
	"""Class which creates the plastic tube"""
	def __init__(self, maze):
		self.image = pygame.image.load(constants.tube).convert_alpha()
		self.position = self._place_random(maze)



class Endgame:
	"""Class that defines the end of the game"""
	@classmethod
	def win(self, characters, maze):
		pygame.init()
		quit_game = pygame.display.set_mode((225, 225))
		if characters.objects_num == 3:
			quit_game.blit(pygame.image.load(constants.win).convert(), (0,0))
		else:
			quit_game.blit(pygame.image.load(constants.loose).convert(), (0,0))

		pygame.display.flip() #Refresh the window