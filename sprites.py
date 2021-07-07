import pygame as pg
from settings import *
vec = pg.math.Vector2


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


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        # self.rect.center = (WIDTH / 2, HEIGHT / 4)
        self.step_size = vec(0, 0)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, PLAYER_GRAV)
        self.on_ground, self.is_jumping = False, False
        self.LEFT_KEY, self.RIGHT_KEY = False, False

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC

        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
       
    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.vel.y -= PLAYER_JUMP
            self.on_ground = False

    def horizontal_movement(self):
        self.acc.x = 0
        self.get_keys()
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel.x += self.acc.x * (self.game.dt ** 2)
        self.pos.x += (self.vel.x * self.game.dt) + (self.acc.x * .5) * (self.game.dt * self.game.dt)
        self.rect.x = self.pos.x
        # Map boundaries
        if self.pos.x > self.game.map.width - self.rect.w:
            self.pos.x = self.game.map.width - self.rect.w
        if self.pos.x < 0:
            self.pos.x = 0

    def vertical_movement(self):
        self.vel.y += self.acc.y * self.game.dt
        if self.vel.y > 20: self.vel.y = 20
        self.pos.y += (self.vel.y * self.game.dt) + (self.acc.y * 0.5) * (self.game.dt * self.game.dt)
        self.rect.bottom = self.pos.y
        # Map boundaries
        if self.pos.y > self.game.map.height - self.rect.h:
            self.pos.y = self.game.map.height - self.rect.h
            self.game.player_death = True
        if self.pos.y < 0:
            self.pos.y = 0

    def update(self):
        self.horizontal_movement()
        self.check_collisions_x()
        self.vertical_movement()
        self.check_collisions_y()

    def get_hits(self):
        hits = []
        for tile in self.game.map_tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def check_collisions_x(self):
        collisions = self.get_hits()
        for tile in collisions:
            if self.vel.x > 0:  # Hit tile moving right
                self.pos.x = tile.rect.left - self.rect.w
                self.rect.x = self.pos.x
            elif self.vel.x < 0:  # Hit tile moving left
                self.pos.x = tile.rect.right
                self.rect.x = self.pos.x

    def check_collisions_y(self):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits()
        for tile in collisions:
            if self.vel.y > 0:  # Hit tile from the top
                self.on_ground = True
                self.is_jumping = False
                self.vel.y = 0
                self.pos.y = tile.rect.top
                self.rect.bottom = self.pos.y
            elif self.vel.y < 0:  # Hit tile from the bottom
                self.vel.y = 0
                self.pos.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.pos.y
                