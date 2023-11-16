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
    def CreateState(self):
        self.matrix[(self.foodY//CELL_SIZE)-1][(self.foodX//CELL_SIZE)-1]=-1
        for i in range(len(self.snakeX)):
            self.matrix[(self.snakeY[i]//CELL_SIZE)-1][(self.snakeX[i]//CELL_SIZE)-1]=i+1
        self.CreateObstacle()
        return self.matrix
    def out(self):      
        print(self.CreateState())
    
    def CreateObstacle(self):
        self.matrix[:H,0] = -2
        self.matrix[-1, :W] = -2
        self.matrix[:H, -1] = -2
        for i in range(NAV_H):
            self.matrix[i,:W] = -2
            self.matrix[i,:W] = -2
