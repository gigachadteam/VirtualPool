# BROUGHT TO YOU WITH LOVE BY THE GIGACHAD TEAM <3

import pygame
import pymunk
import pymunk.pygame_util as pmg
import math

# Game Meta Data
DIM_WIDTH = 1200
DIM_HEIGHT = 678
BOTTOM_PANEL = 50
WINDOW_TITLE = "Virtual Pool"
GAME_ON = True

# Ball Data
BALL_MASS = 5
BALL_ELASTICITY = 0.8
BALL_DIAMETER = 36
pottedBalls = []
cuePotted = False

# Wall Data
CUSHION_ELASTICITY = 0.6
POCKET_DIAMETER = 70

# Shooting Data
TAKING_SHOT = True
POWERING_UP = False
MAX_FORCE = 10000
BAR_SENSTIVITY = 1000
FORCE_SENSITIVITY = 20
force = 0

# Initilize the modules
pygame.init()

# Setting up the window
screen = pygame.display.set_mode((DIM_WIDTH,DIM_HEIGHT + BOTTOM_PANEL))
pygame.display.set_caption(WINDOW_TITLE)

# Setting up the space for pymunk
space = pymunk.Space()
static_body = space.static_body
drawOptions = pmg.DrawOptions(screen)  # to draw on the screen


# Adding a clock to update calculations
clock = pygame.time.Clock()
FPS = 120

# Colors
BG = (50,50,50) # So there is no trail
BARCOLOR = (0 , 0 , 255)

# Load images
cueImage = pygame.image.load("gameAssets/Cue.png").convert_alpha()
tableImage = pygame.image.load("gameAssets/Table.png").convert_alpha()
ballImages =[]
for i in range (1,17):
    ballImage = pygame.image.load(f"gameAssets/Ball_{i}.png").convert_alpha()
    ballImages.append(ballImage)

# Create the body and shape of the ball
def createBall(radius, position):
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.mass = BALL_MASS
    shape.elasticity = BALL_ELASTICITY
    #use pivot joint to add friction
    pivot = pymunk.PivotJoint(static_body,body,(0,0),(0,0))
    pivot.max_bias= 0 #disable joint correction
    pivot.max_force= 1000 #emulate linear friction

    #edit created pivot added to apply friction
    space.add(body, shape, pivot)
    return shape

# Setup game balls
balls = []
rows = 5
# Putting the normal balls as a grid
for col in range(5):
    for row in range(rows):
        # the x is inital 250 + all the balls diameter + 1 pixel gap
        # the y is the all the balls diameter + all
        pos = (250 + (col * (BALL_DIAMETER+1)), 267 + (row  * (BALL_DIAMETER+1)) + (col * BALL_DIAMETER/2))
        new_ball = createBall(BALL_DIAMETER/2 , pos)
        balls.append(new_ball)
    rows -= 1

# Cue "white" ball created
pos = (888 , DIM_HEIGHT/2)
cueBall = createBall(BALL_DIAMETER / 2, pos)
balls.append(cueBall)

# Creating pockets
pockets = [
    (37,50),
    (600,50),
    (1162,50),
    (39,629),
    (603,629),
    (1162,625)
]

# Create pool table cushions
# Defining the pixel coordinets of the walls corner order = TR,BR,TL,BL _ wall order = TR,TL,BR,BL,L,R
cushions = [
    [(69, 44), (100, 77), (545, 77), (555, 44)],
  [(633, 44), (663, 78), (1108, 78), (1118, 44)],
  [(69, 631), (100, 598),(545, 598), (565, 631)],
  [(633, 631), (653, 598), (1108, 598), (1118, 631)],
  [(35, 96), (64, 127), (64, 560), (35, 591)],
  [(1163, 96), (1135, 127), (1135, 560), (1163, 571)]
]

def createCushion(poly_dims):
    body = pymunk.Body(body_type = pymunk.Body.STATIC) 
    shape = pymunk.Poly(body,poly_dims)
    shape.elasticity = CUSHION_ELASTICITY

    space.add(body, shape)

for c in cushions:
    createCushion(c)

