import pygame
import numpy as np
from pygame.locals import *
import time
import random
import math
from snake import Snake
from food import Food
from static import *

class Node:
    def __init__(self,snakeX,snakeY,foodX,foodY):
        self.matrix= np.zeros((HEIGHT_BOARD//CELL_SIZE,WIDTH_BOARD//CELL_SIZE))
        self.snakeX = snakeX
        self.snakeY = snakeY
        self.foodX = foodX
        self.foodY = foodY
    def CreateState(self):
        self.matrix[(self.foodX//CELL_SIZE)-1][(self.foodY//CELL_SIZE)-1]=-1
        for i in range(len(self.snakeX)):
            self.matrix[(self.snakeX[i]//CELL_SIZE)-1][(self.snakeY[i]//CELL_SIZE)-1]=i+1
        return self.matrix
    def out(self):      
        print(self.CreateState())