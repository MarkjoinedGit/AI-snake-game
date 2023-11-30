from node import *
from collections import deque
import numpy as np
from queue import PriorityQueue
from static import *
from queue import Queue

class DFS:
    def __init__(self, initial_X, initial_Y, food_x, food_y,obstacles):
        self.X = initial_X
        self.Y = initial_Y
        self.food_x = food_x
        self.food_y = food_y
        self.obstacles =  obstacles
        self.node = Node(self.X, self.Y, self.food_x, self.food_y)
        self.node.obstacles=obstacles
        self.matrix_state = self.node.CreateState()
        self.moved_pos=[]
        self.run_time=0   
    
    def isValid(sefl, mat, visited, row, col):
        return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0])) and ((mat[row][col] == 0) or (mat[row][col] == -1)) and not visited[row][col]
    
    def check_stuck_posible(self, mat, visited, row, col):
        directions = [(0, -1, LEFT), (-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN)]
        for d in directions:
            newRow, newCol = row+d[0], col+d[1]
            if self.isValid(mat, visited, newRow, newCol):
                return True
        return False
    
    def dfs(self):
        start_time=time.time()
        mat = self.matrix_state
        src = ((self.Y[0]//CELL_SIZE)-1, (self.X[0]//CELL_SIZE)-1)
        dest = ((self.food_y//CELL_SIZE)-1, (self.food_x//CELL_SIZE)-1)
        tempX = self.X.copy()
        tempY = self.Y.copy()
        current_path = []

        visited = [[False for x in range(len(mat[0]))] for y in range(len(mat))] 

        stack = []
        visited[src[0]][src[1]] = True
        stack.append((src, [], tempX, tempY, mat))
        while stack:
            node = stack.pop()
            (pt, path, tempX, tempY, mat) = (node[0], node[1], node[2], node[3], node[4])
            current_path=path
            (row, col) = (pt[0], pt[1])
            directions = [(0, -1, LEFT), (-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN)]
            for d in directions:
                newRow, newCol = row + d[0], col + d[1]
                newPath = path + [d[2]]
                if self.isValid(mat, visited, newRow, newCol): 
                    self.moved_pos.append((newCol,newRow))
                    visited[newRow][newCol] = True
                    if ((newRow, newCol)) == dest:
                        if self.check_stuck_posible(mat, visited, newRow, newCol) == False:
                            continue
                        self.run_time=(time.time()-start_time)*1000//1
                        return newPath
                    newNode = Node(tempX, tempY, self.food_x, self.food_y).move(d[2])
                    newNode.obstacles = self.obstacles
                    newMat, newTempX, newTempY = newNode.CreateState(), newNode.snakeX, newNode.snakeY  
                    stack.append(((newRow, newCol), newPath, newTempX, newTempY, newMat))
        return current_path
    
# X = [255, 260, 265, 270, 275, 280, 285, 290, 295, 300]
# Y= [220, 220, 220, 220, 220, 220, 220, 220, 220, 220]
# food_x = 50
# food_y = 150
# ids = DFS(X, Y, food_x, food_y, set())
# print(ids.dfs())