# Creating the cue
class Cue():
    def __init__(self,pos):
        self.originalImage = cueImage #preserving the image before rotating
        self.angle = 0
        self.image = pygame.transform.rotate(self.originalImage, self.angle) # rotating the img
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
    def update(self, angle):
        self.angle = angle

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.originalImage, self.angle) # rotating the img
        surface.blit(self.image,
            (self.rect.centerx - self.image.get_width() / 2,
            self.rect.centery - self.image.get_height() / 2)
        )

# Placing the cue around the cueball
cue = Cue(balls[-1].body.position)

# Create the power bar
powerBar = pygame.Surface((10,20))
powerBar.fill(BARCOLOR)

# Game loop
while GAME_ON:

    clock.tick(FPS)
    space.step(1/FPS)

    # Fill background
    screen.fill(BG)

    # Draw images
    screen.blit(tableImage,(0,0)) # Table

    # Check potted
    for i,ball in enumerate(balls):
        for pocket in pockets:
            ballPocketDistanceX = abs(ball.body.position[0] - pocket[0])
            ballPocketDistanceY = abs(ball.body.position[1] - pocket[1])
            ballPocketDistance = math.sqrt((ballPocketDistanceX**2) + (ballPocketDistanceY**2))
            if (ballPocketDistance <= POCKET_DIAMETER/2):
                # Check if white
                if i == len(balls) - 1:
                    cuePotted = True
                    ball.body.position = (-444, -444)
                    ball.body.velocity = (0.0,0.0)
                else:
                    space.remove(ball.body)
                    balls.remove(ball)
                    pottedBalls.append(ballImages[i])
                    ballImages.pop(i)

    # Put potted balls in bottom panel
    for i, ball in enumerate (balls): # Ball
        screen.blit(ballImages[i], ((ball.body.position[0] - ball.radius),(ball.body.position[1])- ball.radius))

    # Check for no movment based on int velocity
    TAKING_SHOT = True
    
    for ball in balls: 
        if(int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0):
            TAKING_SHOT = False

    if TAKING_SHOT: # Cue

        if cuePotted:
            balls[-1].body.position = (888, DIM_HEIGHT/2)
            cuePotted = False

        mousePosition = pygame.mouse.get_pos()
    
        # Update the cue center to white center
        cue.rect.center = balls[-1].body.position

        # Calcuate the angle
        cueXDistance = balls[-1].body.position[0] - mousePosition[0]
        cueYDistance = -(balls[-1].body.position[1] - mousePosition[1]) # Inverted in pygame (increase as you go down)
        cueAngle = math.degrees(math.atan2(cueYDistance,cueXDistance))
        cue.update(cueAngle)
        cue.draw(screen)

        # Power up
        cueBallDistance = math.sqrt(math.pow((balls[-1].body.position[0]-mousePosition[0]),2) + math.pow((balls[-1].body.position[1]-mousePosition[1]),2)) # Calculate the distance between the ball and mouse

        if POWERING_UP:
            force = cueBallDistance * FORCE_SENSITIVITY
            if (force > MAX_FORCE):
                force = MAX_FORCE
            # Draw power bar
            for adjustment in range(math.ceil(force / BAR_SENSTIVITY)): #bar per power
                screen.blit(powerBar, (balls[-1].body.position[0] - 30 + adjustment * 15,balls[-1].body.position[1] + 30))
            
            
        elif not POWERING_UP and TAKING_SHOT:
            # Splitting the angle
            shotX = force * math.cos(math.radians(cueAngle))
            shotY = force * math.sin(math.radians(cueAngle))
            balls[-1].body.apply_impulse_at_local_point((-shotX,shotY),(0,0))
            force = 0

    # Draw bottom panel
    pygame.draw.rect(screen, BG, (0, DIM_HEIGHT, DIM_WIDTH, BOTTOM_PANEL))

    # Drawing scored goals
    for i, ball in enumerate(pottedBalls):
        screen.blit(ball, ((10 + (i * 50)),DIM_HEIGHT+10))

    # Note: for handling
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and TAKING_SHOT:
            POWERING_UP = True
                
        if event.type == pygame.MOUSEBUTTONUP and TAKING_SHOT:
            POWERING_UP = False

        if event.type == pygame.QUIT:
            GAME_ON = False

    if(len(pottedBalls) == 14):
        print("GG YOU WIN")
        GAME_ON = False
    # Display the objects
    #space.debug_draw(drawOptions)
    pygame.display.update()

pygame.quit()