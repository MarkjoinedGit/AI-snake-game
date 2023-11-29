from node import *
from collections import deque
import numpy as np
from queue import PriorityQueue
from static import *
from queue import Queue
import math

class ASTAR:
    def __init__(self, initial_X, initial_Y, food_x, food_y):
        self.X = initial_X
        self.Y = initial_Y
        self.food_x = food_x
        self.food_y = food_y
        self.node = Node(self.X, self.Y, self.food_x, self.food_y)
        self.matrix_state = self.node.CreateState()
        self.moved_pos=[]  
    def get_possible_moves(self, matrix):
        moves = []
        head_pos = np.where(matrix==1)
        head_pos_x = head_pos[1][0]
        head_pos_y = head_pos[0][0]

        if head_pos_x > 0:
            if matrix[head_pos_y][head_pos_x-1] == 0 or matrix[head_pos_y][head_pos_x-1] == -1:
                moves.append(LEFT)
        if head_pos_x < WIDTH_BOARD//CELL_SIZE-1:
            if matrix[head_pos_y][head_pos_x+1] == 0 or matrix[head_pos_y][head_pos_x+1] == -1:
                moves.append(RIGHT)
        if head_pos_y > 0:
            if matrix[head_pos_y-1][head_pos_x] == 0 or matrix[head_pos_y-1][head_pos_x] == -1:
                moves.append(UP)
        if head_pos_y < HEIGHT_BOARD//CELL_SIZE-1: 
            if matrix[head_pos_y+1][head_pos_x] == 0 or matrix[head_pos_y+1][head_pos_x] == -1:
                moves.append(DOWN)

        return moves

    def perform_move(self, matrix, move, tempX, tempY):
        val_x = tempX[0]
        val_y = tempY[0]
        tempX = np.roll(tempX, 1)
        tempY = np.roll(tempY, 1)
        speed = CELL_SIZE

        if move == LEFT:
            tempX[0] = val_x - speed
            tempY[0] = val_y
        if move == RIGHT:
            tempX[0] = val_x + speed
            tempY[0] = val_y
        if move == UP:
            tempY[0] = val_y - speed 
            tempX[0] = val_x
        if move == DOWN:
            tempY[0] = val_y + speed 
            tempX[0] = val_x  
        new_matrix = Node(tempX, tempY, self.food_x, self.food_x).CreateState()
        return new_matrix, tempX, tempY
    
    def isValid(sefl, mat, visited, row, col):
        return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0])) and ((mat[row][col] == 0) or (mat[row][col] == -1)) and not visited[row][col]
    
    def heuristic(self, row, col, dest_y, dest_x):
        return abs(row-dest_y) + abs(col-dest_x)
        #return math.sqrt((row - dest_y)**2 + (col - dest_x)**2)
    
    def check_stuck_posible(self, mat, visited, row, col):
        directions = [(0, -1, LEFT), (-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN)]
        for d in directions:
            newRow, newCol = row+d[0], col+d[1]
            if self.isValid(mat, visited, newRow, newCol):
                return True
        return False
    
    def a_star(self):
        mat = self.matrix_state
        src = ((self.Y[0]//CELL_SIZE)-1, (self.X[0]//CELL_SIZE)-1)
        dest = ((self.food_y//CELL_SIZE)-1, (self.food_x//CELL_SIZE)-1)
        tempX = self.X.copy()
        tempY = self.Y.copy()

        visited = [[False for x in range(len(mat[0]))] for y in range(len(mat))]
        self.visited_cost = set()

        q = PriorityQueue()

        visited[src[0]][src[1]] = True
        q.put((0, 0, src, [], tempX, tempY, mat))

        while not q.empty():
            node = q.get()
            (F, cost, pt, path, tempX, tempY, mat) = (node[0], node[1], node[2], node[3], node[4], node[5], node[6])
            self.visited_cost.add((pt))

            (row, col) = (pt[0], pt[1])

            directions = [(0, -1, LEFT), (-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN)]
            for d in directions:
                newRow, newCol = row + d[0], col + d[1]
                newPath = path + [d[2]]
                if self.isValid(mat, visited, newRow, newCol):
                    self.moved_pos.append((newCol, newRow))
                    visited[newRow][newCol] = True
                    if ((newRow, newCol)) == dest:
                        if self.check_stuck_posible(mat, visited, newRow, newCol) == False:
                            continue
                        return newPath
                    newNode = Node(tempX, tempY, self.food_x, self.food_y).move(d[2])
                    newMat, newTempX, newTempY = newNode.CreateState(), newNode.snakeX, newNode.snakeY
                    newCost = cost + 1
                    newH = self.heuristic(newRow, newCol, dest[0], dest[1]) 
                    f = newCost + newH
                    q.put((f, newCost, (newRow, newCol), newPath, newTempX, newTempY, newMat))

        return Queue()
    
    def is_collision(self, x1, y1, x2, y2,d=0):
        if x1 >= x2-d and x1 < x2 + 1+d:
            if y1 >= y2-d and y1 <y2 + 1+d:
                return True
        return False
