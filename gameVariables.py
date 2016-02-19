#!/usr/bin/env python
import pygame
from pygame.locals import *

#Global variables for the game
WIDTH = 300                         #Game window width
HEIGHT = 500                        #Game window height
FPS = 60                            #Frames per second

BIRD_HEIGHT = 35                    #Height of the bird
BIRD_WIDTH = 48                     #Width of the bird
BIRD_JUMP_STEPS = 15                #Number of pixels the bird jumps when pressing spce or left click
FRAME_BIRD_JUMP_HEIGHT = 4          #Pixels per frame
FRAME_BIRD_DROP_HEIGHT = 3          #Pixels per frame

GROUND_HEIGHT = 73                  #Height of the ground
PIPE_WIDTH = 52                     #Width of a pipe
PIPE_MAX_HEIGHT = 320               #Max height of a pipe
PIPES_SPACE = 4 * BIRD_HEIGHT       #Space between pipes
PIPE_ADD_INTERVAL = 2000            #Milliseconds

FRAME_ANIMATION_WIDTH = 2           #Pixels per frame
EVENT_NEWPIPE = USEREVENT + 1       #Custom event

pygame.init()
SCR_RES = pygame.display.Info()     #Screen resolution
pygame.quit()