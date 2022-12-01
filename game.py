import pygame
import pymunk
import pymunk.pygame_util as pmg

#Game Meta Data
DIM_WIDTH = 1200
DIM_HEIGHT = 678
WINDOW_TITLE = "Virtual Pool"
gameOn = True
BALL_MASS = 5

#Initilize the modules
pygame.init()

#Setting up the window
screen = pygame.display.set_mode((DIM_WIDTH,DIM_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

#Setting up the space for pymunk
space = pymunk.Space()
drawOptions = pmg.DrawOptions(screen) # to draw on the screen

#Create the body and shape of the ball
def createBall(radius, position):
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.mass = BALL_MASS

    space.add(body, shape)
    return shape

new_ball = createBall(25,(300, 100))

#Game loop
while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
    
    # Display the objects
    space.debug_draw(drawOptions)
    pygame.display.update()

pygame.quit()