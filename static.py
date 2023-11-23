import pygame


FOOD_IMG = (
    pygame.image.load(r'assets\foods\food-0.png'),
    pygame.image.load(r'assets\foods\food-1.png'),
    pygame.image.load(r'assets\foods\food-2.png'),
    pygame.image.load(r'assets\foods\food-3.png'),
    pygame.image.load(r'assets\foods\food-4.png'),
    pygame.image.load(r'assets\foods\food-5.png'),
    pygame.image.load(r'assets\foods\food-6.png')   
)


SNAKE_BLOCK_IMG = pygame.image.load(r'assets\snake\body-snake-blue.png')

SNAKE_HEAD_IMG = {
    'left':pygame.image.load(r'assets\snake\head-snake-blue-left.png'),
    'right':pygame.image.load(r'assets\snake\head-snake-blue-right.png'),
    'up':pygame.image.load(r'assets\snake\head-snake-blue-up.png'),
    'down':pygame.image.load(r'assets\snake\head-snake-blue-down.png')
}

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


CELL_SIZE = 5
CELL_NUMBER_X = 210
CELL_NUMBER_Y = 140
ZERO_POS = 0
HEIGHT_NAVBAR = 50
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
DEPTH_LIMIT = 50

DIRECTIONS = [(0, -1, LEFT), (-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN)]

GREEDY_ALGORITHM='greedy'
UCS_ALGORITHM='ucs'
BFS_ALGORITHM='bfs'
DFS_ALGORITHM='dfs'
NO_ALGORITHM=''