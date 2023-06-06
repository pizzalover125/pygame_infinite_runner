import pygame
import random

pygame.init()

# game constants
white = (255, 255, 255)
black = (0, 0, 0)
green = (144, 238, 144)
darkgreen = (121, 189, 121)
red = (255, 0, 0)
blue = (173, 216, 230)
magenta = (255, 0, 255)
WIDTH = 900  # Double the original width
HEIGHT = 600  # Double the original height

# game variables
score = 0
high_score = 0
start = 1

# player variables
player_x = 50
player_y = 400
y_change = 0
x_change = 0
gravity = 1
died = False

# obstacle variables
obstacles = [600, 900, 1200]  # Adjusted obstacle positions
obstacle_speed = 2
active = False
restart_allowed = True  # Flag to control restart
collision = False  # Flag to track collision

# game info
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Infinite Runner")
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)
background = darkgreen
fps = 60
font = pygame.font.Font("font.ttf", 64)
font2 = pygame.font.Font("font.ttf", 24)
font3 = pygame.font.Font("font.ttf", 8)
timer = pygame.time.Clock()

def restart_game():
    global active, died, collision, restart_allowed, obstacles, player_x, player_y, score, obstacle_speed
    active = True
    died = False
    collision = False
    obstacles = [600, 900, 1200]
    player_x = 50
    player_y = 400
    score = 0
    obstacle_speed = 2
    restart_allowed = False  # Prevent multiple restarts



running = True
while running:
    timer.tick(fps)
    screen.fill(background)

    if start == 1:  
        start_text = font2.render("Infinite Runner", True, black)
        start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(start_text, start_text_rect)

        start_text2 = font3.render("Press Space to Start", True, black)
        start_text_rect2 = start_text2.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 100))
        screen.blit(start_text2, start_text_rect2)


    # draw floor
    floor = pygame.draw.rect(screen, magenta, [0, 440, WIDTH, 440])

    if not active and died:
        if score > high_score:
            high_score = score

        end_text = font2.render("You have died...", True, black, background)
        end_text_rect = end_text.get_rect()
        end_text_x = WIDTH - end_text_rect.width - 10
        end_text_y = 10
        screen.blit(end_text, (end_text_x, end_text_y))

        score_text = font2.render(f"Score: {score}", True, black, background)
        score_text_rect = score_text.get_rect()
        score_text_x = WIDTH - score_text_rect.width - 10
        score_text_y = 100
        screen.blit(score_text, (score_text_x, score_text_y))

        high_score_text = font2.render(f"High Score: {high_score}", True, black, background)
        high_score_text_rect = high_score_text.get_rect()
        high_score_text_x = WIDTH - high_score_text_rect.width - 10
        high_score_text_y = 150
        screen.blit(high_score_text, (high_score_text_x, high_score_text_y))

        end_text2 = font2.render("Press Space to retry", True, black, background)
        end_text_rect2 = end_text2.get_rect()
        end_text_x2 = WIDTH - end_text_rect2.width - 10
        end_text_y2 = 200
        screen.blit(end_text2, (end_text_x2, end_text_y2))

    if active and not died:
        # draw score
        score_text = font.render(str(score), True, black, background)
        score_text_rect = score_text.get_rect()
        score_text_x = WIDTH - score_text_rect.width - 10
        score_text_y = 10
        screen.blit(score_text, (score_text_x, score_text_y))

    # draw player
    player = pygame.draw.rect(screen, green, [player_x, player_y, 40, 40])

    # draw obstacles
    obstacle0 = pygame.draw.rect(screen, magenta, [obstacles[0], 400, 40, 40])
    obstacle1 = pygame.draw.rect(screen, magenta, [obstacles[1], 400, 40, 40])
    obstacle2 = pygame.draw.rect(screen, magenta, [obstacles[2], 400, 40, 40])

    for event in pygame.event.get():
        # handle closing the window
        if event.type == pygame.QUIT:
            running = False

        # handle restarting
        if event.type == pygame.KEYDOWN and not active and restart_allowed:
            if event.key == pygame.K_SPACE:
                start = 0
                restart_game()

        # handle player controls
        if event.type == pygame.KEYDOWN and active and not collision:
            if event.key == pygame.K_UP and y_change == 0:
                y_change = 14
            if event.key == pygame.K_RIGHT:
                x_change = 4
            if event.key == pygame.K_LEFT:
                x_change = -4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and x_change > 0:
                x_change = 0
            if event.key == pygame.K_LEFT and x_change < 0:
                x_change = 0

    # handle obstacles
    for i in range(len(obstacles)):
        if active and not collision:
            obstacles[i] -= obstacle_speed
            if obstacles[i] < -40:
                obstacles[i] = random.randint(920, 1020)
                score += 1
            if (
                player.colliderect(obstacle0)
                or player.colliderect(obstacle1)
                or player.colliderect(obstacle2)
            ):
                active = False
                died = True
                collision = True
                restart_allowed = True  # Enable restart

    # handle player limits
    if 0 <= player_x <= 860 and not collision:
        player_x += x_change
    if player_x < 0:
        player_x = 0
    if player_x > 860:
        player_x = 860

    if y_change > 0 or player_y < 400:
        player_y -= y_change
        y_change -= gravity
    if player_y > 400:
        player_y = 400
    if player_y == 400 and y_change < 0:
        y_change = 0

    # make obstacles faster
    if obstacle_speed < 3.5:
        obstacle_speed *= 1.001

    pygame.display.flip()

pygame.quit()
