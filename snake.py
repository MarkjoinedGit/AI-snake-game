import pygame
from pygame.locals import *
from static import *
from skin import *
class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        
        self.snake_skin = Skin(SkinName=SKIN_1)
        self.direction = LEFT
        self.block = self.snake_skin.block.convert_alpha()
        self.block_rect = self.block.get_rect()
        self.head = self.snake_skin.head[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()
        self.length = 10
        self.x = [910, 920, 930, 940, 950, 960, 970, 980, 990, 1000]
        self.y = [560, 560, 560, 560, 560, 560, 560, 560, 560, 560]
        
    def move_left(self):
        self.direction = LEFT
        self.head = self.snake_skin.head[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()

    def move_right(self):
        self.direction = RIGHT
        self.head = self.snake_skin.head[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()

    def move_up(self):
        self.direction = UP
        self.head = self.snake_skin.head[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()

    def move_down(self):
        self.direction = DOWN
        self.head = self.snake_skin.head[self.direction].convert_alpha()
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
        
    def changeSkin(self,skinname):
        self.snake_skin= Skin(skinname)
        self.block = self.snake_skin.block.convert_alpha()
        self.head = self.snake_skin.head[self.direction].convert_alpha()