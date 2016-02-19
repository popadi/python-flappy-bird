#!/usr/bin/env python

import pygame, math, random
from gameVariables import *

class Bird:
    #- The class for the bird; the x position is always the same, we only
    #update the y position when we fall or jump, based on a formula
    def __init__(self):
        self.bird_x = WIDTH / 2 - BIRD_WIDTH
        self.bird_y = HEIGHT / 2 - BIRD_HEIGHT / 2
        self.steps_to_jump = 0

    #The formula used makes everything to move "smooth"
    def update_position(self):
        if self.steps_to_jump > 0:
            self.bird_y -= (1 - math.cos((BIRD_JUMP_STEPS - self.steps_to_jump) * math.pi)) * FRAME_BIRD_JUMP_HEIGHT 
            #self.bird_y -= FRAME_BIRD_JUMP_HEIGHT * (BIRD_JUMP_STEPS - self.steps_to_jump) / 5 ;
            self.steps_to_jump -= 1
        else:
            self.bird_y += FRAME_BIRD_DROP_HEIGHT

    #- When we redraw the bird on the game screen, we draw the wing-up or
    #the wing-down image, to create the "flapping" effect
    def redraw(self, screen, image_1, image_2):
        if pygame.time.get_ticks() % 500 >= 250 :
            screen.blit(image_1, (self.bird_x, self.bird_y))
        else:
            screen.blit(image_2, (self.bird_x, self.bird_y))

    #Rotating the bird to create the falling effect
    def redraw_dead(self, screen, image):
        self.bird_y += FRAME_BIRD_DROP_HEIGHT
        bird_rot = pygame.transform.rotate(image, HEIGHT / 2 - self.bird_y)
        screen.blit(bird_rot, (self.bird_x, self.bird_y))

class PipePair:
    #- The class for the pipes; the original x position is the margin of the
    #game window; the pipes moves FRAME_ANIMATION_WIDTH / FPS
    #- Every time, we generate two heights: one for the upper pipe
    #and one for the lower pipe, with the same exact space between
    #then, PIPES_SPACE
    #- score_counted tells us if we passed through the pipes succesfully and
    #we received the points
    
    def __init__(self, x, score_counted):
        self.x = WIDTH
        self.toph = random.randint(50, 250) - PIPE_MAX_HEIGHT
        self.bottomh = self.toph + PIPE_MAX_HEIGHT + PIPES_SPACE
        self.score_counted = score_counted

    #Check collision with the bird and return 1 or 0 (1 = collision, 0 = no collision)
    def check_collision(self, bird_position):
        bx, by = bird_position
        in_x_range = bx + BIRD_WIDTH > self.x and bx < self.x + PIPE_WIDTH
        in_y_range = by > self.toph + PIPE_MAX_HEIGHT and by + BIRD_HEIGHT < self.toph + PIPE_MAX_HEIGHT + PIPES_SPACE
        return in_x_range and not in_y_range

class Ground:
    #- A small class for the ground who seems to roll to the left
    #- It's just a image who has twice the width of the game screen,
    #but when it is reaching its end, we reset it
    
    def __init__(self, image):
        self.x = 0
        self.y = HEIGHT - GROUND_HEIGHT
        self.image = image

    def move_and_redraw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.x -= FRAME_ANIMATION_WIDTH
        if(self.x < - WIDTH):
            self.x = 0