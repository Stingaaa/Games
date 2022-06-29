import random
import time
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
shipSpeed = 10
shipBullets = 1
shipProjectiles = []
projectileAngle = []
lootObjects = []
lootInfo = []

enemies = []
enemyStats = []
enemyProjectiles = []
enemyMovement = []

elite = []
eliteStats = []
eliteProjectiles = []
eliteMovement = []

boss = pygame.Rect(GetSystemMetrics(0)/2-50,0,100,100)
bossMoveTimeout = 17
bossProjectiles = []
bossProjectileAngle = []
bossProjectilesUlt = []
bossProjectileAngleUlt = []
bossAlive = False
bossHP = 0
bossAtk= 50
bossThrust = 200
bossUlt = 500

waves = []
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
        if waveCleared % 10 == 0:
            spawnBoss()
        
def generateWaves():
    w = 101
    while w > 0:
        waves.append(5+2*(101-w))
        w -= 1
    
def spawnEnemy(e):
    lenX = 0
    help = int(e/10)
    rows = int(e/10)
    temp = e
    total = e
    checkRow = e
    spawned = 0
    pos = e
    el = False
    while checkRow > 0:
        rand = random.randint(0,9)
        if rand == 5:
            el = True
        else:
            el = False
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
        if el == False:
            enemies.append(en)
            enemyStats.append("2")
            enemyMovement.append(True)
        else:
            elite.append(en)
            eliteStats.append("4")
            eliteMovement.append(True)
            
def spawnBoss():
    global boss, bossHP, bossAlive, bossAtk, bossThrust, bossUlt
    if (wavesCleared+1) % 10 == 0:
        boss.y = -100 - 100*int((wavesCleared+1)/10)
        bossAlive = True
        bossHP = 100 + 10*(wavesCleared+1)
        bossAtk = 60 - 3*((wavesCleared+1)/10)
        bossThrust = 200 - 10*((wavesCleared+1)/10)
        bossUlt = 500 - 25*((wavesCleared+1)/10)
                
moveCount = 1
        
def moveEnemies():
    global enemyTimeout, moveLeft, moveCount
    val = 0
    if enemyTimeout < 0:
        for e in enemies:
            tempE = e
            index = enemies.index(e)
            if e.x < 50:
                pygame.draw.rect(DISPLAYSURF, (0,0,0), e)
                e = e.move(100,0)
            elif e.x+60 > 1870:
                pygame.draw.rect(DISPLAYSURF, (0,0,0), e)
                e = e.move(-100,0)
            enemyTimeout = 10
            try:
                if bool(enemyMovement[index]) == True:
                    val = -7
                    moveCount -= 1
                    if(moveCount == 0):
                        enemyMovement.pop(index)
                        enemyMovement.insert(index, False)
                        moveCount = 40/difficulty
                else:
                    val = 7
                    moveCount -= 1
                    if(moveCount == 0):
                        enemyMovement.pop(index)
                        enemyMovement.insert(index, True)
                        moveCount = 40/difficulty
            except:
                print()
            enemies.remove(tempE)
            pygame.draw.rect(DISPLAYSURF, (0,0,0), e)
            e = e.move(val*difficulty, 2*difficulty) 
            pygame.draw.rect(DISPLAYSURF, (0,255,0), e)
            imgRaw = pygame.image.load("Space Invaders/enemy.png").convert()
            img = pygame.transform.scale(imgRaw, (e.width, e.height))
            screen.blit(img, e)
            enemies.insert(index, e)
            if e.y > 1080:
                pygame.draw.rect(DISPLAYSURF, (0,0,0), e)  
                enemies.remove(e) 
                 
        for e in elite:
                tempE = e
                index = elite.index(e)
                if e.x < 50:
                    pygame.draw.rect(DISPLAYSURF, (0,0,0), e)
                    e = e.move(100,0)
                elif e.x+60 > 1870:
                    pygame.draw.rect(DISPLAYSURF, (0,0,0), e)
                    e = e.move(-100,0)
                enemyTimeout = 10
                if bool(eliteMovement[index]) == True:
                    val = -7
                    moveCount -= 1
                    if(moveCount == 0):
                        eliteMovement.pop(index)
                        eliteMovement.insert(index, False)
                        moveCount = 40/difficulty
                else:
                    val = 7
                    moveCount -= 1
                    if(moveCount == 0):
                        eliteMovement.pop(index)
                        eliteMovement.insert(index, True)
                        moveCount = 40/difficulty
                elite.remove(tempE)
                pygame.draw.rect(DISPLAYSURF, (0,0,0), e)
                e = e.move(val*difficulty, 2*difficulty) 
                pygame.draw.rect(DISPLAYSURF, (255,255,0), e)
                imgRaw = pygame.image.load("Space Invaders/elite.png").convert()
                img = pygame.transform.scale(imgRaw, (e.width, e.height))
                screen.blit(img, e)
                elite.insert(index, e)
                if e.y > 1080:
                    pygame.draw.rect(DISPLAYSURF, (0,0,0), e)  
                    elite.remove(e)
                    
