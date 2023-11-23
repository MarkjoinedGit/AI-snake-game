import pygame
from pygame.locals import *
from static import *

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        
        self.direction = LEFT
        self.block = SNAKE_BLOCK_IMG.convert_alpha()
        self.block_rect = self.block.get_rect()
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()
        self.length = 10
        self.x = [255, 260, 265, 270, 275, 280, 285, 290, 295, 300]
        self.y = [220, 220, 220, 220, 220, 220, 220, 220, 220, 220]

    def move_left(self):
        self.direction = LEFT
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()

    def move_right(self):
        self.direction = RIGHT
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()

    def move_up(self):
        self.direction = UP
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()

    def move_down(self):
        self.direction = DOWN
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        speed = CELL_SIZE
        # update head
        if self.direction == LEFT:
            self.x[0] -= speed
            
        if self.direction == RIGHT:
            self.x[0] += speed
            
        if self.direction == UP:
            self.y[0] -= speed
        if self.direction == DOWN:
            self.y[0] += speed
        self.draw()

    def draw(self):
        for i in range(self.length-1,-1,-1):         
            if self.direction==LEFT:                
                self.head_rect.center = (self.x[i], self.y[i])        
            elif self.direction==RIGHT:           
                self.head_rect.center = (self.x[i], self.y[i])        
            elif self.direction==UP:               
                self.head_rect.center = (self.x[i], self.y[i])        
            elif self.direction==DOWN:
                self.head_rect.center = (self.x[i], self.y[i])       
                             
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