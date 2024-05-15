#Import libraries
import pygame as pg
from pygame.sprite import Sprite
from settings import *
import sys
from os import path
 
#Import Sprite Class
from pygame.sprite import Sprite

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
 
#Player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.shield_active = False  # Flag to indicate if shield is active
        self.shield_duration = 1000  # Duration of shield in milliseconds
        self.shield_timer = 0  # Timer for shield duration
        self.dash_duration = 1

    def activate_shield(self): #added from ChatGPT
        """Activate the shield."""
        self.shield_active = True
        self.shield_timer = pg.time.get_ticks()  # Start the timer

    def update_shield(self):
        """Update the shield state."""
        if self.shield_active:
            # Check if shield duration has passed
            if pg.time.get_ticks() - self.shield_timer > self.shield_duration:
                self.shield_active = False  # Deactivate the shield
        def load_images(self):
       
            class Animated_sprite(Sprite):
                def __init__(self):
                 Sprite.__init__(self)
            self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
            self.load_images()
            self.image = self.standing_frames[0]
            self.jumping = False
            self.walking = False
            self.current_frame = 0
            self.last_update = 0
 
    #Input to move player
    #def move(self, dx = 0, dy = 0):
    #    self.x += dx
    #    self.y += dy
   
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if keys[pg.K_r]:
            self.activate_shield()  # Activate shield when R key is pressed. Added from ChatGPT.
        if keys[pg.K_SPACE]: #speed boost when space key pressed. got help from Tino.
            if self.dash_start_time == 0:
                self.dash_start_time = pg.time.get_ticks()
                self.image.fill(ORANGE)
            if pg.time.get_ticks() - self.dash_start_time < self.dash_duration * 100:
                self.vx *= 2
                self.vy *= 2     
        else:
            self.dash_start_time = 0
            self.image.fill(GREEN)
        if self.vx != 0 and self.vy !=0:
                self.vx * 0.7071
                self.vy * 0.7071
    #def collide_with_obj(self, group, kill):
    #    hits = pg.sprite.spritecollide(self, self.game.group, kill)
    #    if hits:
    #        self.rect.x.width += 25
    #        self.rect.y.width += 25

   
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, True)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                #print(hits[0].__class__.__name__)
                self.speed += 150 #changed from 
        
                
    def collide_with_Mob(self, group, kill):
        opponent_collision = pg.sprite.spritecollide(self, group, True)
        if opponent_collision:
            if str(opponent_collision[0].__class__.__name__) == "Mob":
                pg.quit()
                sys.exit()

    #Update player movement
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_Mob(self.game.mob, False)
 
#Wall class
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
 
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((10, 10))  # Adjust bullet size as needed
        self.image.fill(YELLOW)  # Adjust bullet color
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -game.player.bullet_speed  # Adjust bullet speed  
   
    def update(self):
        self.rect.y += self.speedy
        # Kill the bullet if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
