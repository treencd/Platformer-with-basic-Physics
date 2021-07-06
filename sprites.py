import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        # self.rect.center = (WIDTH / 2, HEIGHT / 4)
        self.step_size = vec(0, 0)
        self.pos = vec(self.x, self.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.update_rects()

    def update_rects(self):
        self.x = self.rect.x
        self.y = self.rect.y
        self.rectTop = pg.Rect(self.x, self.y, self.width, 10)
        self.rectLeft = pg.Rect(self.x, self.y + 10, 10, self.height - 20)
        self.rectRight = pg.Rect(self.x + self.width - 10, self.y + 10, 10, self.height - 20)
        self.rectBottom = pg.Rect(self.x, self.y + self.height - 10, self.width, 10)

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # for event in pg.event.get():
        #     if event.type == pg.KEYDOWN:
        #         if event.key == pg.K_SPACE:
        #             self.jump()

    def collide_with_walls(self):
           #check for collision
            for tile in self.game.map_tiles:
                #check for collision in x direction
                if tile.rect.colliderect(self.rect.x + self.step_size.x * (60 / FPS), self.rect.y, self.width, self.height):
                    if self.vel.x < 0:
                        self.pos.x = tile.rect.right
                        print("left collision")
                    elif self.vel.x > 0:
                        self.pos.x = tile.rect.left - self.width
                        print("right collision")
                #check for collision in y direction
                if tile.rect.colliderect(self.rect.x, self.rect.y + self.step_size.y * (60 / FPS), self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel.y < 0:
                        print("top collision")
                        self.pos.y = tile.rect.bottom + self.height
                        print(tile.rect.bottom)
                        self.vel.y = 0
                    #check if above the ground i.e. falling
                    elif self.vel.y >= 0:
                        self.pos.y = tile.rect.top
                        self.vel.y = 0
            
    
    def jump(self):
        # jump only if standing on a platform
        self.jumping = False
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.map_tiles, False)
        self.rect.y -= 1
        if hits:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.get_keys()
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION 
        # equations of motion
        self.vel += self.acc * (60 / FPS) #* round(self.game.dt, 2)
        if abs(self.vel.x) < 0.1: self.vel.x = 0
        self.step_size = self.vel + 0.5 * self.acc #* round(self.game.dt/1.65, 2)
        self.pos += self.step_size * (60 / FPS) #round(self.game.dt, 2) # * (FPS / 60)
        self.collide_with_walls()
        # Map boundaries
        if self.pos.x > self.game.map.width - self.rect.w:
            self.pos.x = self.game.map.width - self.rect.w
        if self.pos.x < 0:
            self.pos.x = 0
        
        print(self.pos.y)
        self.rect.bottomleft = self.pos
        self.update_rects()
        

class Tile(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.groups = game.map_tiles, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE