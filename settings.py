# game options/settings
TITLE = "Platformer"
WIDTH = 1024 # 32*32
HEIGHT = 640 # 32 *20
TILESIZE = 32
FPS = 60
FONT_NAME = 'arial'

# Player properties
PLAYER_ACC = 1.2
PLAYER_FRICTION = -0.3
PLAYER_GRAV = 0.5
PLAYER_JUMP = 15

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (125, HEIGHT - 350, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
