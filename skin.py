import pygame
from static import *

class Skin:
    def __init__(self,SkinName):
        self.head= {
            'left': pygame.transform.scale(pygame.image.load('assets/snake/head-'+SkinName+'-left.png'), SIZE_SNAKE_IMG),
            'right':pygame.transform.scale(pygame.image.load('assets/snake/head-'+SkinName+'-right.png'), SIZE_SNAKE_IMG),
            'up':pygame.transform.scale(pygame.image.load('assets/snake/head-'+SkinName+'-up.png'), SIZE_SNAKE_IMG),
            'down':pygame.transform.scale(pygame.image.load('assets/snake/head-'+SkinName+'-down.png'), SIZE_SNAKE_IMG),
        }
        self.block= pygame.transform.scale(pygame.image.load('assets/snake/body-'+SkinName+'.png'), SIZE_SNAKE_IMG)