import numpy as np
from static import *
import copy
import time
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
        self.time= time.time()
    
    def getPos_Matrix(self,pos):
        return (pos//CELL_SIZE)-1
    
    def CreateState(self):
        matrix= np.zeros((H,W),dtype=int)
        matrix[posGame_to_posMatrix(self.foodY)][posGame_to_posMatrix(self.foodX)]=FOOD
        for i in range(len(self.snakeX)):
            matrix[posGame_to_posMatrix(self.snakeY[i])][posGame_to_posMatrix(self.snakeX[i])]=i+1
        matrix=self.CreateObstacle(matrix)
        self.matrix= matrix
        return matrix
    def out(self):      
        print(self.CreateState())
    
    def CreateObstacle(self,matrix):
        matrix[:H,0] = OBSTACLE
        matrix[-1, :W] = OBSTACLE
        matrix[:H, -1] = OBSTACLE
        for i in range(NAV_H):
            matrix[i,:W] = OBSTACLE
        return matrix
    def move(self, move):
        new_node = self.copy_myself()
        head_x, head_y = new_node.snakeX[0], new_node.snakeY[0]
        new_node.snakeX = np.roll(new_node.snakeX, 1)
        new_node.snakeY = np.roll(new_node.snakeY, 1)
    
        speed = CELL_SIZE
        if move == LEFT :
            new_node.snakeY[0] = head_y
            new_node.snakeX[0] = head_x - speed
        if move == RIGHT:
            new_node.snakeY[0] = head_y 
            new_node.snakeX[0] = head_x + speed 
        if move == UP:
            new_node.snakeX[0] = head_x
            new_node.snakeY[0] = head_y - speed
        if move == DOWN:
            new_node.snakeX[0] = head_x 
            new_node.snakeY[0] = head_y + speed
        new_node.direction=move
        new_node.h=self.h 
        new_node.g=self.g
        new_node.parent=self.parent
        new_node.time= time.time()
        return new_node
    
    def dist(self):
        self.h = abs(self.foodX - self.snakeX[0]) + abs(self.foodY - self.snakeY[0])
        return self.h 
    
    def is_collision(self):
        if self.snakeX[0] == self.foodX and self.snakeY[0] == self.foodY:
            return True
        return False
    
    def copy_myself(self):
        return copy.deepcopy(self)
    def get_path(self):
        path=[]
        node=self.copy_myself()
        if node.parent == None:
            return node.direction
        while node.parent.parent != None:
            path.append(node.direction)
            node = node.parent
        path.append(node.direction)
        return  path[::-1]
    
    def print(self,name='Node-State'):
        print(f'-----------------------------{name}--------------------------------')
        print('snakeX= ',posGame_to_posMatrix_list( self.snakeX))
        print('snakeY= ',posGame_to_posMatrix_list(self.snakeY))
        print('Food(x,y)= ',(posGame_to_posMatrix(self.foodX),posGame_to_posMatrix(self.foodY)))
        print('h= ',self.h)
        print('g= ',self.g)
        print('f= ',self.f)
        path= self.get_path()
        if path==None:
            path=[]
        print(f'path({len(path)})= ',path)
        print('time_create= ',self.time)
        
    def __lt__(self, other):
        return self.f < other.f
