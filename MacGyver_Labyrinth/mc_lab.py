# coding: utf-8

import pygame
from pygame. locals import *

import constants
import classes

def main():
	"""Main function of the MacGyver maze profram"""
	
	#Pygame initialization
	pygame.init()

	#Game window properties
	width = constants.sprite_width_num * constants.sprite_size
	height = constants.sprite_height_num * constants.sprite_size
	window = pygame.display.set_mode((width, height))

	pygame.display.set_caption(constants.title) #Window title

	maze = classes.Maze() #maze creation from 'Maze' class
	#Game elements initialization
	hero_position = classes.Position(0, 0)
	guard_position = classes.Position(14, 14)
	macgyver = classes.Hero(hero_position)
	guard = classes.Guard(guard_position)
	objects = [classes.Ether(maze), classes.Needle(maze), classes.Tube(maze)]
	labyrinth_elements = [macgyver, guard] + objects
	
	proceed = 1
	stop = 1

	while proceed:
		pygame.time.Clock().tick(40) #Loop speed limit to not overload the processor (30 frames per second)
		
		for event in pygame.event.get():
				if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
					proceed = 0
					stop = 0
				if event.type == KEYDOWN:
					if event.key == K_RIGHT:
						macgyver.move("right", maze)
						macgyver.take_object(*objects)
					if event.key == K_LEFT:
						macgyver.move("left", maze)
						macgyver.take_object(*objects)
					if event.key == K_UP:
						macgyver.move("up", maze)
						macgyver.take_object(*objects)
					if event.key == K_DOWN:
						macgyver.move("down", maze)
						macgyver.take_object(*objects)

		#Show the labyrinth on the window
		window.fill((0,0,0)) #Reset the screen for the inventory
		maze.show(window)
		for element in labyrinth_elements:
			window.blit(element.image,(element.position.x, element.position.y))

		pygame.display.flip()

		if (macgyver.position.row, macgyver.position.column) == (guard.position.row, guard.position.column):
			proceed = 0

	start_tick = pygame.time.get_ticks() #Get a number of frames to display the win or loose image window
	while stop:
		time = (pygame.time.get_ticks() - start_tick)/1000
		classes.Endgame.win(macgyver, maze)
		#After 5 seconds close all the windows
		if time > 2:
			stop = 0

if __name__ == "__main__":
	main()
