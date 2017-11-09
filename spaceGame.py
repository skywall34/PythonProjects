import pygame
from pygame.locals import *
import sys
import random


class SpaceInvaders:
    def __init__(self): #fundamentals of the game
        self.score = 0
        self.lives = 2
        pygame.font.init()
        self.font = pygame.font.Font(None, 15) #assets/space_inaders.ttf
        self.barrierDesign = [[],[0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0],
                         [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
                         [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
                         [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                         [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1],
                         [1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1],
                         [1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1],
                         [1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1],
                         [1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1]]


        self.screen = pygame.display.set_mode((800,600))
        self.background = pygame.image.load("space.jpg")
        self.enemySprites = { #1 and 2 are when I want to create different aliens
            0: [pygame.image.load("alien.jpg").convert(), pygame.image.load("alien.jpg").convert()],
            1: [pygame.image.load("alien.jpg").convert(), pygame.image.load("alien.jpg").convert()],
            2: [pygame.image.load("alien.jpg").convert(), pygame.image.load("alien.jpg").convert()]
        }
        self.player = pygame.image.load("spacecraft.jpg").convert()
        self.animationOn = 0
        self.direction = 1 #direction of enemies
        self.enemySpeed = 20 #speed of enemy
        self.lastEnemyMove = 0 #create pixel movement(do if you want to)
        self.playerX  = 400 #initial location of player
        self.playerY = 530
        self.bullet = None #array for hero bullet
        self.bullets = [] #array for enemy bullets
        self.enemies = [] #array for enemies
        self.barrierParticles = [] #the barriers
        self.level = 0 #the levels
        self.hit = 0
        self.startY = 50
        self.startX = 50
        for rows in range(2):
            self.out = []
            if rows < 2:
                enemy = 0
            elif rows < 4:
                enemy = 1
            else:
                enemy = 2
            for columns in range(10):
                self.out.append((enemy, pygame.Rect(self.startX * columns, self.startY * rows, 35, 35)))
            self.enemies.append(self.out)
        self.chance = 900
        self.barrierX = 50
        self.barrierY =  400
        self.space = 100


    def createBarrier(self):
        for offset in range(1, 5):
            for b in self.barrierDesign:
                for b in b:
                    if b != 0:
                        self.barrierParticles.append(pygame.Rect(self.barrierX + self.space * offset, self.barrierY, 5, 5))
                    self.barrierX += 5
                self.barrierX = 50 * offset
                self.barrierY += 3
            self.barrierY = 400

    def enemyUpdate(self):
        if not self.lastEnemyMove:
            for enemy in self.enemies:
                for enemy in enemy:
                    enemy = enemy[1]
                    if enemy.colliderect(pygame.Rect(self.playerX, self.playerY, self.player.get_width(), self.player.get_height())):
                        self.lives -= 1
                        self.resetPlayer()
                    enemy.x += self.enemySpeed * self.direction
                    self.lastEnemyMove = 25 #needed to handle ok enemy shots
                    if enemy.x >= 750 or enemy.x <= 0:
                        self.moveEnemiesDown()
                        self.direction *= -1

                    chance = random.randint(0, 1000)
                    if self.level >= 1:
                        if self.level == 2:
                            self.chance = 750
                            if chance > self.chance:
                                self.bullets.append(pygame.Rect(enemy.x, enemy.y, 5, 10))
                                self.score += 1 #one point for each hit
                        else:
                            if chance > self.chance:
                                self.bullets.append(pygame.Rect(enemy.x, enemy.y, 5, 10))
                                self.score += 1  # one point for each hit
            if self.animationOn:
                self.animationOn -= 1
            else:
                self.animationOn += 1
        else:
            self.lastEnemyMove -= 1

    def moveEnemiesDown(self):
        for enemy in self.enemies:
            for enemy in enemy:
                enemy = enemy[1]
                enemy.y += 20

    def playerUpdate(self):
        key = pygame.key.get_pressed()
        if key[K_RIGHT] and self.playerX < 800 - self.player.get_width():
            self.playerX += 5
        elif key[K_LEFT] and self.playerX > 0:
            self.playerX -= 5
        if key[K_SPACE] and not self.bullet:
            self.bullet = pygame.Rect(self.playerX + self.player.get_width()/2 - 2, self.playerY - 15, 5, 10)

    def bulletUpdate(self):
        for i, enemy in enumerate(self.enemies):
            for j , enemy in enumerate(enemy):
                enemy = enemy[1]
                if self.bullet and enemy.colliderect(self.bullet):
                    self.enemies[i].pop(j)
                    self.bullet = None
                    self.chance -= 1
                    self.score += 100
                    self.hit += 1

        if self.bullet:
            self.bullet.y -= 20
            if self.bullet.y < 0:
                self.bullet = None

        for x in self.bullets:
            x.y += 20
            if x.y > 600:
                self.bullets.remove(x)
            if x.colliderect(pygame.Rect(self.playerX, self.playerY, self.player.get_width(), self.player.get_height())):
                self.lives -= 1
                self.bullets.remove(x)
                self.resetPlayer()

        for b in self.barrierParticles:
            check = b.collidelist(self.bullets)
            if check != -1:
                self.barrierParticles.remove(b)
                self.bullets.pop(check)
                self.score += 2 #difference to check code
            elif self.bullet and b.colliderect(self.bullet):
                self.barrierParticles.remove(b)
                self.bullet = None
                self.score += 2


    def resetPlayer(self):
        self.playerX = 400


    def run(self):
        pygame.display.set_caption('Forif Spacegame')
        clock = pygame.time.Clock()
        for x in range(3):
            self.moveEnemiesDown()
        while self.level <= 3:

            clock.tick(60)
            self.screen.fill((0,0,0))
            self.screen.blit(self.background, (0,0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            for enemy in self.enemies:
                for enemy in enemy: #scale() == resize to new resolution
                    self.screen.blit(pygame.transform.scale(self.enemySprites[enemy[0]][self.animationOn], (35, 35)), (enemy[1].x, enemy[1].y))
            self.screen.blit(self.player, (self.playerX, self.playerY))
            if self.bullet:
                pygame.draw.rect(self.screen, (52, 255, 0), self.bullet)
            for bullet in self.bullets:
                pygame.draw.rect(self.screen, (255, 255, 255), bullet)
            for b in self.barrierParticles:
                pygame.draw.rect(self.screen, (52, 255, 0), b)


            if self.hit == 20:
                for rows in range(2):
                    self.out = []
                    if rows < 2:
                        enemy = 0
                    elif rows < 4:
                        enemy = 1
                    else:
                        enemy = 2
                    for columns in range(10):
                        self.out.append((enemy, pygame.Rect(self.startX * columns, self.startY * rows, 35, 35)))
                    self.enemies.append(self.out)
                    for enemy in self.enemies:
                        for enemy in enemy:
                            self.screen.blit(pygame.transform.scale(self.enemySprites[enemy[0]][self.animationOn], (35, 35)), (enemy[1].x, enemy[1].y))
                self.level += 1
                self.hit = 0
                if self.level == 2:
                    self.lives = 1
                else:
                    self.lives = 2
                self.createBarrier()


            elif self.level == 3:
                self.screen.blit(pygame.font.Font(None, 100).render("You Win!", -1, (52, 255, 0)), (200, 200))
                self.screen.blit(pygame.font.Font(None, 100).render("Press x to exit", -1, (52, 255, 0)), (200, 300))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_x:
                            sys.exit()

            elif self.lives > 0:
                self.bulletUpdate()
                self.enemyUpdate()
                self.playerUpdate()
            elif self.lives == 0:
                self.screen.blit(pygame.font.Font(None, 100).render("You Lose!", -1, (52,255,0)), (200, 200))
                self.screen.blit(pygame.font.Font(None, 100).render("Press x to exit", -1, (52,255,0)), (200, 300))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_x:
                            sys.exit()


            self.screen.blit(self.font.render("Lives: {}".format(self.lives), -1, (255,255,255)), (20, 10))
            self.screen.blit(self.font.render("Score: {}".format(self.score), -1, (255, 255, 255)), (400, 10))
            pygame.display.flip()


if __name__ == "__main__":
    SpaceInvaders().run()



#when lives == 0 and level == 2 hard to press x since loop is infinite
#bullets are single for difficulty
#convert() creates a new copy with the pixel format changed

'''Rules
1. 3 levels, 2 lives for each level, single shot
2. Get hit -1 life, you have two lives
3. Aliens shoot at second level
4. barriers to hide behind appear at level 2
5. destroy all aliens to proceed
6. Defeat all 3 levels to win
7. Aliens shoot more often at level 3
'''
