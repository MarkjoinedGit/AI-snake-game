from node import *
from collections import deque
import numpy as np
from queue import PriorityQueue
from static import *
from queue import Queue
import time
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
    
    def isValid(sefl, mat, visited, row, col):
        return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0])) and ((mat[row][col] == 0) or (mat[row][col] == -1)) and not visited[row][col]
    
    def heuristic(self, row, col, dest_y, dest_x):
        #return abs(row-dest_y) + abs(col-dest_x)
        return math.sqrt((row - dest_y)**2 + (col - dest_x)**2)
    
    def a_star(self):
        mat = self.matrix_state
        src = ((self.Y[0]//CELL_SIZE)-1, (self.X[0]//CELL_SIZE)-1)
        dest = ((self.food_y//CELL_SIZE)-1, (self.food_x//CELL_SIZE)-1)

        # Khởi tạo mảng visited
        visited = [[False for x in range(len(mat[0]))] for y in range(len(mat))]
        self.visited_cost = set()

        # Tạo hàng đợi để lưu trữ các ô của bàn chơi
        q = PriorityQueue()

        # Đánh dấu ô nguồn là đã được thăm và đưa nó vào hàng đợi
        visited[src[0]][src[1]] = True
        q.put((0, src, []))  # (cost, ô hiện tại, danh sách hướng di chuyển)

        # Lặp cho đến khi hàng đợi trống
        while not q.empty():
            # Lấy ra ô hiện tại và danh sách hướng di chuyển từ hàng đợi
            node = q.get()
            (cost, pt, path) = (node[0], node[1], node[2])
            self.visited_cost.add((pt))

            # Nếu ô hiện tại là đích, trả về danh sách hướng di chuyển
            if self.is_collision(pt[0],pt[1],dest[0],dest[1]):
                print("A*: ",pt,dest)
                return path

            # Lấy ra tọa độ của ô hiện tại
            (row, col) = (pt[0], pt[1])

            # Kiểm tra tất cả các ô xung quanh ô hiện tại và đưa chúng vào hàng đợi
            directions = [(0, -1, LEFT), (-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN)]
            for d in directions:
                newRow, newCol = row + d[0], col + d[1]
                newPath = path + [d[2]]
                if self.isValid(mat, visited, newRow, newCol):
                    if ((newRow, newCol)) == dest:
                        return newPath
                    self.moved_pos.append((newCol,newRow))
                    visited[newRow][newCol] = True
                    g = cost + 1  # assuming each move has a cost of 1
                    h = self.heuristic(newRow, newCol, dest[0], dest[1])  # Manhattan distance
                    f = g + h
                    q.put((f, (newRow, newCol), newPath))

        # Nếu không tìm thấy đường đi, trả về None
        return None
    
    def is_collision(self, x1, y1, x2, y2,d=0):
        if x1 >= x2-d and x1 < x2 + 1+d:
            if y1 >= y2-d and y1 <y2 + 1+d:
                return True
        return False
# Call method
# X = [340, 335, 330, 325, 320, 315, 310, 305, 300, 295, 290, 285]
# Y =  [305, 305, 305, 305, 305, 305, 305, 305, 305, 305, 305, 305]
# food_x = 220
# food_y = 110


# foodX = 55
# foodY = 275
# snakeX = [350, 345, 345, 340, 340, 335, 330, 325, 320, 315, 310, 305, 300, 295, 290, -1]
# snakeY = [275, 275, 270, 270, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, -1]
foodX = 135
foodY = 105
snakeX = [105, 110, 115, 115, 115, 115, 110, 105, 105, 105]
snakeY = [105, 105, 105, 100,  95,  90,  90,  90,  85,  80]

#solution = Algorithm(X, Y, food_x, food_y).DFS(10)
b=ASTAR(snakeX, snakeY, foodX, foodY)
solution = b.a_star()
print(solution)
print(len(solution))
print(len(b.visited_cost))