def moveBoss():
        global boss, bossMoveTimeout
        bossMoveTimeout -= 1
        if bossMoveTimeout < 0:
            bossMoveTimeout = 37
            pygame.draw.rect(DISPLAYSURF, (0,0,0), boss)
            boss = boss.move(0, 2*difficulty)
            pygame.draw.rect(DISPLAYSURF, (178, 98, 129), boss)
            imgRaw = pygame.image.load("Space Invaders/boss.png").convert()
            img = pygame.transform.scale(imgRaw, (boss.width, boss.height))
            screen.blit(img, boss)
                        
def shoot():
    global shootTimeout, shipBullets
    if shootTimeout < 0:
        shots = shipBullets
        while shots >= 1:
            anglePer = 90/(shipBullets+1)
            anglePro = anglePer * shots
            shots -= 1
            bullet = pygame.Rect(ship.centerx-5, ship.centery-70, 10, 20)
            shipProjectiles.append(bullet)
            projectileAngle.append(str(anglePro))
                
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
        for e in elite:
            rand = random.randint(0,7)
            if rand == 5:
                bullet = pygame.Rect(e.centerx-5, e.centery+40, 10, 20)
                eliteProjectiles.append(bullet)
                
def bossAttack():
    global bossAtk, bossThrust, bossUlt, boss
    bossAtk -= 1
    bossThrust -= 1
    bossUlt -= 1
    if bossAtk < 0:
        bossAtk = 60 - 3*((wavesCleared+1)/10)
        shots = 5
        burst = shots
        while shots >= 1:
            anglePer = 110/(burst+1)
            anglePro = anglePer * shots
            shots -= 1
            bullet = pygame.Rect(boss.centerx-7, boss.centery+50, 14, 30)
            bossProjectiles.append(bullet)
            bossProjectileAngle.append(str(anglePro))
    if bossThrust < 0:
        bossThrust = 200 - 10*((wavesCleared+1)/10)
        pygame.draw.rect(DISPLAYSURF, (0,0,0), boss)
        boss = boss.move(0, 50)
    if bossUlt < 0:
        bossUlt = 500 - 25*((wavesCleared+1)/10)
        shots = 7
        burst = shots
        while shots >= 1:
            anglePer = 90/(burst+1)
            anglePro = anglePer * shots
            shots -= 1
            bullet = pygame.Rect(boss.centerx-15, boss.centery+50, 30, 50)
            bossProjectilesUlt.append(bullet)
            bossProjectileAngleUlt.append(str(anglePro))
        
        
    
