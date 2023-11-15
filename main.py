from typing import Any
import pygame as pg
from pygame.sprite import Group
import color as col
import buttons as btn
import snakegame

def draw_sub_menu(menu_list, menu_open):
    screen.blit(sub_menu_surf, sub_menu_rect)
    for btn in menu_list:
        btn.draw()
    # if menu_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0] and sub_menu_rect.collidepoint(pg.mouse.get_pos()) == False:
    #     menu_open = False
    # else:
    #     menu_open = True
    # return menu_open    


pg.init()
screen = pg.display.set_mode((1050, 750))
pg.display.set_caption('Snather')
clock = pg.time.Clock()

#menu
menu_surf = pg.image.load(r'assets\menu\menu-bg.png').convert()
menu_rect = menu_surf.get_rect(topleft = (0, 47.73))
sub_menu_surf = pg.image.load(r'assets\menu\sub-menu-bg.png').convert_alpha()
sub_menu_rect = sub_menu_surf.get_rect(topleft=(0, 48))
menu_mode = True

#nav_bar
nav_bar_surf = pg.image.load(r'assets\nav-bar\navbar.png').convert()
nav_bar_rect = nav_bar_surf.get_rect(topleft=(0, 0))
#logo
logo_surf = pg.image.load(r'assets\nav-bar\logo.png').convert_alpha()
logo_rect = logo_surf.get_rect(center=(60, 23.865))
#button
btn_image = r'assets\btn.png'
btn_surf = pg.image.load(btn_image).convert_alpha()
btn_rect = btn_surf.get_rect(center=(525, 375))
btn_list_func = ['Start', 'Mode', 'Settings', 'Exit']
btn_list_mode = ['Basic', 'Auto play', 'Solo machine', 'Machine vs Machine', 'Slither.io']
btn_list_setting = ['Algorithm', 'Sound', 'Snake skin', 'Reset Settings']
#text_font 
text_font = pg.font.Font(r'assets\font\Inknut_Antiqua\InknutAntiqua-Bold.ttf', 18)

#buttons
btn_menu_list = []
for i in range(len(btn_list_func)):
    button = btn.Button(screen, text_font, f'{btn_list_func[i]}', 162, 51, (739, 434 +i*56), True, col.WHITE, col.GREEN_HOVER, col.WHITE, col.GREEN_HOVER)
    btn_menu_list.append(button)
#buttons_sub_menu_mode
btn_sub_mode_list = []
for i in range(len(btn_list_mode)):
    button = btn.Button(screen, text_font, f'{btn_list_mode[i]}', 280, 76, (0, 54 + 79*i), False, col.BLACK, col.BLACK_BLUE, col.WHITE, col.GREEN_HOVER)
    btn_sub_mode_list.append(button)
mode_menu_open = False
#buttons_sub_menu_settings:
btn_sub_setting_list = []
for i in range(len(btn_list_setting)):
    button = btn.Button(screen, text_font, f'{btn_list_setting[i]}', 280, 76, (0, 54 + 79*i), False, col.BLACK, col.BLACK_BLUE, col.WHITE, col.GREEN_HOVER)
    btn_sub_setting_list.append(button)
setting_menu_open = False

start_game = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            for btn in btn_menu_list:
                if btn.check_click():
                    mode_menu_open = False
                    setting_menu_open = False
                    start_game = False
                    if btn.text == 'Mode':
                        mode_menu_open = True
                    elif btn.text == 'Settings':
                        setting_menu_open = True
                    elif btn.text == 'Start':
                        start_game = True
    screen.fill('black')
    if start_game == False:
        screen.blit(nav_bar_surf, nav_bar_rect)
        if menu_mode:
            screen.blit(logo_surf, logo_rect)
            screen.blit(menu_surf, (0, 47.73))

            for btn in btn_menu_list:
                btn.draw()

            if mode_menu_open:
                draw_sub_menu(btn_sub_mode_list, mode_menu_open)         
            elif setting_menu_open:
                draw_sub_menu(btn_sub_setting_list, setting_menu_open)

    else:
        snakegame.Game().run()
        start_game = False
        mode_menu_open = False

    pg.display.update()
    clock.tick(60)

            

