import pygame
import pymunk
import pymunk.pygame_util as pmg

#Game Meta Data
DIM_WIDTH = 1200
DIM_HEIGHT = 678
WINDOW_TITLE = "Virtual Pool"
gameOn = True
BALL_MASS = 5
BALL_ELASTICITY = 0.8
CUSHION_ELASTICITY = 0.8
BALL_DIAMETER = 36

#Initilize the modules
pygame.init()

#Setting up the window
screen = pygame.display.set_mode((DIM_WIDTH,DIM_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

#Setting up the space for pymunk
space = pymunk.Space()
static_body = space.static_body
drawOptions = pmg.DrawOptions(screen)  # to draw on the screen


#Adding a clock to update calculations
clock = pygame.time.Clock()
FPS = 120

#colors
bg = (50,50,50) # So there is no trail

#load images
table_image = pygame.image.load("gameAssets/Table.png").convert_alpha()

ballImages =[]
for i in range (1,17):
    ballImage = pygame.image.load(f"gameAssets/Ball_{i}.png").convert_alpha()
    ballImages.append(ballImage)

#Create the body and shape of the ball
def createBall(radius, position):
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.mass = BALL_MASS
    shape.elasticity = BALL_ELASTICITY
    #use pivot joint to add friction
    pivot = pymunk.PivotJoint(static_body,body,(0,0),(0,0))
    pivot.max_bias= 0 #disable joint correction
    pivot.max_force= 900 #emulate linear friction

    #edit created pivot added to apply friction
    space.add(body, shape, pivot)
    return shape

#setup game balls
balls = []
rows = 5
#Putting the normal balls as a grid
for col in range(5):
    for row in range(rows):
        # the x is inital 250 + all the balls diameter + 1 pixel gap
        # the y is the all the balls diameter + all
        pos = (250 + (col * (BALL_DIAMETER+1)), 267 + (row  * (BALL_DIAMETER+1)) + (col * BALL_DIAMETER/2))
        new_ball = createBall(BALL_DIAMETER/2 , pos)
        balls.append(new_ball)
    rows -= 1

#cue "white" ball created
pos = (888 , DIM_HEIGHT/2)
cueBall = createBall(BALL_DIAMETER / 2, pos)
balls.append(cueBall)

#create pool table cushions
# Defining the pixel coordinets of the walls corner order = TR,BR,TL,BL _ wall order = TR,TL,BR,BL,L,R
cushions = [
    [(69, 44), (89, 77), (545, 77), (565, 44)],
  [(633, 44), (653, 78), (1108, 78), (1128, 44)],
  [(69, 631), (89, 598),(545, 598), (565, 631)],
  [(633, 631), (653, 598), (1108, 598), (1128, 631)],
  [(35, 96), (64, 117), (64, 560), (35, 581)],
  [(1163, 96), (1135, 117), (1135, 560), (1163, 581)]
]

def createCushion(poly_dims):
    body = pymunk.Body(body_type = pymunk.Body.STATIC) 
    shape = pymunk.Poly(body,poly_dims)
    shape.elasticity = CUSHION_ELASTICITY

    space.add(body, shape)

for c in cushions:
    createCushion(c)
#Game loop
while gameOn:

    clock.tick(FPS)
    space.step(1/FPS)

    #fill background
    screen.fill(bg)

    #draw images
    screen.blit(table_image,(0,0))

    for i, ball in enumerate (balls):
        screen.blit(ballImages[i], ((ball.body.position[0] - ball.radius),(ball.body.position[1])- ball.radius))

    #Note: for handling
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            cueBall.body.apply_impulse_at_local_point((-1500,0),(0,0))
        if event.type == pygame.QUIT:
            gameOn = False
    
    # Display the objects
    #space.debug_draw(drawOptions)
    pygame.display.update()

pygame.quit()