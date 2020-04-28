import pygame
import random
import math
import pickle
from pygame import mixer
from os import path


#Mix
pygame.mixer.init(22100, -16, 2, 64)
sound1=pygame.mixer.Sound("explosion.wav")
pygame.init()



# create the screen
screen = pygame.display.set_mode((800, 600))



# title and icon
pygame.display.set_caption("Smelly Dungeon")
icon = pygame.image.load("hat.png")
pygame.display.set_icon(icon)



# waves
level = 1
score_value = 0
score_total = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10
leveltextx = 10
leveltexty = 40

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
final_score = pygame.font.Font('freesansbold.ttf', 32)

def final_score_text():
    final_text = final_score.render('Final Score: ' + str(score_total), True,(255,255,255))
    screen.blit(final_text, (200, 350))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def showlevel(x,y):
    wave = font.render("Level : " + str(level), True,(255,255,255))
    screen.blit(wave, (x, y))
def showscore(x,y):
    score = font.render("Kills : " + str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

# attacks
blastimg = pygame.image.load('explosion.png')
blastx = 370
blasty = 480
blastmovex = 0
blastmovey = 1
blaststate = "ready"

# Player
playerimg = pygame.image.load('wizard.png')
playerx = 370
playery = 530
playermovex = 0
playermovey = 0

# Enemy
enemyimg = []
enemyx = []
enemyy = []
enemymovey = []
numberenemies = 6 + level

for i in range(numberenemies):
    enemyimg.append(pygame.image.load('skull.png'))
    enemyx.append(random.randint(50, 750))
    enemyy.append(random.uniform(-36, -200))
    enemymovey.append(0.05)

def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y):
    screen.blit(enemyimg[i], (x, y))


def firebullet(x, y):
    global blaststate
    blaststate = "fire"
    screen.blit(blastimg, (x + 16, y + 10))


def iscollision(enemyx, enemyy, blastx, blasty):
    distance = math.sqrt((math.pow(enemyx - blastx, 2)) + (math.pow(enemyy - blasty, 2)))
    if distance < 40:
        return True
    else:
        return False


# Game Loop

running = True
while running:
    f = open('score.txt', 'a')

    # Background rbg
    screen.fill((40, 40, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            f.write(str(score_total) + ', ')
            f.close()
            running = False

        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playermovex = -1
            if event.key == pygame.K_d:
                playermovex = 1
            if event.key == pygame.K_UP:
                if blaststate is "ready":
                    blast_sound = mixer.Sound('fire.wav')
                    blast_sound.play()
                    blastx = playerx
                    firebullet(blastx, blasty)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playermovex = 0

    # boundaries
    playerx += playermovex

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # enemy movement
    for i in range(numberenemies):

        #game over and saving score
        if enemyy[i] >500:
            for j in range(numberenemies):
                enemyy[j] = 2000
            game_over_text()
            final_score_text()
            break


        enemyy[i] += enemymovey[i]
        if enemyy[i] <= 0:
            enemymovey[i] = 0.05 * level
            # collision
        collision = iscollision(enemyx[i], enemyy[i], blastx, blasty)
        if collision:
            sound1.set_volume(0.08)
            sound1.play()
            blasty = 480
            blaststate = "ready"
            score_value += 1
            if score_value == 20:
                level = level + 1
                score_value = 0

            score_total += 1
            enemyx[i] = random.randint(50, 750)
            enemyy[i] = -100

        enemy(enemyx[i], enemyy[i])



    # attack movement
    if blasty <= 0:
        blasty = 480
        blaststate = "ready"

    if blaststate is "fire":
        firebullet(blastx, blasty)
        blasty -= blastmovey


    showscore(textx, texty)
    showlevel(leveltextx, leveltexty)
    player(playerx, playery)
    pygame.display.update()
