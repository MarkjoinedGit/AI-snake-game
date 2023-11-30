from node import *
from collections import deque
import numpy as np
from queue import PriorityQueue
from static import *
from queue import Queue
import math

class HillClimbing:
    def __init__(self, initial_X, initial_Y, food_x, food_y, obstacles):
        self.X = initial_X
        self.Y = initial_Y
        self.food_x = food_x
        self.food_y = food_y
        self.obstacles =  obstacles
        self.node = Node(self.X, self.Y, self.food_x, self.food_y)
        self.node.obstacles=obstacles
        self.matrix_state = self.node.CreateState()
        self.moved_pos=[] 
    
    def isValid(sefl, mat, visited, row, col):
        return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0])) and ((mat[row][col] == 0) or (mat[row][col] == -1)) and not visited[row][col]
    
    def hill_climbing(self):
        mat = self.matrix_state
        src = ((self.Y[0] // CELL_SIZE) - 1, (self.X[0] // CELL_SIZE) - 1)
        dest = ((self.food_y // CELL_SIZE) - 1, (self.food_x // CELL_SIZE) - 1)
        current_position = src
        current_path = []
        best_neighbor_h = len(mat[0])*len(mat)
        
        visited = [[False for x in range(len(mat[0]))] for y in range(len(mat))]
        
        while True:
            if current_position == dest:
                return current_path
            best_neighbor = None
            neighbors = []
            directions = [(0, -1, LEFT), (-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN)]
            for d in directions:
                
                newRow, newCol = current_position[0] + d[0], current_position[1] + d[1]
                
                if self.isValid(self.matrix_state, visited, newRow, newCol):
                    tempX = self.X.copy()
                    tempY = self.Y.copy()
                    newNode = Node(tempX, tempY, self.food_x, self.food_y).move(d[2])
                    self.moved_pos.append((newCol,newRow))
                    visited[newRow][newCol] = True
                    neighbor_h = abs(newRow - dest[0]) + abs(newCol - dest[1])  # Heuristic function
                    if neighbor_h < best_neighbor_h:
                        self.mat = newNode.CreateState()
                        neighbors.append((newRow, newCol, d[2]))
                        best_neighbor = d[2]
                        best_neighbor_h = neighbor_h
            if len(neighbors) == 0:
                return current_path
            best_neighbor = min(neighbors, key=lambda x: abs(dest[0] - x[0]) + abs(dest[1] - x[1]))
            current_path.append(best_neighbor[2])
            current_position = (best_neighbor[0], best_neighbor[1])
