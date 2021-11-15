# game options
TITLE = "Running Bunny"
WIDTH = 1000
HEIGHT = 500
PLAT_H = 120
FPS = 70
HS_FILE = "high_score.txt"
SPRITESHEET = "spritesheet_jumper.png"

# player
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.2
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

MONEY_SPAN = 20
ENIMY_SPAN = 10
GOLD_CAROOT_SPAN = 5

#platforms
PLATFORM_LIST = [(0, HEIGHT - PLAT_H, 0), 
                (350 , HEIGHT - PLAT_H, 1),
                (600, HEIGHT - PLAT_H, 0),
                (900, 260, 1),
                (1100, HEIGHT - PLAT_H, 0),
                (1300, HEIGHT - PLAT_H - 60, 0)
                ]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (0, 155, 155)
LIGHT_BLUE2 = (173,230,255)
DARK_BLUE = (8, 30, 48)
BG_COLOR = LIGHT_BLUE
