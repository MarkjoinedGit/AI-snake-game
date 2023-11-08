from typing import Any
import pygame as pg
from pygame.sprite import Group
import my_color as col
import my_buttons as btn

#MENU
menu_width, menu_height = 657, 683
menu_x = -menu_width  # Đặt menu ẩn ban đầu
menu_y = 50

black = (0, 0, 0)
menu_color = (163,167,172)
WHITE = (255, 255, 255)
BORDER_COLOR = (146,163,186)
NAVBAR_COLOR = (15,15,15)

border_width = 3
border_color = WHITE

menu_surface = pg.Surface((menu_width, menu_height))
menu_surface.fill(menu_color)

CELL_SIZE = 20
CELL_NUMBER_X = 50
CELL_NUMBER_Y = 33

ZERO_POS = 0
HEIGHT_NAVBAR = 50

WIDTH_BOARD = CELL_SIZE*CELL_NUMBER_X + CELL_SIZE*2
HEIGHT_BOARD = CELL_NUMBER_Y*CELL_SIZE + CELL_SIZE*2 + HEIGHT_NAVBAR

WIDTH_BORDER_BOARD = WIDTH_BOARD
HEIGHT_BORDER_BOARD = CELL_SIZE

CLOSE_BTN_IMG = pg.image.load('close-btn.png')

pos_border = [(ZERO_POS,HEIGHT_NAVBAR),(ZERO_POS, HEIGHT_BOARD - HEIGHT_BORDER_BOARD),(ZERO_POS,HEIGHT_NAVBAR),(WIDTH_BOARD - HEIGHT_BORDER_BOARD,HEIGHT_NAVBAR)]

def draw_sub_menu(menu_list, btn_sub_algorithm_list, menu_open):
    screen.blit(sub_menu_surf, sub_mode_rect)
    screen.blit(sub_menu_surf, sub_algorithm_rect)
    for btn in menu_list:
        btn.draw(menu_open, menu_open)
        
    for btn in btn_sub_algorithm_list:
        btn.draw(menu_open, menu_open)
        
    if menu_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
        menu_open = False
    else:
        menu_open = True
    return menu_open

pg.init()
screen = pg.display.set_mode((WIDTH_BOARD, HEIGHT_BOARD))
pg.display.set_caption('Snather')
clock = pg.time.Clock()
pg.display.flip()

#menu
menu_surf = pg.image.load(r'assets\menu\menu-bg.png').convert()
menu_rect = menu_surf.get_rect(topleft = (0, 47.73))
sub_menu_surf = pg.image.load(r'assets\menu\sub-menu-bg.png').convert_alpha()
sub_mode_rect = sub_menu_surf.get_rect(topleft=(0, 48))
sub_algorithm_rect = sub_menu_surf.get_rect(topleft=(300, 48))
menu_mode = True

#borders
border_horizontal_top = pg.Surface((WIDTH_BORDER_BOARD, HEIGHT_BORDER_BOARD))
border_horizontal_top.fill(BORDER_COLOR)
border_horizontal_bottom = border_horizontal_top
border_vertical_left = pg.transform.rotate (border_horizontal_top, 90)
border_vertical_right = border_vertical_left

def drawBorderBoard():
    screen.blit(border_horizontal_top,pos_border[0])
    screen.blit(border_horizontal_bottom,pos_border[1])
    screen.blit(border_vertical_left,pos_border[2])
    screen.blit(border_vertical_right,pos_border[3])

#nav_bar
navbar = pg.Surface((WIDTH_BOARD,HEIGHT_NAVBAR))
navbar.fill(NAVBAR_COLOR)

#logo
logo_surf = pg.image.load(r'assets\nav-bar\logo.png').convert_alpha()
logo_rect = logo_surf.get_rect(center=(60, 23.865))
#button
btn_image = r'assets\btn.png'
btn_surf = pg.image.load(btn_image).convert_alpha()
btn_rect = btn_surf.get_rect(center=(525, 375))
btn_list_func = ['MENU', '0', 'PLAY', 'NEW']
btn_list_mode = ['Basic', 'Auto play', 'Solo machine', 'Machine vs Machine', 'Slither.io']
btn_list_algorithm = ['BFS', 'Greedy', 'UCS', 'A*']
#text_font 
text_font = pg.font.Font(r'assets\font\Inknut_Antiqua\InknutAntiqua-Bold.ttf', 18)

#buttons
btn_menu_list = []
for i in range(len(btn_list_func)):
    button = btn.Button(screen, text_font, f'{btn_list_func[i]}', 100, 40, (200 +i*200, 5), True, col.WHITE, col.GREEN_HOVER, col.WHITE, col.GREEN_HOVER)
    btn_menu_list.append(button)

#buttons_sub_menu_mode
btn_sub_mode_list = []
for i in range(len(btn_list_mode)):
    button = btn.Button(screen, text_font, f'{btn_list_mode[i]}', 280, 76, (0, 54 + 79*i), False, col.BLACK, col.BLACK_BLUE, col.WHITE, col.GREEN_HOVER)
    btn_sub_mode_list.append(button)
mode_menu_open = False

#buttons_sub_menu_settings:
btn_sub_algorithm_list = []
for i in range(len(btn_list_algorithm)):
    button = btn.Button(screen, text_font, f'{btn_list_algorithm[i]}', 280, 76, (300, 54 + 79*i), False, col.BLACK, col.BLACK_BLUE, col.WHITE, col.GREEN_HOVER)
    btn_sub_algorithm_list.append(button)
setting_menu_open = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
    screen.fill((35,45,63))
    screen.blit(navbar,(0,0))
    drawBorderBoard()
    if menu_mode:
        screen.blit(logo_surf, logo_rect)

        for btn in btn_menu_list:
            mode_menu_open, setting_menu_open = btn.draw(mode_menu_open, setting_menu_open)
        if mode_menu_open:
            mode_menu_open = draw_sub_menu(btn_sub_mode_list, btn_sub_algorithm_list, mode_menu_open)
    
    pg.display.update()
    clock.tick(60)