def moveBullets():
    i = 0
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
        imgRaw = pygame.image.load("Space Invaders/shipBullet.png").convert()
        img = pygame.transform.scale(imgRaw, (b.width, b.height))
        screen.blit(img, b)
        shipProjectiles.insert(index, b)
        projectileAngle.insert(index, angle)
        i += 1
        if b.y < 0:
            pygame.draw.rect(DISPLAYSURF, (0,0,0), b)  
            shipProjectiles.remove(b)
            projectileAngle.pop(index) 
            i -= 1
    i = 0
    for b in bossProjectiles:
        index = bossProjectiles.index(b)
        angle = float(bossProjectileAngle[index])
        bossProjectiles.remove(b)
        bossProjectileAngle.pop(index)
        pygame.draw.rect(DISPLAYSURF, (0,0,0), b) 
        #Bullet moves at max 20 pixels per movement tick
        
        dirX = 10.0 - (20.0/110.0)*angle
        dirY = 20.0 - abs(dirX)
        b = b.move(-dirX, dirY)
        pygame.draw.rect(DISPLAYSURF, (255,0,0), b)
        imgRaw = pygame.image.load("Space Invaders/bossBullet.png").convert()
        img = pygame.transform.scale(imgRaw, (b.width, b.height))
        screen.blit(img, b)
        bossProjectiles.insert(index, b)
        bossProjectileAngle.insert(index, angle)
        i += 1
        if b.y < 0:
            pygame.draw.rect(DISPLAYSURF, (0,0,0), b)  
            bossProjectiles.remove(b)
            bossProjectileAngle.pop(index) 
            i -= 1
    i = 0
    for b in bossProjectilesUlt:
        index = bossProjectilesUlt.index(b)
        angle = float(bossProjectileAngleUlt[index])
        bossProjectilesUlt.remove(b)
        bossProjectileAngleUlt.pop(index)
        pygame.draw.rect(DISPLAYSURF, (0,0,0), b) 
        #Bullet moves at max 20 pixels per movement tick
        
        dirX = 10.0 - (20.0/90.0)*angle
        dirY = 20.0 - abs(dirX)
        b = b.move(-dirX, dirY)
        pygame.draw.rect(DISPLAYSURF, (255,0,0), b)
        imgRaw = pygame.image.load("Space Invaders/bossUltBullet.png").convert()
        img = pygame.transform.scale(imgRaw, (b.width, b.height))
        screen.blit(img, b)
        bossProjectilesUlt.insert(index, b)
        bossProjectileAngleUlt.insert(index, angle)
        i += 1
        if b.y < 0:
            pygame.draw.rect(DISPLAYSURF, (0,0,0), b)  
            bossProjectilesUlt.remove(b)
            bossProjectileAngleUlt.pop(index) 
            i -= 1
    z = 0
    for b in enemyProjectiles:
        enemyProjectiles.remove(b)
        pygame.draw.rect(DISPLAYSURF, (0,0,0), b) 
        b = b.move(0, 10)
        pygame.draw.rect(DISPLAYSURF, (255,255,255), b)
        imgRaw = pygame.image.load("Space Invaders/enemyBullet.png").convert()
        img = pygame.transform.scale(imgRaw, (b.width, b.height))
        screen.blit(img, b)
        enemyProjectiles.insert(z, b)
        z += 1
        if b.y > 1060:
            pygame.draw.rect(DISPLAYSURF, (0,0,0), b)  
            enemyProjectiles.remove(b) 
            z -= 1
    y = 0
    for b in eliteProjectiles:
        eliteProjectiles.remove(b)
        pygame.draw.rect(DISPLAYSURF, (0,0,0), b) 
        b = b.move(0, 10)
        pygame.draw.rect(DISPLAYSURF, (255,255,255), b)
        imgRaw = pygame.image.load("Space Invaders/eliteBullet.png").convert()
        img = pygame.transform.scale(imgRaw, (b.width, b.height))
        screen.blit(img, b)
        eliteProjectiles.insert(z, b)
        y += 1
        if b.y > 1060:
            pygame.draw.rect(DISPLAYSURF, (0,0,0), b)  
            eliteProjectiles.remove(b) 
            y -= 1
                       
def moveShip():
    global ship
    if keyboard.is_pressed("a"):
        if(ship.x > 0):
            pygame.draw.rect(DISPLAYSURF, (0,0,0), ship) 
            ship = ship.move(-shipSpeed, 0)
            pygame.draw.rect(DISPLAYSURF, color, ship)
            imgRaw = pygame.image.load("Space Invaders/ship.png").convert()
            img = pygame.transform.scale(imgRaw, (ship.width, ship.height))
            screen.blit(img, ship)
    elif keyboard.is_pressed("d"):
        if(ship.x < GetSystemMetrics(0)-100):
            pygame.draw.rect(DISPLAYSURF, (0,0,0), ship) 
            ship = ship.move(shipSpeed, 0)
            pygame.draw.rect(DISPLAYSURF, color, ship)
            imgRaw = pygame.image.load("Space Invaders/ship.png").convert()
            img = pygame.transform.scale(imgRaw, (ship.width, ship.height))
            screen.blit(img, ship)
            
