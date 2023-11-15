from typing import Any
import pygame as pg
from pygame.sprite import Group
import my_color as col
import buttons as btn
from static import *




class DisplayGame():
    def __init__(self, screen):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH_BOARD, HEIGHT_BOARD))
        pg.display.set_caption('Snather')
        self.clock = pg.time.Clock()
        pg.display.flip()
        
        #menu
        self.menu_surf = pg.image.load(r'assets\menu\menu-bg.png').convert()
        self.menu_rect = self.menu_surf.get_rect(topleft = (0, 47.73))
        self.sub_menu_surf = pg.image.load(r'assets\menu\sub-menu-bg.png').convert_alpha()
        self.sub_mode_rect = self.sub_menu_surf.get_rect(topleft=(0, 48))
        self.sub_algorithm_rect = self.sub_menu_surf.get_rect(topleft=(300, 48))
        self.menu_mode = True

        #borders
        self.border_horizontal_top = pg.Surface((WIDTH_BORDER_BOARD, HEIGHT_BORDER_BOARD))
        self.border_horizontal_top.fill(BORDER_COLOR)
        self.border_horizontal_bottom = self.border_horizontal_top
        self.border_vertical_left = pg.transform.rotate ( self.border_horizontal_top, 90)
        self.border_vertical_right =  self.border_vertical_left

        #nav_bar
        self.navbar = pg.Surface((WIDTH_BOARD,HEIGHT_NAVBAR))
        self.navbar.fill(NAVBAR_COLOR)

        #logo
        self.logo_surf = pg.image.load(r'assets\nav-bar\logo.png').convert_alpha()
        self.logo_rect = self.logo_surf.get_rect(center=(60, 23.865))
        #button
        self.btn_image = r'assets\btn.png'
        self.btn_surf = pg.image.load(self.btn_image).convert_alpha()
        self.btn_rect = self.btn_surf.get_rect(center=(525, 375))
        self.btn_list_func = ['MENU', '0', 'PLAY', 'NEW']
        self.btn_list_mode = ['Basic', 'Auto play', 'Solo machine', 'Machine vs Machine', 'Slither.io']
        self.btn_list_algorithm = ['BFS', 'Greedy', 'UCS', 'A*']
        #text_font 
        self.text_font = pg.font.Font(r'assets\font\Inknut_Antiqua\InknutAntiqua-Bold.ttf', 18)

        #buttons
        self.btn_menu_list = []
        for i in range(len(self.btn_list_func)):
            button = btn.Button(self.screen, self.text_font, f'{self.btn_list_func[i]}', 100, 40, (200 +i*200, 5), True, col.WHITE, col.GREEN_HOVER, col.WHITE, col.GREEN_HOVER)
            self.btn_menu_list.append(button)

        #buttons_sub_menu_mode
        self.btn_sub_mode_list = []
        for i in range(len(self.btn_list_mode)):
            button = btn.Button(screen, self.text_font, f'{self.btn_list_mode[i]}', 280, 76, (0, 54 + 79*i), False, col.BLACK, col.BLACK_BLUE, col.WHITE, col.GREEN_HOVER)
            self.btn_sub_mode_list.append(button)
        self.mode_menu_open = False

        #buttons_sub_menu_settings:
        self.btn_sub_algorithm_list = []
        for i in range(len(self.btn_list_algorithm)):
            button = btn.Button(screen,self.text_font, f'{self.btn_list_algorithm[i]}', 280, 76, (300, 54 + 79*i), False, col.BLACK, col.BLACK_BLUE, col.WHITE, col.GREEN_HOVER)
            self.btn_sub_algorithm_list.append(button)
        self.setting_menu_open = False

    def drawMainDisplay(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    for btn in self.btn_menu_list:
                        if btn.check_click():
                            if btn.text == 'MENU':
                                print('get into menu')
                                self.mode_menu_open = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.logo_rect.collidepoint(pg.mouse.get_pos()):
                        print('collide with logo')
                        return
            self.screen.fill((35,45,63))
            self.screen.blit(self.navbar,(0,0))
            self.drawBorderBoard()
            if self.menu_mode:
                self.screen.blit(self.logo_surf, self.logo_rect)

                for btn in self.btn_menu_list:
                    btn.draw()
                if self.mode_menu_open:
                    self.mode_menu_open = self.draw_sub_menu(self.btn_sub_mode_list, self.btn_sub_algorithm_list, self.mode_menu_open)
            pg.display.update()
            self.clock.tick(60)

    
    def drawBorderBoard(self):
        self.screen.blit(self.border_horizontal_top,pos_border[0])
        self.screen.blit(self.border_horizontal_bottom,pos_border[1])
        self.screen.blit(self.border_vertical_left,pos_border[2])
        self.screen.blit(self.border_vertical_right,pos_border[3])


    def draw_sub_menu(self, menu_list, btn_sub_algorithm_list, menu_open):
        self.screen.blit(self.sub_menu_surf, self.sub_mode_rect)
        self.screen.blit(self.sub_menu_surf, self.sub_algorithm_rect)
        for btn in menu_list:
            btn.draw()
            
        for btn in btn_sub_algorithm_list:
            btn.draw()
            
        if self.menu_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
            menu_open = False
        else:
            menu_open = True
        return menu_open
        