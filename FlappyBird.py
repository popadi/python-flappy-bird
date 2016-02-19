#!/usr/bin/env python

#Importing libraries
import os, sys, pygame, random, math
from pygame.locals import *
from gameVariables import *
from gameClasses import *
from gameFunctions import *
   
def main():
    #- Opening the game window in the center of the screen, setting the caption,
    #and setting the icon
    #- This is also the main function of the game which uses the other functions
    #and classes to run properly

    #Initializing pygame & mixer
    pygame.init()
    pygame.mixer.init()

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((SCR_RES.current_w - WIDTH) / 2, (SCR_RES.current_h - HEIGHT) / 2)
    screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.DOUBLEBUF, 32)
    pygame.display.set_caption("Flappy Bird")
    pygame.display.set_icon(pygame.image.load('images/icon.ico'))

    #Setting up some timers 
    clock = pygame.time.Clock()
    pygame.time.set_timer(EVENT_NEWPIPE, PIPE_ADD_INTERVAL)
    
    #Loading the images | Creating the bird | Creating the ground | Creating the pipes list | Initiating the score
    images = load_images()
    my_bird = Bird()
    my_ground = Ground(images['ground'])
    pipes = []
    score = 0
    wait = True
    
    #Loading the sounds
    jump_sound = pygame.mixer.Sound('sounds/jump.ogg')
    score_sound = pygame.mixer.Sound('sounds/score.ogg')
    dead_sound = pygame.mixer.Sound('sounds/dead.ogg')

    while(wait == True):
        #Draw everything and wait for the user to click to start the game
        #When we click somewhere, the bird will jump and the game will start
        screen.blit(images['background'], (0, 0))
        draw_text(screen, "Click to start", 285, 20)
        screen.blit(images['ground'], (0, HEIGHT - GROUND_HEIGHT))

        #Drawing a "floating" flappy bird
        my_bird.redraw(screen, images['bird'], images['bird2'])

        #Updating the screen
        pygame.display.update()

        #Checking if the user pressed left click or space and start (or not) the game
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN or (e.type == pygame.KEYDOWN and e.key == K_SPACE):
                my_bird.steps_to_jump = 15
                wait = False
    jump_sound.play()
    
    #Loop until...we die!
    while True:
        #Drawing the background
        screen.blit(images['background'], (0, 0))

        #Getting the mouse, keyboard or user events and act accordingly
        for e in pygame.event.get():
            if e.type == EVENT_NEWPIPE:
                p = PipePair(WIDTH, False)
                pipes.append(p)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                my_bird.steps_to_jump = BIRD_JUMP_STEPS
                jump_sound.play()
            elif e.type == pygame.KEYDOWN:
                if e.key == K_SPACE:
                    my_bird.steps_to_jump = BIRD_JUMP_STEPS
                    jump_sound.play()
                elif e.key == K_ESCAPE:
                    exit()

        #Tick! (new frame)
        clock.tick(FPS)

        #Updating the position of the pipes and redrawing them; if a pipe is not visible anymore,
        #we remove it from the list
        for p in pipes:
            p.x -= FRAME_ANIMATION_WIDTH
            if p.x <= - PIPE_WIDTH:
                pipes.remove(p)
            else:
                screen.blit(images['pipe-up'], (p.x, p.toph))
                screen.blit(images['pipe-down'], (p.x, p.bottomh))

        #Redrawing the ground
        my_ground.move_and_redraw(screen)
        
        #Updating the bird position and redrawing it
        my_bird.update_position()
        my_bird.redraw(screen, images['bird'], images['bird2'])

        #Checks for any collisions between the pipes, bird and/or the lower and the
        #upper part of the screen
        if any(p.check_collision((my_bird.bird_x, my_bird.bird_y)) for p in pipes) or my_bird.bird_y < 0 or my_bird.bird_y + BIRD_HEIGHT > HEIGHT - GROUND_HEIGHT:
            dead_sound.play()
            break

        #There were no collision if we ended up here, so we are checking to see if 
        #the bird went thourgh one half of the pipe's width; if so, we update the score
        for p in pipes:
            if(my_bird.bird_x > p.x and not p.score_counted):
                p.score_counted = True
                score += 1
                score_sound.play()

        #Draws the score on the screen
        draw_text(screen, score, 50, 35)
        
        #Updates the screen
        pygame.display.update()

    #We are dead now, so we make the bird "fall"
    while(my_bird.bird_y + BIRD_HEIGHT < HEIGHT - GROUND_HEIGHT):
        #Redraws the background
        screen.blit(images['background'], (0, 0))

        #Redrawing the pipes in the same place as when it died
        for p in pipes:
            screen.blit(images['pipe-up'], (p.x, p.toph))
            screen.blit(images['pipe-down'], (p.x, p.bottomh))

        #Draws the ground piece to get the rolling effect
        my_ground.move_and_redraw(screen)

        #Makes the bird fall down and rotates it
        my_bird.redraw_dead(screen, images['bird'])

        #Tick!
        clock.tick(FPS * 3)
    
        #Updates the entire screen
        pygame.display.update()

    #Let's end the game!
    if not end_the_game(screen, score):
        main()
    else:
        pygame.display.quit()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    #- If this module had been imported, __name__ would be 'Flappy Bird';
    #otherwise, if it was executed (by double-clicking the file) we would call main
    main()