def moveLoot():
    i = 0
    for l in lootObjects:
        info = lootObjects.index(l)
        lootObjects.remove(l)
        pygame.draw.rect(DISPLAYSURF, (0,0,0), l) 
        l = l.move(0, 10)
        if "HP" in lootInfo[info]:
            col = hpColor
            imgRaw = pygame.image.load("Space Invaders/heart.png").convert()
        if "Dmg" in lootInfo[info]:
            col = dmgColor
            imgRaw = pygame.image.load("Space Invaders/bullet.png").convert()
        if "Speed" in lootInfo[info]:
            col = pierceColor
            imgRaw = pygame.image.load("Space Invaders/speed.png").convert()
        if "Bullet" in lootInfo[info]:
            col = bulletColor
            imgRaw = pygame.image.load("Space Invaders/multishot.png").convert()
        
        pygame.draw.rect(DISPLAYSURF, col, l)
        img = pygame.transform.scale(imgRaw, (l.width, l.height))
        screen.blit(img, l)
        lootObjects.insert(info, l)
        i += 1
        if l.y > 1100:
            pygame.draw.rect(DISPLAYSURF, (0,0,0), l)  
            lootObjects.remove(l) 
            i -= 1
            
def checkCollisions():
    global score, gameOver, shipHP, bossHP, bossAlive
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
    for b in eliteProjectiles:
        if(ship.colliderect(b)):
            scoreRect = pygame.Rect(GetSystemMetrics(0)-200, 0, 200, 100)
            screen.fill((0,0,0), scoreRect)
            screen.blit(font1.render("Score: " + str(score), True, (255,0,0)), (int(GetSystemMetrics(0))-200, 20))
            if shipHP > 1:
                shipHP -= 1
                pygame.draw.rect(DISPLAYSURF, (0,0,0), b)
                eliteProjectiles.pop(help)
            else:
                gameOver = True
        help += 1
    for b in bossProjectiles:
        if(ship.colliderect(b)):
            scoreRect = pygame.Rect(GetSystemMetrics(0)-200, 0, 200, 100)
            screen.fill((0,0,0), scoreRect)
            screen.blit(font1.render("Score: " + str(score), True, (255,0,0)), (int(GetSystemMetrics(0))-200, 20))
            gameOver = True
        help += 1
    for b in bossProjectilesUlt:
        if(ship.colliderect(b)):
            scoreRect = pygame.Rect(GetSystemMetrics(0)-200, 0, 200, 100)
            screen.fill((0,0,0), scoreRect)
            screen.blit(font1.render("Score: " + str(score), True, (255,0,0)), (int(GetSystemMetrics(0))-200, 20))
            gameOver = True
        help += 1
    help = 0
    for e in enemies:
        for b in shipProjectiles:
            if(e.colliderect(b)):
                scoreRect = pygame.Rect(GetSystemMetrics(0)-200, 0, 200, 100)
                screen.fill((0,0,0), scoreRect)
                screen.blit(font1.render("Score: " + str(score), True, (255,0,0)), (int(GetSystemMetrics(0))-200, 20))
                screen.blit(font1.render("Wave: " + str(waveNr), True, (255,0,0)), (20, 20))
                try:
                    if float(enemyStats[help]) > 0.01:
                        hp = int(enemyStats[help])
                        enemyStats.pop(help)
                        enemyStats.insert(help, hp-shipDmg)
                    else:
                        score += 100
                        dropLoot(e)
                        enemyMovement.pop(help)
                        enemyStats.pop(help)
                        enemies.remove(e)
                except:
                    print()
                pygame.draw.rect(DISPLAYSURF, (0,0,0), e)
                pygame.draw.rect(DISPLAYSURF, (0,0,0), b)
        if(e.colliderect(ship)):
            gameOver = True 
        if(e.y+60 > 1080):
            gameOver = True
        help += 1
    help = 0
    for el in elite:
        for b in shipProjectiles:
            if(el.colliderect(b)):
                scoreRect = pygame.Rect(GetSystemMetrics(0)-200, 0, 200, 100)
                waveRect = pygame.Rect(20, 0, 200, 100)
                screen.fill((0,0,0), scoreRect)
                screen.fill((0,0,0), waveRect)
                screen.blit(font1.render("Score: " + str(score), True, (255,0,0)), (int(GetSystemMetrics(0))-200, 20))
                screen.blit(font1.render("Wave: " + str(waveNr), True, (255,0,0)), (20, 20))
                try:
                    if float(eliteStats[help]) > 0.01:
                        hp = int(eliteStats[help])
                        eliteStats.pop(help)
                        eliteStats.insert(help, hp-shipDmg)
                    else:
                        score += 200
                        dropLoot(el)
                        eliteMovement.pop(help)
                        eliteStats.pop(help)
                        elite.remove(el)
                except:
                    print()
                pygame.draw.rect(DISPLAYSURF, (0,0,0), el)
                pygame.draw.rect(DISPLAYSURF, (0,0,0), b)
        if(el.colliderect(ship)):
            gameOver = True 
        if(el.y+60 > 1080):
            gameOver = True
        help += 1
    for b in shipProjectiles:
        if(b.colliderect(boss) and bossAlive):
            bossHP -= shipDmg
            if bossHP > 0:
                pygame.draw.rect(DISPLAYSURF, (0,0,0), b)
                projectileAngle.pop(shipProjectiles.index(b))
                shipProjectiles.remove(b)
            else:
                score += 1000*((wavesCleared+1)/10)
                dropLoot(boss)
                pygame.draw.rect(DISPLAYSURF, (0,0,0), boss)
                bossAlive = False
    if boss.colliderect(ship):
        gameOver = True
    if boss.y > 1080:
        gameOver = True
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
    if(15 < rand < 30):
        loot = pygame.draw.rect(DISPLAYSURF, hpColor, e)
        lootObjects.append(loot)
        lootInfo.append("HP")
    if(40 < rand < 48):
        loot = pygame.draw.rect(DISPLAYSURF, dmgColor, e)
        lootObjects.append(loot)
        lootInfo.append("Dmg")  
    if(55 < rand < 63):
        loot = pygame.draw.rect(DISPLAYSURF, pierceColor, e)
        lootObjects.append(loot)
        lootInfo.append("Speed")
    if(69 == rand):
        loot = pygame.draw.rect(DISPLAYSURF, bulletColor, e)
        lootObjects.append(loot)
        lootInfo.append("Bullet")      
        
