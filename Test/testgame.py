from logging import exception
import random
from shutil import move
import time
from tkinter.tix import DirSelectBox
from black import diff
import pygame
import keyboard
from win32api import GetSystemMetrics
import pyautogui

rect = pygame.Rect(60,60,100,100)
ship = pygame.Rect(GetSystemMetrics(0)/2-50,900,100,100)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
color = (0,0,255)
hpColor = (242, 75, 41)
dmgColor = (153, 147, 145)
pierceColor = (169, 216, 245)
bulletColor = (192, 54, 235)
pygame.draw.rect(DISPLAYSURF, color, ship) 
pygame.display.flip()

setup = True
moveLeft = True
gameOver = False
won = False
score = 0
shipHP = 3
shipDmg = 1
shipPierce = 1
shipBullets = 1
shipProjectiles = []
projectileInfo = []
projectileAngle = []
enemyProjectiles = []
lootObjects = []
lootInfo = []
enemies = []
enemyStats = []
waves = [5, 7, 9, 11, 13]
shootTimeout = 40
attackTimeout = 50
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
        waveCleared = False
        enemies = waves[waveNr]
        waveNr += 1
        spawnEnemy(enemies)
        
def loadTest():
    spawnEnemy(100)
    
def spawnEnemy(e):
    lenX = 0
    help = int(e/10)
    rows = int(e/10)
    temp = e
    total = e
    checkRow = e
    spawned = 0
    pos = e
    while checkRow > 0:
        spawned -= 1
        if total > 10*(help):
            while temp > 10:
                if(temp > 10):
                    temp -= 10*rows
                    pos -= 10*rows
            lenX = GetSystemMetrics(0)/(temp+1)
        else:
            lenX = GetSystemMetrics(0)/(11)
        if checkRow % 10 == 0:
            rows -= 1
        if pos == 0:
            pos = 10
        en = pygame.Rect(lenX*pos, -20-(80*rows), 60, 60)
        pos -= 1
        checkRow -= 1
        total -= 1
        enemies.append(en)
        enemyStats.append("2")
        
moveCount = 40
        
def moveEnemies():
    global enemyTimeout, moveLeft, moveCount
    i = 0
    val = 0
    try:
        x = GetSystemMetrics(0)/waves[waveNr]
    except:
        x = GetSystemMetrics(0)/waves[waveNr]
    if enemyTimeout < 0:
        for e in enemies:
            enemyTimeout = 10
            if moveLeft == True:
                val = -7
                moveCount -= 1
                if(moveCount == 0):
                    moveLeft = False
                    moveCount = 40
            else:
                val = 7
                moveCount -= 1
                if(moveCount == 0):
                    moveLeft = True
                    moveCount = 40
            enemies.remove(e)
            pygame.draw.rect(DISPLAYSURF, (0,0,0), e)
            e = e.move(val*difficulty, 2*difficulty) 
            pygame.draw.rect(DISPLAYSURF, (0,255,0), e)
            enemies.insert(i, e)
            i += 1
            if e.y > 1080:
                pygame.draw.rect(DISPLAYSURF, (0,0,0), e)  
                enemies.remove(e) 
                i -= 1   
                        
def shoot():
    global shootTimeout, shipBullets
    if shootTimeout < 0:
        shots = shipBullets
        
        if shots == 1:
            bullet = pygame.Rect(ship.centerx-5, ship.centery-70+(30*shots), 10, 20)
            shipProjectiles.append(bullet)
            projectileInfo.append(str(shipPierce))
        else:
            while shots >= 1:
                anglePer = 90/(shipBullets+1)
                anglePro = anglePer * shots
                shots -= 1
                bullet = pygame.Rect(ship.centerx-5, ship.centery-70+(30*shots), 10, 20)
                shipProjectiles.append(bullet)
                projectileAngle.append(str(anglePro))
                projectileInfo.append(str(shipPierce))
                
        shootTimeout = 15
        
def enemyAttack():
    global attackTimeout, difficulty
    if attackTimeout < 0:
        attackTimeout = 50/difficulty
        for e in enemies:
            rand = random.randint(0,9)
            if rand == 5:
                bullet = pygame.Rect(e.centerx-5, e.centery+40, 10, 20)
                enemyProjectiles.append(bullet)
    
