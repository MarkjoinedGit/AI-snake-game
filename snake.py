import pygame
from pygame.locals import *
from static import *

# GAME_WIDTH= WIDTH_BOARD - 2*CELL_SIZE
# GAME_HEIGHT= HEIGHT_BOARD - 2*CELL_SIZE - HEIGHT_NAVBAR

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        
        self.direction = 'down'
        self.block = SNAKE_BLOCK_IMG.convert_alpha()
        self.block_rect = self.block.get_rect()
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()
        self.length = 10
        self.x = [CELL_SIZE*20]*self.length
        self.y = [CELL_SIZE*20]*self.length

    def move_left(self):
        self.direction = 'left'
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()

    def move_right(self):
        self.direction = 'right'
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()

    def move_up(self):
        self.direction = 'up'
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()

    def move_down(self):
        self.direction = 'down'
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        speed = CELL_SIZE
        # update head
        if self.direction == 'left':
            self.x[0] -= speed
            
        if self.direction == 'right':
            self.x[0] += speed
            
        if self.direction == 'up':
            self.y[0] -= speed
        if self.direction == 'down':
            self.y[0] += speed

        self.draw()

    def draw(self):
        d=0
        for i in range(self.length-1,-1,-1):         
            if self.direction=='left':                
                self.head_rect.center = (self.x[i]-d, self.y[i])        
            elif self.direction=='right':           
                self.head_rect.center = (self.x[i]+d, self.y[i])        
            elif self.direction=='up':               
                self.head_rect.center = (self.x[i], self.y[i]-d)        
            elif self.direction=='down':
                self.head_rect.center = (self.x[i], self.y[i]+d)       
                             
            if(i==0):                  
                self.parent_screen.blit(self.head, self.head_rect)
            elif(i>0 and i<self.length-1): 
                self.block_rect.center = (self.x[i], self.y[i])  
                self.parent_screen.blit(self.block, self.block_rect)

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)