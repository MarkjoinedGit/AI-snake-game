from node import *
from collections import deque
import numpy as np
from static import *

class BFS_PATH:
    def __init__(self, initial_X, initial_Y, food_x, food_y):
        self.X = initial_X
        self.Y = initial_Y
        self.node = Node(self.X, self.Y, food_x, food_y)
        self.matrix_state = self.node.CreateState()
            
    def get_possible_moves(self, matrix):
        moves = []
        head_pos = np.where(matrix==1)
        head_pos_x = head_pos[1][0]
        head_pos_y = head_pos[0][0]

        if head_pos_x > 0:
            if matrix[head_pos_y][head_pos_x-1] == 0 or matrix[head_pos_y][head_pos_x-1] == -1:
                moves.append("Left")
        if head_pos_x < WIDTH_BOARD//CELL_SIZE-1:
            if matrix[head_pos_y][head_pos_x+1] == 0 or matrix[head_pos_y][head_pos_x+1] == -1:
                moves.append("Right")
        if head_pos_y > 0:
            if matrix[head_pos_y-1][head_pos_x] == 0 or matrix[head_pos_y-1][head_pos_x] == -1:
                moves.append("Up")
        if head_pos_y < HEIGHT_BOARD//CELL_SIZE-1: 
            if matrix[head_pos_y+1][head_pos_x] == 0 or matrix[head_pos_y+1][head_pos_x] == -1:
                moves.append("Down")

        return moves

    def perform_move(self, matrix, move, tempX, tempY):
        val_x = tempX[0]
        val_y = tempY[0]
        tempX = np.roll(tempX, 1)
        tempY = np.roll(tempY, 1)
        speed = CELL_SIZE
        # update head
        if move == 'Left':
            tempX[0] = val_x - speed
            tempY[0] = val_y
        if move == 'Right':
            tempX[0] = val_x + speed
            tempY[0] = val_y
        if move == 'Up':
            tempY[0] = val_y - speed 
            tempX[0] = val_x
        if move == 'Down':
            tempY[0] = val_y + speed 
            tempX[0] = val_x  
        new_matrix = Node(tempX, tempY, food_x, food_y).CreateState()
        return new_matrix, tempX, tempY

    def bfs(self):
        visited = set()
        tempX = self.X.copy()
        tempY = self.Y.copy()
        queue = deque([(self.matrix_state, [], tempX, tempY)])

        while queue:
            current_matrix, path, tempX, tempY = queue.popleft()
            if tempX[0] == food_x and tempY[0] == food_y:
                return path
            for move in self.get_possible_moves(current_matrix):
                new_matrix, newTempX, newTempY = self.perform_move(current_matrix, move, tempX, tempY)
                new_matrix_tuple = tuple(tuple(row) for row in new_matrix)
                if new_matrix_tuple not in visited:
                    visited.add(new_matrix_tuple)
                    new_path = path + [move]
                    queue.append((new_matrix, new_path, newTempX, newTempY))
        

# Call method
X = [255, 260, 265, 270, 275, 280, 285, 290, 295, 300]
Y =  [220, 220, 220, 220, 220, 220, 220, 220, 220, 220]

food_x = 250
food_y = 250
solution = BFS_PATH(X, Y, food_x, food_y).bfs()
print(solution)