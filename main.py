import pygame
import random
import math

from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

# constant screen
screen = pygame.display.set_mode((900, 600))

# music
mixer.music.load('backmusic.mp3')
mixer.music.play(-1)

# title & icon
pygame.display.set_caption("Space War")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# background

backgroundImage = pygame.image.load('background.png')
bckImage = pygame.transform.scale(backgroundImage, (900, 600))

# player
playerImage = pygame.image.load('player.png')
playerX = 370
playerY = 500
playerX_change = 0

# enemy

enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
n = 7

for i in range(n):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(10, 730))
    enemyY.append(random.randint(10, 50))
    enemyX_change.append(5)
    enemyY_change.append(40)

# bullet
bulletImage = pygame.image.load('bullet.png')
bltImage = pygame.transform.scale(bulletImage, (32, 32))
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf', 30)
over = pygame.font.Font('freesansbold.ttf', 50)
textX = 10
textY = 10


def show_score(x, y):
    score_value = font.render("Your score : " + str(score), True, (250, 250, 250))
    screen.blit(score_value, (x, y))


def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


def background(x, y):
    screen.blit(bckImage, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bltImage, (x + 16, y + 10))


def game_over():
    over_text = over.render("GAME OVER ", True, (250, 250, 250))
    screen.blit(over_text, (300, 250))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    d = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if d < 27:
        return True
    else:
        return False


running = True
# loop game
while running:

    screen.fill((0, 0, 0))
    background(0, 0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -7
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('Shoot.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player position

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 836:
        playerX = 836

    # enemy position
    for i in range(n):

        # game over
        if enemyY[i] > 440:
            for j in range(n):
                enemyY[j] = 1500
            game_over()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] = enemyY[i] + enemyY_change[i]
        elif enemyX[i] >= 836:
            enemyX_change[i] = -4
            enemyY[i] = enemyY[i] + enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('blast.wav')
            explosion_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(10, 730)
            enemyY[i] = random.randint(10, 50)

        enemy(enemyX[i], enemyY[i], i)

    # bullet motion
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
