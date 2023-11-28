import pygame
from pygame.locals import *
from static import *
from skin import *
class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        
        self.snake_skin = Skin(SkinName=SKIN_5)
        self.direction = UP
        self.block = self.snake_skin.block.convert_alpha()
        self.block_rect = self.block.get_rect()
        self.head = self.snake_skin.head[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect()
        self.length = 192
        self.x = [460, 460, 460, 460, 460, 460, 460, 460, 460, 460, 455, 450, 445, 440, 435, 430, 425, 420, 415, 410, 405, 400, 395, 390, 385, 380, 375, 370, 365, 360, 355, 350, 345, 340, 335, 330, 325, 320, 315, 310, 305, 300, 295, 290, 285, 280, 275, 270, 265, 260, 255, 250, 245, 240, 235, 230, 225, 220, 215, 210, 205, 200, 195, 190, 185, 180, 175, 170, 165, 160, 155, 150, 145, 140, 135, 130, 125, 120, 115, 110, 105, 100, 95, 90, 85, 85, 85, 85, 85, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 45, 50, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 55, 50, 45, 45, 45, 45, 45, 50, 55, 60, 60, 60, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140]
        self.y = [155, 150, 145, 140, 135, 130, 125, 120, 115, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 115, 120, 125, 130, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 190, 190, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300, 305, 310, 310, 305, 300, 295, 290, 285, 280, 275, 270, 265, 260, 255, 250, 245, 240, 235, 230, 225, 220, 215, 210, 205, 200, 195, 190, 185, 185, 185, 185, 180, 175, 170, 165, 165, 165, 165, 160, 155, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150]
        
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