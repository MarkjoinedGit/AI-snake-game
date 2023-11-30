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
    
    def heuristic(self, row, col, dest_y, dest_x):
        return abs(row-dest_y) + abs(col-dest_x)
    
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
        new_node = Node(tempX, tempY, self.food_x, self.food_x)
        new_node.obstacles=self.obstacles
        new_matrix = new_node.CreateState()
        return new_matrix, tempX, tempY
    
    def hill_climbing(self):
        current_distance = self.heuristic(self.Y[0]//CELL_SIZE, self.X[0]//CELL_SIZE, self.food_y//CELL_SIZE, self.food_x//CELL_SIZE)
        while True:
            best_distance = current_distance
            best_move = None
            for move in self.get_possible_moves(self.matrix_state):
                tempX = self.X.copy()
                tempY = self.Y.copy()
                newNode = self.perform_move(self.matrix_state, move, tempX, tempY)
                new_distance = self.heuristic(newNode.snakeY[0]//CELL_SIZE, newNode.snakeX[0]//CELL_SIZE, self.food_y//CELL_SIZE, self.food_x//CELL_SIZE)
                if new_distance < best_distance:
                    best_distance = new_distance
                    best_move = move
            
            if best_move:
                tempX = self.X.copy()
                tempY = self.Y.copy()
                newNode = self.perform_move(self.matrix_state, move, tempX, tempY)
               
                self.X = newNode.snakeX
                self.Y = newNode.snakeY
                self.matrix_state = newNode.CreateState()
                current_distance = best_distance
                # Thêm đỉnh mới vào danh sách self.moved_pos
                self.moved_pos.append((self.X[0]//CELL_SIZE, self.Y[0]//CELL_SIZE))
                print(f"Moved to: {self.X[0]//CELL_SIZE}, {self.Y[0]//CELL_SIZE}")  # In ra đỉnh đã đi qua
            else:
                break
if __name__ == "__main__":
    initial_Y = [345, 340, 335, 330, 325, 320, 315, 310, 305, 300, 295, 290, 285, 280, 275, 270, 265, 260]  # Thay thế giá trị ban đầu cho X và Y tại đây
    initial_X = [405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405]
    food_x = 250  # Thay thế giá trị thức ăn X và Y tại đây
    food_y = 250

    astar = HillClimbing(initial_X, initial_Y, food_x, food_y,{})
    astar.hill_climbing()  # Gọi phương thức Hill Climbing

    # In ra đường đi sau khi tối ưu
    print("Optimized path:")
    optimized_path = astar.moved_pos
    print(optimized_path)# Không có bước di chuyển nào cải thiện được nữa
