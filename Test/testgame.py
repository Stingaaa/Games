import time
import wave
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

shipProjectiles = []
enemies = []
waves = [5, 7, 9, 11, 13]
shootTimeout = 40
enemyTimeout = 10
waveNr = 0
waveCleared = True

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
    print(lenX)
    while e > 0:
        e -= 1
        en = pygame.Rect(lenX*(temp-e), -20, 60, 60)
        enemies.append(en)
        
def moveEnemies():
    global enemyTimeout
    i = 0
    if enemyTimeout < 0:
        for e in enemies:
            enemyTimeout = 10
            enemies.remove(e)
            pygame.draw.rect(DISPLAYSURF, (0,0,0), e) 
            e = e.move(0, 1)
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
        pygame.draw.rect(DISPLAYSURF, (0,0,0), ship) 
        ship = ship.move(-7, 0)
        pygame.draw.rect(DISPLAYSURF, color, ship)
    elif keyboard.is_pressed("d"):
        pygame.draw.rect(DISPLAYSURF, (0,0,0), ship) 
        ship = ship.move(7, 0)
        pygame.draw.rect(DISPLAYSURF, color, ship)
                
running = True
while running:
    time.sleep(0.03)
    shootTimeout -= 1
    enemyTimeout -= 1
    loadWave()
    moveBullets()
    moveShip()
    moveEnemies()
    pygame.display.update()
    if(rect.colliderect(ship)):
        pygame.quit()
    if keyboard.is_pressed("shift+esc"):
        running = False
    if keyboard.is_pressed("space"):
        shoot()
    if running == False:
        pygame.quit()