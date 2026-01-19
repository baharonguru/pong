import pygame, random, sys
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
paddle1_speed = 8  # Default speed for player 1
paddle2_speed = 8  # Default speed for player 2
l_score = 0
r_score = 0

# canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Pong - Speed Control')


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    horz = random.randrange(2, 4)
    vert = random.randrange(1, 3)

    if right == False:
        horz = - horz

    ball_vel = [horz, -vert]


# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, l_score, r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT // 2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT // 2]
    l_score = 0
    r_score = 0
    if random.randrange(0, 2) == 0:
        ball_init(True)
    else:
        ball_init(False)


# draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score

    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH // 2, HEIGHT // 2], 70, 1)

    # update paddle's vertical position, keep paddle on the screen
    # Update paddle 1
    new_paddle1_y = paddle1_pos[1] + paddle1_vel
    # Keep paddle 1 within bounds
    if new_paddle1_y < HALF_PAD_HEIGHT:
        paddle1_pos[1] = HALF_PAD_HEIGHT
    elif new_paddle1_y > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle1_pos[1] = new_paddle1_y

    # Update paddle 2
    new_paddle2_y = paddle2_pos[1] + paddle2_vel
    # Keep paddle 2 within bounds
    if new_paddle2_y < HALF_PAD_HEIGHT:
        paddle2_pos[1] = HALF_PAD_HEIGHT
    elif new_paddle2_y > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    else:
        paddle2_pos[1] = new_paddle2_y

    # update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    # draw paddles and ball
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    # ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,
                                                                                 paddle1_pos[1] + HALF_PAD_HEIGHT, 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)

    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(
            paddle2_pos[1] - HALF_PAD_HEIGHT, paddle2_pos[1] + HALF_PAD_HEIGHT, 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)

    # update scores
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score " + str(l_score), 1, YELLOW)
    canvas.blit(label1, (50, 20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score " + str(r_score), 1, YELLOW)
    canvas.blit(label2, (470, 20))

    # Display speed controls
    speed_font = pygame.font.SysFont("Arial", 14)
    speed1_label = speed_font.render(f"P1 Speed: {paddle1_speed}", 1, WHITE)
    speed2_label = speed_font.render(f"P2 Speed: {paddle2_speed}", 1, WHITE)
    canvas.blit(speed1_label, (50, 50))
    canvas.blit(speed2_label, (470, 50))

    # Display controls
    controls_font = pygame.font.SysFont("Arial", 12)
    controls1 = controls_font.render("A/D: P1 speed", 1, WHITE)
    controls2 = controls_font.render("Left/Right: P2 speed", 1, WHITE)
    canvas.blit(controls1, (50, 370))
    canvas.blit(controls2, (420, 370))


# keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel, paddle1_speed, paddle2_speed

    if event.key == K_UP:
        paddle2_vel = -paddle2_speed
    elif event.key == K_DOWN:
        paddle2_vel = paddle2_speed
    elif event.key == K_w:
        paddle1_vel = -paddle1_speed
    elif event.key == K_s:
        paddle1_vel = paddle1_speed

    # Speed control for player 1 (A/D keys)
    elif event.key == K_a:
        paddle1_speed = max(2, paddle1_speed - 2)  # Decrease speed, minimum 2
        # Update velocity if currently moving
        if paddle1_vel != 0:
            paddle1_vel = -paddle1_speed if paddle1_vel < 0 else paddle1_speed
    elif event.key == K_d:
        paddle1_speed = min(20, paddle1_speed + 2)  # Increase speed, maximum 20
        # Update velocity if currently moving
        if paddle1_vel != 0:
            paddle1_vel = -paddle1_speed if paddle1_vel < 0 else paddle1_speed

    # Speed control for player 2 (Left/Right arrow keys)
    elif event.key == K_LEFT:
        paddle2_speed = max(2, paddle2_speed - 2)  # Decrease speed, minimum 2
        # Update velocity if currently moving
        if paddle2_vel != 0:
            paddle2_vel = -paddle2_speed if paddle2_vel < 0 else paddle2_speed
    elif event.key == K_RIGHT:
        paddle2_speed = min(20, paddle2_speed + 2)  # Increase speed, maximum 20
        # Update velocity if currently moving
        if paddle2_vel != 0:
            paddle2_vel = -paddle2_speed if paddle2_vel < 0 else paddle2_speed


# keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel

    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0


init()

# game loop
while True:

    draw(window)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps.tick(60)
