import time
import pygame
import keyboard
from win32api import GetSystemMetrics

rect = pygame.Rect(60,60,100,100)
ship = pygame.Rect(500,500,100,100)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
color = (0,0,255) 
pygame.draw.rect(DISPLAYSURF, color, ship) 
pygame.display.flip()

moveLeft = True
gameOver = False
won = False
score = 0
shipProjectiles = []
enemies = []
waves = [5, 7, 9, 11, 13]
shootTimeout = 40
enemyTimeout = 10
waveNr = 0
waveCleared = True
wavesCleared = 0

screen = pygame.display.set_mode((int(GetSystemMetrics(0)), int(GetSystemMetrics(1))))
font1 = pygame.font.SysFont('Garamond', 30)
font2 = pygame.font.SysFont('Garamond', 70)

def loadWave():
    global waveCleared, waveNr
    if waveCleared:
        waveNr += 1
        waveCleared = False
        enemies = waves[waveNr]
        spawnEnemy(enemies)
    
def spawnEnemy(e):
    lenX = (GetSystemMetrics(0)/e)-30
    temp = e
    while e > 0:
        e -= 1
        en = pygame.Rect(lenX*(temp-e), -20, 60, 60)
        enemies.append(en)
        
def moveEnemies():
    global enemyTimeout, moveLeft
    i = 0
    val = 0
    if enemyTimeout < 0:
        for e in enemies:
            enemyTimeout = 10
            if moveLeft == True:
                val = -5
                if(enemies[0].x <= 100):
                    moveLeft = False
            else:
                val = 5
                if(enemies[0].x >= 260):
                    moveLeft = True
            enemies.remove(e)
            pygame.draw.rect(DISPLAYSURF, (0,0,0), e)
            e = e.move(val, 2) 
            pygame.draw.rect(DISPLAYSURF, (0,255,0), e)
            enemies.insert(i, e)
            i += 1
            if e.y > 1080:
                pygame.draw.rect(DISPLAYSURF, (0,0,0), e)  
                enemies.remove(e) 
                i -= 1   
                        
def shoot():
    global shootTimeout
    if shootTimeout < 0:
        bullet = pygame.Rect(ship.centerx-5, ship.centery-70, 10, 20)
        shipProjectiles.append(bullet)
        shootTimeout = 40
    
def moveBullets():
    i = 0
    for b in shipProjectiles:
        shipProjectiles.remove(b)
        pygame.draw.rect(DISPLAYSURF, (0,0,0), b) 
        b = b.move(0, -10)
        pygame.draw.rect(DISPLAYSURF, (255,0,0), b)
        shipProjectiles.insert(i, b)
        i += 1
        if b.y < 0:
            pygame.draw.rect(DISPLAYSURF, (0,0,0), b)  
            shipProjectiles.remove(b) 
            i -= 1
            
def moveShip():
    global ship
    if keyboard.is_pressed("a"):
        if(ship.x > 0):
            pygame.draw.rect(DISPLAYSURF, (0,0,0), ship) 
            ship = ship.move(-7, 0)
            pygame.draw.rect(DISPLAYSURF, color, ship)
    elif keyboard.is_pressed("d"):
        if(ship.x < GetSystemMetrics(0)-100):
            pygame.draw.rect(DISPLAYSURF, (0,0,0), ship) 
            ship = ship.move(7, 0)
            pygame.draw.rect(DISPLAYSURF, color, ship)
            
def checkCollisions():
    global score, gameOver
    for e in enemies:
        for b in shipProjectiles:
            if(e.colliderect(b)):
                score += 100
                scoreRect = pygame.Rect(GetSystemMetrics(0)-200, 0, 200, 100)
                screen.fill((0,0,0), scoreRect)
                screen.blit(font1.render("Score: " + str(score), True, (255,0,0)), (int(GetSystemMetrics(0))-200, 20))
                enemies.remove(e)
                pygame.draw.rect(DISPLAYSURF, (0,0,0), e)
                shipProjectiles.remove(b)
                pygame.draw.rect(DISPLAYSURF, (0,0,0), b)
        if(e.colliderect(ship)):
            gameOver = True 

def checkCleared():
    global waveCleared, wavesCleared, score
    if len(enemies) == 0:
        waveCleared = True
        wavesCleared += 1
        score += 500   

def checkWin():
    global gameOver, won
    if wavesCleared == len(waves):
        gameOver = True
        won = True         
                
running = True
while running:
    time.sleep(0.03)
    shootTimeout -= 1
    enemyTimeout -= 1
    if gameOver == False:
        loadWave()
        moveBullets()
        moveShip()
        moveEnemies()
        checkCollisions()
        checkCleared()
        checkWin()
    elif won == True:
        screen.fill((0,0,0))
        screen.blit(font2.render("You have won!", True, (255,0,0)), (int(GetSystemMetrics(0)/2.0)-200, int(GetSystemMetrics(1)/2.0)-50))
    else:
        screen.fill((0,0,0))
        screen.blit(font2.render("Your score: " + str(score), True, (255,0,0)), (int(GetSystemMetrics(0)/2.0)-200, int(GetSystemMetrics(1)/2.0)-50))
    pygame.display.update()
    if(rect.colliderect(ship)):
        pygame.quit()
    if keyboard.is_pressed("shift+esc"):
        running = False
    if keyboard.is_pressed("space"):
        shoot()
    if running == False:
        pygame.quit()