def collectLoot():
    global shipHP, shipDmg, shipSpeed, shipBullets
    info = lootInfo[0]
    num = 10
    
    if "HP" in info:
        num = 0
    if "Dmg" in info:
        num = 1
    if "Speed" in info:
        num = 2
    if "Bullet" in info:
        num = 3
        
    if num == 0:
        shipHP += 1
    if num == 1:
        shipDmg += 0.33
    if num == 2:
        shipSpeed += 1
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
    global difficulty, setup, shipDmg, shipBullets, shipSpeed, shipHP, waveNr, wavesCleared
    if keyboard.is_pressed("g+o+d"):
        difficulty = 10
        waveNr = 9
        wavesCleared = 9
        shipDmg = 10
        shipHP = 1000
        shipBullets = 17
        shipSpeed = 20
        setup = False
        generateWaves()
        screen.fill((0,0,0))
    if tempX/5-50 <= pyautogui.position()[0] <= tempX/5+50 and tempY <= pyautogui.position()[1] <= tempY+50:
        difficulty = 0.5
        setup = False
        generateWaves()
        screen.fill((0,0,0))
    if tempX/5*2-50 <= pyautogui.position()[0] <= tempX/5*2+50 and tempY <= pyautogui.position()[1] <= tempY+50:
        difficulty = 1
        setup = False
        generateWaves()
        screen.fill((0,0,0))
    if tempX/5*3-50 <= pyautogui.position()[0] <= tempX/5*3+50 and tempY <= pyautogui.position()[1] <= tempY+50:
        difficulty = 2
        setup = False
        generateWaves()
        screen.fill((0,0,0))
    if tempX/5*4-50 <= pyautogui.position()[0] <= tempX/5*4+50 and tempY <= pyautogui.position()[1] <= tempY+50:
        difficulty = 5
        setup = False
        generateWaves()
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
            loadWave()
            moveShip()
            moveEnemies()
            loadWave()
            moveLoot()
            enemyAttack()
            checkCollisions()
            checkCleared()
            if bossAlive:
                bossMoveTimeout -= 1
                bossAttack()
                moveBoss()
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