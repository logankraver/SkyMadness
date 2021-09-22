"""
This game is a simple side scroller with a plane infinitely moving through 
the sky dodging projectiles and destroying enemies to accumulate money.

The game employs the pygame module in order to set up all aspects of the
game. Additionally, all sprites used in the game are custom made.

Author: Logan Kraver
Date: 5/12/2021
"""


import pygame as p
import pygame.freetype
import os
import random
import time
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

#intializing the game
p.init()

#initializing game clock
clock = p.time.Clock()

#screen
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000
screen = p.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

#random game events 
ADDFIREBALL = p.USEREVENT + 1
p.time.set_timer(ADDFIREBALL, 200)

ADDCLOUD = p.USEREVENT + 2
p.time.set_timer(ADDCLOUD, 500)

ADDENEMYPLANE = p.USEREVENT + 3
p.time.set_timer(ADDENEMYPLANE, 5000)

SHOOT = p.USEREVENT + 4
p.time.set_timer(SHOOT, 2000)


money = 0


#player class
class Player(p.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = p.image.load("plane.png").convert()
        self.size = self.surf.get_size()
        self.surf.set_colorkey((0,0,0))
        self.surf = p.transform.scale(self.surf, (int(self.size[0]*3), int(self.size[1]*3)))
        self.size = self.surf.get_size()
        self.rect = self.surf.get_rect()
        
       
    #movement
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -8)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 8)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-8, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(8, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


#bullet class
class Bullet(p.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.surf = p.Surface((5,2))
        self.surf.fill((26, 59, 1))
        self.rect = self.surf.get_rect(center = (player.rect.x + player.size[0] - 5, player.rect.y + player.size[1]/2))

    def update(self):
        self.rect.move_ip(10, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

#enemyplane class
enemyPosX = 0
enemyPosY = 0

class enemyPlane(p.sprite.Sprite):
    def __init__(self):
        super(enemyPlane, self).__init__()
        self.surf = p.Surface((40,15))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(center = (random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT)))
    
    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.right < SCREEN_WIDTH - 100:
            self.rect.right = SCREEN_WIDTH - 100

    def shoot(self):
        new_enemyBullet = enemyBullet()
        enemies.add(new_enemyBullet)
        all_sprites.add(new_enemyBullet)


#enemy bullet class
class enemyBullet(p.sprite.Sprite):
    def __init__(self):
        super(enemyBullet, self).__init__()
        self.surf = p.Surface((5,2))
        self.surf.fill((63, 0, 122))
        self.rect = self.surf.get_rect(center = (enemyPosX, enemyPosY))

    def update(self):
        self.rect.move_ip(-10,0)
        if self.rect.right < 0:
            self.kill()


#fireball class
class Fireball(p.sprite.Sprite):
    def __init__(self):
        super(Fireball, self).__init__()
        self.surf = p.image.load("fireball.png").convert()
        self.surf.set_colorkey((255, 255, 255))
        self.size = self.surf.get_size()
        self.surf = p.transform.scale(self.surf, (int(self.size[0]*1.5), int(self.size[1]*1.5)))
        self.rect = self.surf.get_rect(center = (random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT)))
        self.speed = random.randint(5,20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()



#cloud class
class Cloud(p.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = p.image.load("cloud.png").convert()
        self.surf.set_colorkey((255, 255, 255))
        self.size = self.surf.get_size()
        self.surf = p.transform.scale(self.surf, (int(self.size[0]*4), int(self.size[1]*4)))
        self.rect = self.surf.get_rect(center = (random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT)))
    
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

#defining sprites and sprite groups
player = Player()
enemies = p.sprite.Group()
clouds = p.sprite.Group()
bullets = p.sprite.Group()
destroyableEnemies = p.sprite.Group()
enemy_Planes = p.sprite.Group()
all_sprites = p.sprite.Group()
all_sprites.add(player)


#fonts
menu_font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Fonts","SFPixelateShaded-BoldObliqu.ttf")
menufont = p.freetype.Font(menu_font_path, 64)

stat_font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Fonts","SFPixelate.ttf")
statfont = p.freetype.Font(stat_font_path, 64)

#game states
gameState = True
level = 0  

"""
level values
Menu = 0
Game over = -1
First level = 1
"""


#mainLoop
while gameState:
    
    #global main loop
    for event in p.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                gameState = False
        elif event.type == QUIT:
            gameState = False
    pressed_keys = p.key.get_pressed()
    p.display.flip()
    clock.tick(30)

    #menu
    if level == 0:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                level = 1
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameState = False

        clouds.update()
        screen.fill((184, 238, 245))
        for cloud in clouds:
            screen.blit(cloud.surf, cloud.rect)
        menufont.render_to(screen, (SCREEN_WIDTH/2 - 500, SCREEN_HEIGHT/2), "CLICK ANYWHERE TO CONTINUE", (22, 0, 133) , None, size=64)

    #gameover
    elif level == -1:
        screen.fill((0,0,0))
        menufont.render_to(screen, (SCREEN_WIDTH/2 - 500, SCREEN_HEIGHT/2), "GAME OVER", (84, 11, 23), None, size=64)
        menufont.render_to(screen, (SCREEN_WIDTH/2 - 500, SCREEN_HEIGHT/2 + 300), "CLICK TO RESPAWN", (84, 11, 23), None, size=64)

        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                level = deathLevel
                player.rect = player.surf.get_rect(center = (0,0))

    #fireball
    elif level == 1:
        for event in p.event.get():
            if event.type == KEYDOWN:
                if event.key == p.K_f:
                    new_bullet = Bullet()
                    bullets.add(new_bullet)
                    all_sprites.add(new_bullet)
                elif event.key == K_ESCAPE:
                    gameState = False
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
            elif event.type == ADDFIREBALL:
                new_fireball = Fireball()
                enemies.add(new_fireball)
                all_sprites.add(new_fireball)
            elif event.type == ADDENEMYPLANE:
                new_enemyPlane = enemyPlane()
                enemies.add(new_enemyPlane)
                destroyableEnemies.add(new_enemyPlane)
                enemy_Planes.add(new_enemyPlane)
                all_sprites.add(new_enemyPlane)
            elif event.type == SHOOT:
                for shooter in enemy_Planes:
                    enemyPosX = shooter.rect.centerx
                    enemyPosY = shooter.rect.centery
                    shooter.shoot()

        screen.fill((184, 238, 245))
        bullets.update()
        enemies.update()
        clouds.update()
        player.update(pressed_keys)   
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        statfont.render_to(screen, (SCREEN_WIDTH - 155, 4), "Points:"+str(money), (0,0,0), None, size=24)

        if p.sprite.spritecollideany(player, enemies):
            deathLevel = level
            level = -1
            for enemy in enemies:
                enemy.kill()
            player.rect = player.surf.get_rect(center = (- 100, -100))

        if p.sprite.groupcollide(bullets, destroyableEnemies, True, True):
            money = money + 200


    


    

    


    

    
    