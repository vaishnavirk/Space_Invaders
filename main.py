import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("SPACE INVADERS")
# Background
bgnd = pygame.image.load('bg.png')
# Icon
icon = pygame.image.load('sp(2).png')
pygame.display.set_icon(icon)
# Game over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)
# Scores
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
# to tell wehere score appears
textX = 10
textY = 10


def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    # true to say it should be shown on the screen
    # render then blit
    score = font.render("Score :" + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


# player ( just giving initial positions to player when the program starts)
playerimg = pygame.image.load('rocket.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
# For multiple enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 768))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
# Ready state - when you cant see the bullet
# Fire state - the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
# we will change x coordinate in while loop
bulletX = 0
# it will be where spaceship is
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    # to use bullet_state variable inside this function we need to declare it as global here
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Collision
def iscollision(enemyX, enemyY, bulletX, bulletY):
    dis = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if dis <= 27:
        return True
    else:
        False


# Game Loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    # background image added here
    screen.blit(bgnd, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if any key is pressed ie left or right

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state is "ready":
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                # Get the current x coordinate of spaceship and is ready s that it fires only when one bullet has reached end
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # changing the places of player when any key is pressed
    playerX += playerX_change
    # Boundary checking for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            # to make the enemy dissapear
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        # Boundary checking for enemy
        if enemyX[i] <= 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = 3
        elif enemyX[i] >= 736:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = -3

        # Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_Sound = mixer.Sound('explosion.wav')
            collision_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_val += 1

            # after the bullet hits the enemy change its position
            enemyX[i] = random.randint(0, 768)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # call the player method here as it should always be seen and call it after fill method
    player(playerX, playerY)

    # to display the score( since it has to persist on the screen call it in while
    show_score(textX, textY)

    # always after making any changes make an update
    pygame.display.update()
