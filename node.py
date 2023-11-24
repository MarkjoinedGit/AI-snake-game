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
            self.matrix[i,:W] = OBSTACLE
    def move(self, move):
        head_x, head_y = self.snakeX[0], self.snakeY[0]

        self.snakeX = np.roll(self.snakeX, 1)
        self.snakeY = np.roll(self.snakeY, 1)
    
        speed = CELL_SIZE
        if move == LEFT :
            self.snakeY[0] = head_y
            self.snakeX[0] = head_x - speed
        if move == RIGHT:
            self.snakeY[0] = head_y 
            self.snakeX[0] = head_x + speed 
        if move == UP:
            self.snakeX[0] = head_x
            self.snakeY[0] = head_y - speed
        if move == DOWN:
            self.snakeX[0] = head_x 
            self.snakeY[0] = head_y + speed
        new_node = Node(self.snakeX, self.snakeY, self.foodX, self.foodY)
        return new_node
    
    def dist(self):
        return abs(self.foodX - self.snakeX[0]) + abs(self.foodY - self.snakeY[0])