
import pygame
import numpy as np

CELL_SIZE = 5
WIDTH=500
HEIGHT=400

CELL_NUMBER_X = WIDTH//CELL_SIZE
CELL_NUMBER_Y = HEIGHT//CELL_SIZE
ZERO_POS = 0
HEIGHT_NAVBAR = 50
SIZE_SNAKE_IMG=(CELL_SIZE,CELL_SIZE)
SIZE_FOOD_IMG=(CELL_SIZE,CELL_SIZE)
FPS=120

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

BACKGROUND_IMG=pygame.image.load(r'assets\background.png')

SIMULATION_IMG=pygame.image.load(r'assets\simulation.png')

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

TIME_LIMIT=0.2
DEPTH_LIMIT = 10

DIRECTIONS = [(0, -1, LEFT), (-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN)]

GREEDY_ALGORITHM='greedy'
UCS_ALGORITHM='ucs'
BFS_ALGORITHM='bfs'
DFS_ALGORITHM='dfs'
ASTAR_ALGORITHM='a_star'
NO_ALGORITHM=''

def posGame_to_posMatrix(a):
    return (a//CELL_SIZE)-1

def posMatrix_to_posGame(a):
    return (a+1)*CELL_SIZE

def posGame_to_posMatrix_list(l):
    return (np.array(l)//CELL_SIZE)-1

def posMatrix_to_posGame_list(l):
    return (np.array(l)+1)*CELL_SIZE