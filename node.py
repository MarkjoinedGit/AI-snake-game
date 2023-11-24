import numpy as np
from static import *
W = WIDTH_BOARD//CELL_SIZE
H = HEIGHT_BOARD//CELL_SIZE
NAV_H = 50//CELL_SIZE

class Node:
    def __init__(self,snakeX,snakeY,foodX,foodY):
        self.matrix= np.zeros((H,W),dtype=int)
        self.snakeX = snakeX
        self.snakeY = snakeY
        self.foodX = foodX
        self.foodY = foodY
        self.direction = None 
        self.h = 0
        self.g = 0
        self.f = 1000000
        self.parent = None
    
    def getPos_Matrix(self,pos):
        return (pos//CELL_SIZE)-1
    
    def CreateState(self):
        self.matrix[self.getPos_Matrix(self.foodY)][self.getPos_Matrix(self.foodX)]=FOOD
        for i in range(len(self.snakeX)):
            self.matrix[self.getPos_Matrix(self.snakeY[i])][self.getPos_Matrix(self.snakeX[i])]=i+1
        self.CreateObstacle()
        return self.matrix
    def out(self):      
        print(self.CreateState())
    
    def CreateObstacle(self):
        self.matrix[:H,0] = OBSTACLE
        self.matrix[-1, :W] = OBSTACLE
        self.matrix[:H, -1] = OBSTACLE
        for i in range(NAV_H):
            self.matrix[i,:W] = OBSTACLE
    def move(self, move):
        head_x, head_y = self.snakeX[0], self.snakeY[0]

        snakeX=  self.snakeX.copy()
        snakeY= self.snakeY.copy()
        snakeX = np.roll(snakeX, 1)
        snakeY = np.roll(snakeY, 1)
    
        speed = CELL_SIZE
        if move == LEFT :
            snakeY[0] = head_y
            snakeX[0] = head_x - speed
        if move == RIGHT:
            snakeY[0] = head_y 
            snakeX[0] = head_x + speed 
        if move == UP:
            snakeX[0] = head_x
            snakeY[0] = head_y - speed
        if move == DOWN:
            snakeX[0] = head_x 
            snakeY[0] = head_y + speed
        new_node = Node(snakeX, snakeY, self.foodX, self.foodY)
        new_node.direction=move
        return new_node
    
    def dist(self):
        return abs(self.foodX - self.snakeX[0]) + abs(self.foodY - self.snakeY[0])