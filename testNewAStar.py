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
        # print(initial_X)
        # print(initial_Y)
        # print(food_x)
        # print(food_y)
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
        # print(tempX)
        # print(tempY)
        # print(self.food_x)
        # print(self.food_y)

        # Khởi tạo mảng visited
        visited = [[False for x in range(len(mat[0]))] for y in range(len(mat))]
        self.visited_cost = set()

        # Tạo hàng đợi để lưu trữ các ô của bàn chơi
        q = PriorityQueue()

        # Đánh dấu ô nguồn là đã được thăm và đưa nó vào hàng đợi
        visited[src[0]][src[1]] = True
        q.put((0, 0, src, [], tempX, tempY, mat))  # (cost, H, ô hiện tại, danh sách hướng di chuyển)

        # Lặp cho đến khi hàng đợi trống
        while not q.empty():
            # Lấy ra ô hiện tại và danh sách hướng di chuyển từ hàng đợi
            node = q.get()
            (F, cost, pt, path, tempX, tempY, mat) = (node[0], node[1], node[2], node[3], node[4], node[5], node[6])
            self.visited_cost.add((pt))

            # Lấy ra tọa độ của ô hiện tại
            (row, col) = (pt[0], pt[1])

            # Kiểm tra tất cả các ô xung quanh ô hiện tại và đưa chúng vào hàng đợi
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
                    newCost = cost + 1  # assuming each move has a cost of 1
                    newH = self.heuristic(newRow, newCol, dest[0], dest[1])  # Manhattan distance
                    f = newCost + newH
                    q.put((f, newCost, (newRow, newCol), newPath, newTempX, newTempY, newMat))

        # Nếu không tìm thấy đường đi, trả về None
        return Queue()
    
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
# foodX = 380
# foodY = 100
# snakeX = [460, 460, 460, 460, 460, 460, 460, 460, 460, 460, 455, 450, 445, 440, 435, 430, 425, 420, 415, 410, 405, 400, 395, 390, 385, 380, 375, 370, 365, 360, 355, 350, 345, 340, 335, 330, 325, 320, 315, 310, 305, 300, 295, 290, 285, 280, 275, 270, 265, 260, 255, 250, 245, 240, 235, 230, 225, 220, 215, 210, 205, 200, 195, 190, 185, 180, 175, 170, 165, 160, 155, 150, 145, 140, 135, 130, 125, 120, 115, 110, 105, 100, 95, 90, 85, 85, 85, 85, 85, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 45, 50, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 55, 50, 45, 45, 45, 45, 45, 50, 55, 60, 60, 60, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, -1]
# snakeY = [155, 150, 145, 140, 135, 130, 125, 120, 115, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 115, 120, 125, 130, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 190, 190, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300, 305, 310, 310, 305, 300, 295, 290, 285, 280, 275, 270, 265, 260, 255, 250, 245, 240, 235, 230, 225, 220, 215, 210, 205, 200, 195, 190, 185, 185, 185, 185, 180, 175, 170, 165, 165, 165, 165, 160, 155, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, -1] 

# #solution = Algorithm(X, Y, food_x, food_y).DFS(10)
# b=ASTAR(snakeX, snakeY, foodX, foodY)
# solution = b.a_star()
# print(solution)
# print(b.moved_pos)
# food_mat_x = posGame_to_posMatrix(b.food_x)
# food_mat_y = posGame_to_posMatrix(b.food_y)
# print(posMatrix_to_posGame(food_mat_x))
# print(posMatrix_to_posGame(food_mat_y))
# print(posMatrix_to_posGame_list(b.moved_pos))
# print(len(b.visited_cost))

