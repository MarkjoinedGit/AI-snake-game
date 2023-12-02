
import pygame
import numpy as np
from map import *

CELL_SIZE = 10
WIDTH=1200
HEIGHT=600

CELL_NUMBER_X = WIDTH//CELL_SIZE
CELL_NUMBER_Y = HEIGHT//CELL_SIZE
ZERO_POS = 0
HEIGHT_NAVBAR = 50

SIZE_SNAKE_IMG=(CELL_SIZE,CELL_SIZE)
SIZE_FOOD_IMG=(CELL_SIZE,CELL_SIZE)
FPS=2000

GREEDY_ALGORITHM='GREEDY'
UCS_ALGORITHM='UCS'
BFS_ALGORITHM='BFS'
DFS_ALGORITHM='DFS'
ASTAR_ALGORITHM='A-STAR'
HILL_CLIMBING_ALGORITHM='HILL-CLIMBING'
IDS_ALGORITHM='IDS'
BASIC_MODE='Basic'

#MENU

BLACK = (0, 0, 0)
MENU_COLOR = (163,167,172)
WHITE = (255, 255, 255)
BODER_COLOR = (146,163,186)
NAVBAR_COLOR = (15,15,15)
GREEN_HOVER = (145, 254, 36)
BLACK_BLUE = (35, 45, 63)
BODER_WIDTH = 3
BODER_COLOR = WHITE

FOOD_IMG = (
    pygame.transform.scale(pygame.image.load(r'assets\foods\food-0.png'),SIZE_FOOD_IMG),
    pygame.transform.scale(pygame.image.load(r'assets\foods\food-1.png'),SIZE_FOOD_IMG),
    pygame.transform.scale(pygame.image.load(r'assets\foods\food-2.png'),SIZE_FOOD_IMG),
    pygame.transform.scale(pygame.image.load(r'assets\foods\food-3.png'),SIZE_FOOD_IMG),
    pygame.transform.scale(pygame.image.load(r'assets\foods\food-4.png'),SIZE_FOOD_IMG),
    pygame.transform.scale(pygame.image.load(r'assets\foods\food-5.png'),SIZE_FOOD_IMG),
    pygame.transform.scale(pygame.image.load(r'assets\foods\food-6.png'),SIZE_FOOD_IMG)   
)


SKIN_1= 'snake-blue'
SKIN_2= 'anaconda'
SKIN_3= 'crocodile'
SKIN_4= 'frog'
SKIN_5= 'pig'
SKIN_6= 'sheep'
SKIN_7= 'snake'
SKIN_8= 'unicorn'

ALGORITHM_MODE='Algorithm'

MODES={
    'Basic':BASIC_MODE,
    'Algorithm':ALGORITHM_MODE
}

MAPS={
    'Default':NO_MAP,
    'Easy':MAP0,
    'Normal':MAP1,
    'Difficult':MAP2
    }

SKINS={
    'snake-blue':SKIN_1,
    'anaconda':SKIN_2,
    'crocodile':SKIN_3,
    'frog':SKIN_4,
    'pig':SKIN_5,
    'sheep':SKIN_6,
    'snake':SKIN_7,
    'unicorn':SKIN_8
    }

ALGORITHMS= {
    'BFS':BFS_ALGORITHM,
    'DFS':DFS_ALGORITHM,
    'UCS':UCS_ALGORITHM,
    'GREEDY':GREEDY_ALGORITHM,
    'A-STAR':ASTAR_ALGORITHM,
    'HILL-CLIMBING':HILL_CLIMBING_ALGORITHM,
    'IDS': IDS_ALGORITHM
}

BACKGROUND_IMG=pygame.image.load(r'assets\background.png')

SIMULATION_IMG=pygame.image.load(r'assets\simulation.png')

PATH_IMG=pygame.image.load(r'assets\path.png')

OBSTACLE_IMG = pygame.transform.scale(pygame.image.load(r'assets\obstacle.png'),(CELL_SIZE,CELL_SIZE))



#212x152
WIDTH_BOARD = CELL_SIZE*CELL_NUMBER_X + CELL_SIZE*2
HEIGHT_BOARD = CELL_NUMBER_Y*CELL_SIZE + CELL_SIZE*2 + HEIGHT_NAVBAR
WIDTH_BORDER_BOARD = WIDTH_BOARD
HEIGHT_BORDER_BOARD = CELL_SIZE

# CLOSE_BTN_IMG = pg.image.load('close-btn.png')

POS_BORDER = [(ZERO_POS,HEIGHT_NAVBAR),(ZERO_POS, HEIGHT_BOARD - HEIGHT_BORDER_BOARD),(ZERO_POS,HEIGHT_NAVBAR),(WIDTH_BOARD - HEIGHT_BORDER_BOARD,HEIGHT_NAVBAR)]


LEFT="left"
RIGHT="right"
UP="up"
DOWN="down"

EMPTY = 0
FOOD = -1
HEAD = 1
OBSTACLE=-2

OBSTACLES_POS=set()

TIME_LIMIT=0.2
DEPTH_LIMIT = 10

DIRECTIONS = [(0, -1, LEFT), (-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN)]

DEPTH_OFFSET = 200

DEFAULT_FOOD = [
    (590, 330),
    (1030, 190),
    (670, 560),
    (640, 510),
    (600, 450),
    (660, 190),
    (830, 280),
    (540, 270),
    (150, 260), 
    (100, 200)
]

def posGame_to_posMatrix(a):
    return (a//CELL_SIZE)-1

def posMatrix_to_posGame(a):
    return (a+1)*CELL_SIZE

def posGame_to_posMatrix_list(l):
    return (np.array(l)//CELL_SIZE)-1

def posMatrix_to_posGame_list(l):
    return (np.array(l)+1)*CELL_SIZE

def path_to_pos(head_x,head_y,paths):
    pos=[]
    d={
        LEFT:(0, -1),
        RIGHT:(0, 1),
        UP:(-1, 0),
        DOWN:(1, 0),
    }
    x= posGame_to_posMatrix(head_x)
    y= posGame_to_posMatrix(head_y)
    for p in paths:
        y, x = y+d[p][0], x+d[p][1]
        pos.append(tuple(posMatrix_to_posGame_list((x,y))))
    return pos