def moveBullets():
    i = 0
    if shipBullets == 1:
        for b in shipProjectiles:
            shipProjectiles.remove(b)
            pygame.draw.rect(DISPLAYSURF, (0,0,0), b) 
            #Bullet moves at max 20 pixels per movement tick
            b = b.move(0, -20)
            pygame.draw.rect(DISPLAYSURF, (255,0,0), b)
            shipProjectiles.insert(i, b)
            i += 1
            if b.y < 0:
                pygame.draw.rect(DISPLAYSURF, (0,0,0), b)  
                shipProjectiles.remove(b) 
                i -= 1
    else:
        for b in shipProjectiles:
            index = shipProjectiles.index(b)
            angle = float(projectileAngle[index])
            shipProjectiles.remove(b)
            projectileAngle.pop(index)
            pygame.draw.rect(DISPLAYSURF, (0,0,0), b) 
            #Bullet moves at max 20 pixels per movement tick
            
            dirX = 10.0 - (20.0/90.0)*angle
            dirY = 20.0 - abs(dirX)
            b = b.move(-dirX, -dirY)
            pygame.draw.rect(DISPLAYSURF, (255,0,0), b)
            shipProjectiles.insert(i, b)
            projectileAngle.insert(i, angle)
            i += 1
            if b.y < 0:
                pygame.draw.rect(DISPLAYSURF, (0,0,0), b)  
                shipProjectiles.remove(b) 
                i -= 1
    z = 0
    for b in enemyProjectiles:
        enemyProjectiles.remove(b)
        pygame.draw.rect(DISPLAYSURF, (0,0,0), b) 
        b = b.move(0, 10)
        pygame.draw.rect(DISPLAYSURF, (255,255,255), b)
        enemyProjectiles.insert(i, b)
        z += 1
        if b.y > 1060:
            pygame.draw.rect(DISPLAYSURF, (0,0,0), b)  
            enemyProjectiles.remove(b) 
            z -= 1
                       
def moveShip():
    global ship
    if keyboard.is_pressed("a"):
        if(ship.x > 0):
            pygame.draw.rect(DISPLAYSURF, (0,0,0), ship) 
            ship = ship.move(-10, 0)
            pygame.draw.rect(DISPLAYSURF, color, ship)
    elif keyboard.is_pressed("d"):
        if(ship.x < GetSystemMetrics(0)-100):
            pygame.draw.rect(DISPLAYSURF, (0,0,0), ship) 
            ship = ship.move(10, 0)
            pygame.draw.rect(DISPLAYSURF, color, ship)
            
def moveLoot():
    i = 0
    for l in lootObjects:
        info = lootObjects.index(l)
        lootObjects.remove(l)
        pygame.draw.rect(DISPLAYSURF, (0,0,0), l) 
        l = l.move(0, 10)
        if "HP" in lootInfo[info]:
            col = hpColor
        if "Dmg" in lootInfo[info]:
            col = dmgColor
        if "Pierce" in lootInfo[info]:
            col = pierceColor
        if "Bullet" in lootInfo[info]:
            col = bulletColor
        
        pygame.draw.rect(DISPLAYSURF, col, l)
        lootObjects.insert(i, l)
        i += 1
        if l.y > 1100:
            pygame.draw.rect(DISPLAYSURF, (0,0,0), l)  
            lootObjects.remove(l) 
            i -= 1
            
def checkCollisions():
    global score, gameOver, shipHP
    help = 0
    for b in enemyProjectiles:
        if(ship.colliderect(b)):
            scoreRect = pygame.Rect(GetSystemMetrics(0)-200, 0, 200, 100)
            screen.fill((0,0,0), scoreRect)
            screen.blit(font1.render("Score: " + str(score), True, (255,0,0)), (int(GetSystemMetrics(0))-200, 20))
            if shipHP > 1:
                shipHP -= 1
                pygame.draw.rect(DISPLAYSURF, (0,0,0), b)
                enemyProjectiles.pop(help)
            else:
                gameOver = True
        help += 1
    help = 0
    for e in enemies:
        help2 = 0
        for b in shipProjectiles:
            if(e.colliderect(b)):
                scoreRect = pygame.Rect(GetSystemMetrics(0)-200, 0, 200, 100)
                screen.fill((0,0,0), scoreRect)
                screen.blit(font1.render("Score: " + str(score), True, (255,0,0)), (int(GetSystemMetrics(0))-200, 20))
                if float(enemyStats[help]) > 0.01:
                    hp = int(enemyStats[help])
                    enemyStats.pop(help)
                    enemyStats.insert(help, hp-shipDmg)
                else:
                    score += 100
                    dropLoot(e)
                    enemyStats.pop(help)
                    enemies.remove(e)
                pygame.draw.rect(DISPLAYSURF, (0,0,0), e)
                pierce = int(projectileInfo[help2])
                if pierce == 1:               
                    shipProjectiles.remove(b)
                else:
                    pierce -= 1
                    projectileInfo.pop(help2)
                    projectileInfo.insert(help2, str(pierce))
                pygame.draw.rect(DISPLAYSURF, (0,0,0), b)
        if(e.colliderect(ship)):
            gameOver = True 
        if(e.y+60 > 1080):
            gameOver = True
        help += 1
    for l in lootObjects:
        if l.colliderect(ship):
            collectLoot()
            lootInfo.pop(lootObjects.index(l))
            lootObjects.remove(l)
            pygame.draw.rect(DISPLAYSURF, (0,0,0), l)
        if l.y > 1200:
            lootInfo.remove(lootObjects.index(l))
            lootObjects.remove(l)
            pygame.draw.rect(DISPLAYSURF, (0,0,0), l)

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
        
