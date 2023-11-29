from node import *
from collections import deque
import numpy as np
from queue import PriorityQueue
from static import *
from queue import Queue

class BFS:
    def __init__(self, initial_X, initial_Y, food_x, food_y):
        self.X = initial_X
        self.Y = initial_Y
        self.food_x = food_x
        self.food_y = food_y
        self.node = Node(self.X, self.Y, self.food_x, self.food_y)
        self.matrix_state = self.node.CreateState()
        
    def isValid(sefl, mat, visited, row, col):
        return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0])) and ((mat[row][col] == 0) or (mat[row][col] == -1)) and not visited[row][col]
    
    def check_stuck_posible(self, mat, visited, row, col):
        directions = [(0, -1, LEFT), (-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN)]
        for d in directions:
            newRow, newCol = row+d[0], col+d[1]
            if self.isValid(mat, visited, newRow, newCol):
                return True
        return False
    
    def bfs(self):
        mat = self.matrix_state
        src = ((self.Y[0]//CELL_SIZE)-1, (self.X[0]//CELL_SIZE)-1)
        dest = ((self.food_y//CELL_SIZE)-1, (self.food_x//CELL_SIZE)-1)
        tempX = self.X.copy()
        tempY = self.Y.copy()

        visited = [[False for x in range(len(mat[0]))] for y in range(len(mat))]

        q = Queue()

        visited[src[0]][src[1]] = True
        q.put((src, [], tempX, tempY, mat))

        while not q.empty():
            node = q.get()
            (pt, path, tempX, tempY, mat) = (node[0], node[1], node[2], node[3], node[4])
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
                        return newPath
                    newNode = Node(tempX, tempY, self.food_x, self.food_y).move(d[2])
                    newMat, newTempX, newTempY = newNode.CreateState(), newNode.snakeX, newNode.snakeY                
                    q.put(((newRow, newCol), newPath, newTempX, newTempY, newMat))

        return Queue()
    
    def is_collision(self, x1, y1, x2, y2,d=0):
        if x1 >= x2-d and x1 < x2 + 1+d:
            if y1 >= y2-d and y1 <y2 + 1+d:
                return True
        return False
