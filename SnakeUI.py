# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 19:56:25 2023

@author: Van Hoang
"""

import pygame, sys
from pygame.locals import *
import copy
import random
import time

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

menu_surface = pygame.Surface((menu_width, menu_height))
menu_surface.fill(menu_color)


# Cài đặt vận tốc kéo menu
scroll_speed = 30


CELL_SIZE = 20
CELL_NUMBER_X = 50
CELL_NUMBER_Y = 33

ZERO_POS = 0
HEIGHT_NAVBAR = 50

WIDTH_BOARD = CELL_SIZE*CELL_NUMBER_X + CELL_SIZE*2
HEIGHT_BOARD = CELL_NUMBER_Y*CELL_SIZE + CELL_SIZE*2 + HEIGHT_NAVBAR


WIDTH_BORDER_BOARD = WIDTH_BOARD
HEIGHT_BORDER_BOARD = CELL_SIZE

LOGO_IMG = pygame.image.load('logo.png')

PLAY_BTN_IMG = pygame.image.load('playbtn.png')

SCORE_IMG = pygame.image.load('score.png')

CLOSE_BTN_IMG = pygame.image.load('close-btn.png')

pos_border = [(ZERO_POS,HEIGHT_NAVBAR),(ZERO_POS, HEIGHT_BOARD - HEIGHT_BORDER_BOARD),(ZERO_POS,HEIGHT_NAVBAR),(WIDTH_BOARD - HEIGHT_BORDER_BOARD,HEIGHT_NAVBAR)]

pygame.init()
font = pygame.font.Font(None, 30)
screen = pygame.display.set_mode((WIDTH_BOARD,HEIGHT_BOARD))
clock = pygame.time.Clock()

pygame.display.flip()
MENU_IMG = pygame.image.load('ep_menu.png').convert_alpha()
pygame.display.flip()




def addFrame():
    ModeSurface = pygame.Rect(10, 50,300, 623)
    pygame.draw.rect(menu_surface, WHITE, ModeSurface, 1)
    Mode = "Mode"
    Mode_text_surface = font.render(Mode, True, black)
    Mode_text_rect = Mode_text_surface.get_rect()
    Mode_text_rect.center = (ModeSurface.centerx, 30)
    menu_surface.blit(Mode_text_surface, Mode_text_rect)
    addMode(ModeSurface)
    
    
    AlgorithmSurface = pygame.Rect(347, 50,300, 623)
    pygame.draw.rect(menu_surface, WHITE, AlgorithmSurface, 1)
    Algorithm = "Algorithm"
    Algorithm_text_surface = font.render(Algorithm, True, black)
    Algorithm_text_rect = Algorithm_text_surface.get_rect()
    Algorithm_text_rect.center = (AlgorithmSurface.centerx, 30)
    menu_surface.blit(Algorithm_text_surface, Algorithm_text_rect)
    addAlgorithm(AlgorithmSurface)

BFS_BTN = pygame.Rect(357, 60, 280, 40)
Greedy_BTN = pygame.Rect(357, 110, 280, 40)
UCS_BTN = pygame.Rect(357, 160, 280, 40)
AStar_BTN = pygame.Rect(357, 210, 280, 40)

def addAlgorithm(AlgorithmSurface):#chuwa xong
    
    pygame.draw.rect(menu_surface, black, BFS_BTN, 1)
    BFS = "BFS"
    BFS_text_surface = font.render(BFS, True, black)
    BFS_text_rect = BFS_text_surface.get_rect()
    BFS_text_rect.center = (AlgorithmSurface.centerx, 80)
    menu_surface.blit(BFS_text_surface, BFS_text_rect)
    
    
    pygame.draw.rect(menu_surface, black, Greedy_BTN, 1)
    Greedy = "Greedy"
    Greedy_text_surface = font.render(Greedy, True, black)
    Greedy_text_rect = Greedy_text_surface.get_rect()
    Greedy_text_rect.center = (AlgorithmSurface.centerx, 130)
    menu_surface.blit(Greedy_text_surface, Greedy_text_rect)
    
    
    pygame.draw.rect(menu_surface, black, UCS_BTN, 1)
    UCS = "UCS"
    UCS_text_surface = font.render(UCS, True, black)
    UCS_text_rect = UCS_text_surface.get_rect()
    UCS_text_rect.center = (AlgorithmSurface.centerx, 180)
    menu_surface.blit(UCS_text_surface, UCS_text_rect)
    
    
    pygame.draw.rect(menu_surface, black, AStar_BTN, 1)
    AStar = "A*"
    AStar_text_surface = font.render(AStar, True, black)
    AStar_text_rect = AStar_text_surface.get_rect()
    AStar_text_rect.center = (AlgorithmSurface.centerx, 230)
    menu_surface.blit(AStar_text_surface, AStar_text_rect)

Basic_BTN = pygame.Rect(20, 60, 280, 40)
Auto_Play_BTN = pygame.Rect(20, 110, 280, 40)
Solo_Machine_BTN = pygame.Rect(20, 160, 280, 40)
MAM_BTN = pygame.Rect(20, 210, 280, 40)
Slither_BTN = pygame.Rect(20, 260, 280, 40)

def addMode(ModeSurface):
    
    pygame.draw.rect(menu_surface, black, Basic_BTN, 1)
    Basic = "Basic"
    Basic_text_surface = font.render(Basic, True, black)
    Basic_text_rect = Basic_text_surface.get_rect()
    Basic_text_rect.center = (ModeSurface.centerx, 80)
    menu_surface.blit(Basic_text_surface, Basic_text_rect)
    
    
    pygame.draw.rect(menu_surface, black, Auto_Play_BTN, 1)
    Auto = "Auto"
    Auto_text_surface = font.render(Auto, True, black)
    Auto_text_rect = Auto_text_surface.get_rect()
    Auto_text_rect.center = (ModeSurface.centerx, 130)
    menu_surface.blit(Auto_text_surface, Auto_text_rect)
    
    
    pygame.draw.rect(menu_surface, black, Solo_Machine_BTN, 1)
    SoloMachine = "Solo Machine"
    SoloMachine_text_surface = font.render(SoloMachine, True, black)
    SoloMachine_text_rect = SoloMachine_text_surface.get_rect()
    SoloMachine_text_rect.center = (ModeSurface.centerx, 180)
    menu_surface.blit(SoloMachine_text_surface, SoloMachine_text_rect)
    
    
    pygame.draw.rect(menu_surface, black, MAM_BTN, 1)
    MAM = "Machine And Machine"
    MAM_text_surface = font.render(MAM, True, black)
    MAM_text_rect = MAM_text_surface.get_rect()
    MAM_text_rect.center = (ModeSurface.centerx, 230)
    menu_surface.blit(MAM_text_surface, MAM_text_rect)
    
    
    pygame.draw.rect(menu_surface, black, Slither_BTN, 1)
    Slither = "Slither"
    Slither_text_surface = font.render(Slither, True, black)
    Slither_text_rect = Slither_text_surface.get_rect()
    Slither_text_rect.center = (ModeSurface.centerx, 280)
    menu_surface.blit(Slither_text_surface, Slither_text_rect)

MENU_BTN = pygame.Rect(320, 5, 100, 40)
NEW_BOARD_BTN = pygame.Rect(673, 5, 100, 40)

def drawNavBar():
    screen.blit(navbar,(0,0))
    
    pygame.draw.rect(screen, WHITE, MENU_BTN, 1)
    pygame.draw.rect(screen, WHITE, NEW_BOARD_BTN, 1)

    MENU_BTN_text = "MENU"
    MENU_BTN_text_surface = font.render(MENU_BTN_text, True, WHITE)
    MENU_BTN_text_rect = MENU_BTN_text_surface.get_rect()
    MENU_BTN_text_rect.center = (MENU_BTN.centerx, MENU_BTN.centery)
    navbar.blit(MENU_BTN_text_surface, MENU_BTN_text_rect)
    addFrame()
    
    # Tên của nút "NEW"
    NEW_BOARD_BTN_text = "NEW"
    NEW_BOARD_BTN_text_surface = font.render(NEW_BOARD_BTN_text, True, WHITE)
    NEW_BOARD_BTN_text_rect = NEW_BOARD_BTN_text_surface.get_rect()
    NEW_BOARD_BTN_text_rect.center = (NEW_BOARD_BTN.centerx, NEW_BOARD_BTN.centery)
    screen.blit(NEW_BOARD_BTN_text_surface, NEW_BOARD_BTN_text_rect)

def drawBorderBoard():
    screen.blit(border_horizontal_top,pos_border[0])
    screen.blit(border_horizontal_bottom,pos_border[1])
    screen.blit(border_vertical_left,pos_border[2])
    screen.blit(border_vertical_right,pos_border[3])

def showMenu():
    global menu_x
    menu_x += scroll_speed
    if menu_x > 0:
        menu_x = 0
    pygame.draw.rect(menu_surface, border_color, (0, 0, menu_width, menu_height), border_width)
    screen.blit(menu_surface, (menu_x, menu_y))

def closeMenu():
    global menu_x
    menu_x -= scroll_speed
    if menu_x + menu_width > 0:
        menu_x = -menu_width
    pygame.draw.rect(menu_surface, border_color, (0, 0, menu_width, menu_height), border_width)
    screen.blit(menu_surface, (menu_x, menu_y))

def is_collision_with_menu(mouse_x, mouse_y):
    return menu_x <= mouse_x < menu_surface.get_width() and menu_y <= mouse_y < menu_surface.get_height()

navbar = pygame.Surface((WIDTH_BOARD,HEIGHT_NAVBAR))
navbar.fill(NAVBAR_COLOR)
navbar.blit(LOGO_IMG, (30,15))
navbar.blit(SCORE_IMG, (434,10))
navbar.blit(PLAY_BTN_IMG, (612,10))
navbar.blit(CLOSE_BTN_IMG, (1061,15))




border_horizontal_top = pygame.Surface((WIDTH_BORDER_BOARD, HEIGHT_BORDER_BOARD))
border_horizontal_top.fill(BORDER_COLOR)

border_horizontal_bottom = border_horizontal_top

border_vertical_left = pygame.transform.rotate (border_horizontal_top, 90)
border_vertical_right = border_vertical_left


SHOW_MENU = 1
CLOSE_MENU = 0
current_click = -1

while True:
    screen.fill((35,45,63))
    drawNavBar()
    drawBorderBoard()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # print(Basic_BTN.x,Basic_BTN.y)
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if MENU_BTN.collidepoint(mouse_x, mouse_y):
                # print(current_click)
                if current_click == CLOSE_MENU or current_click == -1:
                    current_click = SHOW_MENU
                elif current_click == SHOW_MENU:
                    current_click = CLOSE_MENU
            if is_collision_with_menu(mouse_x, mouse_y):
                relative_x = mouse_x
                relative_y = mouse_y-100 # lay toa do con tro chuot doi voi menu
                print(relative_x, relative_y)
                if Basic_BTN.collidepoint(relative_x, relative_y):
                    print("Basic_BTN")
            #     Basic_Mode()
            # elif Auto_Play_BTN.collidepoint(mouse_x, mouse_y):
            #     Auto_Play_Mode()
            # elif Solo_Machine_BTN.collidepoint(mouse_x, mouse_y):
            #     Solo_Machine_Mode()
            # elif MAM_BTN.collidepoint(mouse_x, mouse_y):
            #     MAM_Mode()
            # elif Slither_BTN.collidepoint(mouse_x, mouse_y):
            #     Slither_Mode()
            # elif BFS_BTN.collidepoint(mouse_x, mouse_y):
            #     BFS()
            # elif Greedy_BTN.collidepoint(mouse_x, mouse_y):
            #     Greedy()
            # elif UCS_BTN.collidepoint(mouse_x, mouse_y):
            #     UCS()
            # elif AStar_BTN.collidepoint(mouse_x, mouse_y):
            #     AStar()
            
            
    if current_click==SHOW_MENU:
        showMenu()
    elif current_click==CLOSE_MENU:
        closeMenu()
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)