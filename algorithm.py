from node import *
from collections import deque
import numpy as np
from queue import PriorityQueue
from static import *

class Algorithm:
    def __init__(self, initial_X, initial_Y, food_x, food_y):
        self.X = initial_X
        self.Y = initial_Y
        self.food_x = food_x
        self.food_y = food_y
        self.node = Node(self.X, self.Y, self.food_x, self.food_y)
        self.matrix_state = self.node.CreateState()
            
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
        # update head
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

    def BFS(self):
        visited = set()
        tempX = self.X.copy()
        tempY = self.Y.copy()
        queue = deque([(self.matrix_state, [], tempX, tempY)])

        while queue:
            current_matrix, path, tempX, tempY = queue.popleft()
            if tempX[0] == self.food_x and tempY[0] == self.food_y:
                return path
            for move in self.get_possible_moves(current_matrix):
                new_matrix, newTempX, newTempY = self.perform_move(current_matrix, move, tempX, tempY)
                new_matrix_tuple = tuple(tuple(row) for row in new_matrix)
                if new_matrix_tuple not in visited:
                    visited.add(new_matrix_tuple)
                    new_path = path + [move]
                    queue.append((new_matrix, new_path, newTempX, newTempY))
        
    def DFS(self,depth_limit):       
        def dfs_recursive(current_state, path, tempX,tempY,depth):
            if tempX[0] == self.food_x and tempY[0] == self.food_y:
                return path

            if depth == depth_limit:
                return None
            
            for move in self.get_possible_moves(current_state):
                new_matrix, newTempX, newTempY = self.perform_move(current_matrix, move, tempX, tempY)
                new_matrix_tuple = tuple(tuple(row) for row in new_matrix)
                
                if new_matrix_tuple not in visited:
                    visited.add(new_matrix_tuple)
                    new_path = path + [move]
                    
                    result = dfs_recursive(new_matrix, new_path, newTempX, newTempY, depth + 1)
                    if result:
                        return result
                    
        tempX = self.X.copy()
        tempY = self.Y.copy()
        stack = [(self.matrix_state, [], tempX, tempY)]
        visited = set()    
        while stack:
            current_matrix, path,tempX,tempY = stack.pop()
            print(current_matrix)
            result = dfs_recursive(current_matrix, path, tempX, tempY, 0)
            
            if result:
                return result
    
# Call method
# X = [255, 260, 265, 270, 275, 280, 285, 290, 295, 300]
# Y =  [220, 220, 220, 220, 220, 220, 220, 220, 220, 220]

# food_x = 250
# food_y = 250
# #solution = Algorithm(X, Y, food_x, food_y).DFS(10)
# #solution = Algorithm(X, Y, food_x, food_y).BFS()
# print(solution)

#dfs ['left', 'left', 'down', 'right', 'down', 'down', 'down', 'down', 'down']
#bfs ['left', 'down', 'down', 'down', 'down', 'down', 'down']