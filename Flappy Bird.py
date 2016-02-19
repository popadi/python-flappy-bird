#!/usr/bin/env python

#Importing libraries
import os, sys, pygame, random, math
from pygame.locals import *

#Initializing pygame & mixer
pygame.init()
pygame.mixer.init()

#Global variables for the game
SCR_RES = pygame.display.Info()     #Screen resolution
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
                 
def load_images():
    #- Loading all the images required for the game from the images folder
    #and returning a dictionary of them as following:
       
    #'background_1' : day background
    #'bird' : the bird
    #'bird2' : the bird with the wings down
    #'pipe-up' : the pipe for the upper part
    #'pipe-down' : the pipe for the lower part
    #'ground' : the ground

    def load_image(img_file_name):
        #- Looking for images in the game's images folder (./images/)
        #- Loading the image and then converts it, because it speeds up
        #blitting; returning then the image to the dictionary
        #- For the background image, we load a random one, since we
        #have a day background a night background
        
        file_name = os.path.join('.', 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img

    return {'background': load_image('background_' + str(random.randint(1, 2)) + '.png'),
            'bird': load_image('bird.png'),
            'bird2': load_image('bird2.png'),    
            'pipe-up': load_image('pipe-up.png'), 
            'pipe-down': load_image('pipe-down.png'),
            'ground': load_image('ground.png')}

def draw_text(screen, text, y_pos, size):
    #Drawing a black text (bigger) and then a white text, smaller
    #over it to get the desired score effect
    font = pygame.font.Font("04b_19.TTF", size)
    score_text_b = font.render(str(text), 1, (0, 0, 0))
    score_text_w = font.render(str(text), 1, (255, 255, 255))

    x_pos_b = (WIDTH - score_text_b.get_width()) / 2
    x_pos_w = (WIDTH - score_text_w.get_width()) / 2
    screen.blit(score_text_b, (x_pos_b+2, y_pos-1))
    screen.blit(score_text_w, (x_pos_w, y_pos))

def main():
    #- Opening the game window in the center of the screen, setting the caption,
    #and setting the icon
    #- This is also the main function of the game which uses the other functions
    #and classes to run properly
    
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
    ############################################################################################

    #Let's end the game!
    end_the_game(screen, score)
       
def end_the_game(screen, score):
    #Draws a rectangle & shows the score & updates the highscore
    pygame.draw.rect(screen, (0, 0, 0), (23, HEIGHT / 2 - 77, 254, 154))
    pygame.draw.rect(screen, (239, 228, 150), (25, HEIGHT / 2 - 75, 250, 150))
    draw_text(screen, "Your score: " + str(score), 200, 35)
    
    f = open("highscore.txt", "r+")
    hs = int(f.readline())
    if(score > hs):
       hs = score
       f.seek(0)
       f.truncate()
       f.write(str(hs))
    f.close()
    
    draw_text(screen, "Highscore: " + str(hs), 250, 35)
    draw_text(screen, "Press space to restart", 335, 20)
    draw_text(screen, "Press esc to exit", 355, 20)
    
    #Updates the entire screen for the last time
    pygame.display.update()

    #Gets the keyboard events to se if the user wants to restart the game
    while True:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == K_SPACE:
                    main()
                elif e.key == K_ESCAPE:
                    exit()

def exit(): 
    pygame.display.quit()
    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    #- If this module had been imported, __name__ would be 'Flappy Bird';
    #otherwise, if it was executed (by double-clicking the file) we would call main
    main()
