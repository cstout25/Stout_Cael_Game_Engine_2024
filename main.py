# this file was created by: Cael Stout

import pygame as pg
import sys
from settings import *
from sprites import *
from random import randint
from os import path
from time import sleep

#Game class
class Game:
    #initialize method and game class
     def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.running = True
    #load save game data
     def load_data(self):
        game_folder = path.dirname (__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
                # print(enumerate(self.map_data))
   

     #init all variables, set up groups, instantiate classes
     def new(self):
        #print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mob = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            #print(row)
            for col, tile in enumerate(tiles):
                #print(col)
                if tile == '1':
                    #print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
    
    
    #define run method
     def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
   
   
    #quit game + close window
     def quit(self):
         pg.quit()
         sys.exit()
   
   
    #update sprite groups
     def update(self):
        self.all_sprites.update()
   
    #draw lines
     def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
   
    #draw grid
     def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

 
    #define input method
     def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            #if event.type == pg.KEYDOWN:
                #if event.key == pg.K_LEFT:
                    #self.player.move(dx=-1)
                #if event.key == pg.K_RIGHT:
                    #self.player.move(dx=1)
                #if event.key == pg.K_UP:
                    #self.player.move(dy=-1)
                #if event.key == pg.K_DOWN:
                    #self.player.move(dy=1)
   
     def show_start_screen(self):
         pass
   
     def show_go_screen(self):
         pass
         
 
#i have instantiated the Game class    
g = Game()
# g.show_start_screen()
 
while True:
     g.new()
     g.run()
     #g.show_go_screen()
 
def shoot(self):
    now = pg.time.get_ticks()
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE] and now - self.last_shot > self.shoot_delay:
        self.last_shot = now
    bullet = Bullet(self.rect.centerx, self.rect.centery, self.game)
    self.game.all_sprites.add(bullet)
    self.game.bullets.add(bullet)


#run game
g.run()