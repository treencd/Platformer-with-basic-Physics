import pygame as pg
import csv
from settings import *


''' MAP Class
* this reads in your map data
TO DO:
- switch it to pytmx for reading in layered maps
'''
class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                self.data.append(list(row))
                
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

''' CAMERA Class
* receives a 'target' (the player), as well as the map tiles
* and moves the tiles at the players current speed relative to the window
'''
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)