import pygame as pg
import random
from os import path
import time
from sprites import *
from settings import *
from tilemap import *


class Game:
    def __init__(self):
        # initialize game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.dt = 0.0
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        # game monitoring
        self.player_death = False
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'maps/level1.csv'))

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.map_tiles = pg.sprite.Group()
        self.player = Player(self, WIDTH / 4, HEIGHT / 4)
        self.all_sprites.add(self.player)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    map_tile = Tile(self, col, row, GREEN)
                elif tile == '2':
                    map_tile = Tile(self, col, row, BLUE)

        self.camera = Camera(self.map.width, self.map.height)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        prev_time = time.time()
        while self.playing:
            # Compute delta time
            now = time.time()
            self.dt = round((now - prev_time) * 60, 2)
            prev_time = now
            # Set FPS
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.camera.update(self.player)
        # spawn monsters

        # check monster hits


    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # self.map_tiles.draw(self.screen)
        # self.player.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()