def dropLoot(e):
    rand = random.randint(0, 99)
    if(20 < rand < 30):
        loot = pygame.draw.rect(DISPLAYSURF, hpColor, e)
        lootObjects.append(loot)
        lootInfo.append("HP")
    if(40 < rand < 45):
        loot = pygame.draw.rect(DISPLAYSURF, dmgColor, e)
        lootObjects.append(loot)
        lootInfo.append("Dmg")  
    if(55 < rand < 58):
        loot = pygame.draw.rect(DISPLAYSURF, pierceColor, e)
        lootObjects.append(loot)
        lootInfo.append("Pierce")
    if(69 == rand):
        loot = pygame.draw.rect(DISPLAYSURF, bulletColor, e)
        lootObjects.append(loot)
        lootInfo.append("Bullet")      
        
def collectLoot():
    global shipHP, shipDmg, shipPierce, shipBullets
    info = lootInfo[0]
    num = 10
    
    if "HP" in info:
        num = 0
    if "Dmg" in info:
        num = 1
    if "Pierce" in info:
        num = 2
    if "Bullet" in info:
        num = 3
        
    if num == 0:
        shipHP += 1
    if num == 1:
        shipDmg += 0.33
    if num == 2:
        shipPierce += 1
    if num == 3:
        shipBullets += 1
        
tempX = GetSystemMetrics(0)
tempY = GetSystemMetrics(1)/2-50        
diffEasy = pygame.Rect(tempX/5-50,tempY,100,50)
diffMid = pygame.Rect(tempX/5*2-50,tempY,100,50)
diffHard = pygame.Rect(tempX/5*3-50,tempY,100,50)
diffGamer = pygame.Rect(tempX/5*4-50,tempY,100,50)

difficulty = 1     

def checkDiff():
    global difficulty, setup, shipDmg, shipBullets, shipPierce, shipHP
    if keyboard.is_pressed("g+o+d"):
        difficulty = 5
        shipDmg = 10
        shipHP = 1000
        shipBullets = 5
        shipPierce = 5
        setup = False
        screen.fill((0,0,0))
    if tempX/5-50 <= pyautogui.position()[0] <= tempX/5+50 and tempY <= pyautogui.position()[1] <= tempY+50:
        difficulty = 0.5
        setup = False
        screen.fill((0,0,0))
    if tempX/5*2-50 <= pyautogui.position()[0] <= tempX/5*2+50 and tempY <= pyautogui.position()[1] <= tempY+50:
        difficulty = 1
        setup = False
        screen.fill((0,0,0))
    if tempX/5*3-50 <= pyautogui.position()[0] <= tempX/5*3+50 and tempY <= pyautogui.position()[1] <= tempY+50:
        difficulty = 2
        setup = False
        screen.fill((0,0,0))
    if tempX/5*4-50 <= pyautogui.position()[0] <= tempX/5*4+50 and tempY <= pyautogui.position()[1] <= tempY+50:
        difficulty = 5
        setup = False
        screen.fill((0,0,0))
                
running = True
while running:
    if setup == True:
        screen.fill((0,0,0))
        screen.blit(font2.render("Choose Difficulty", True, (255,0,0)), (int(GetSystemMetrics(0)/2.0)-200, int(GetSystemMetrics(1)/2.0)-150))
        pygame.draw.rect(DISPLAYSURF, (255,0,255), diffEasy)
        screen.blit(font1.render("Easy", True, (10,226,255)), (tempX/5-30, tempY+8))
        pygame.draw.rect(DISPLAYSURF, (255,0,255), diffMid)
        screen.blit(font1.render("Normal", True, (10,226,255)), (tempX/5*2-45, tempY+8))
        pygame.draw.rect(DISPLAYSURF, (255,0,255), diffHard)
        screen.blit(font1.render("Hard", True, (10,226,255)), (tempX/5*3-30, tempY+8))
        pygame.draw.rect(DISPLAYSURF, (255,0,255), diffGamer)
        screen.blit(font1.render("Gamer", True, (10,226,255)), (tempX/5*4-40, tempY+8))
        checkDiff()
        pygame.display.update()
    else:
        time.sleep(0.03)
        shootTimeout -= 1
        enemyTimeout -= 1
        attackTimeout -= 1
        if gameOver == False:
            checkWin()
            loadWave()
            moveBullets()
            moveShip()
            moveEnemies()
            moveLoot()
            enemyAttack()
            checkCollisions()
            checkCleared()
        elif won == True:
            screen.fill((0,0,0))
            screen.blit(font2.render("You have won!", True, (255,0,0)), (int(GetSystemMetrics(0)/2.0)-200, int(GetSystemMetrics(1)/2.0)-50))
        else:
            screen.fill((0,0,0))
            screen.blit(font2.render("Your score: " + str(score), True, (255,0,0)), (int(GetSystemMetrics(0)/2.0)-200, int(GetSystemMetrics(1)/2.0)-50))
        pygame.display.update()
        if(rect.colliderect(ship)):
            pygame.quit()
        if keyboard.is_pressed("space"):
            shoot()
    if keyboard.is_pressed("shift+esc"):
            running = False
    if running == False:
        pygame.quit()