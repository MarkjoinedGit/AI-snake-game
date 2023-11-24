from node import *
from collections import deque
import numpy as np
from queue import PriorityQueue
from static import *
from queue import Queue
import time
import random


class DFS:
    def __init__(self, initial_X, initial_Y, food_x, food_y):
        self.X = initial_X
        self.Y = initial_Y
        self.food_x = food_x
        self.food_y = food_y
        self.node = Node(self.X, self.Y, self.food_x, self.food_y)
        self.matrix_state = self.node.CreateState()
        self.moved_pos=[]  
    
    def isValid(sefl, mat, visited, row, col):
        return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0])) and ((mat[row][col] == 0) or (mat[row][col] == -1)) and not visited[row][col]
    
    def dfs(self):
        mat = self.matrix_state
        src = ((self.Y[0]//CELL_SIZE)-1, (self.X[0]//CELL_SIZE)-1)
        dest = ((self.food_y//CELL_SIZE)-1, (self.food_x//CELL_SIZE)-1)
        visited = [[False for x in range(len(mat[0]))] for y in range(len(mat))]
        stack = []
        visited[src[0]][src[1]] = True
        stack.append((src, []))
        while stack:
            node = stack.pop()
            (pt, path) = (node[0], node[1])
            if pt == dest:
                print("dfs: ",pt,dest)
                return path
            (row, col) = (pt[0], pt[1])
            directions = [(0, -1, LEFT), (-1, 0, UP), (0, 1, RIGHT), (1, 0, DOWN)]
            for d in directions:
                newRow, newCol = row + d[0], col + d[1]
                if self.isValid(mat, visited, newRow, newCol):
                    self.moved_pos.append((newCol,newRow))
                    visited[newRow][newCol] = True
                    stack.append(((newRow, newCol), path + [d[2]]))
        return None
    
    # def get_possible_moves(self, matrix):
    #     moves = []
    #     head_pos = np.where(matrix==1)
    #     head_pos_x = head_pos[1][0]
    #     head_pos_y = head_pos[0][0]

    #     if head_pos_x > 0:
    #         if matrix[head_pos_y][head_pos_x-1] == 0 or matrix[head_pos_y][head_pos_x-1] == -1:
    #             moves.append(LEFT)
    #     if head_pos_x < WIDTH_BOARD//CELL_SIZE-1:
    #         if matrix[head_pos_y][head_pos_x+1] == 0 or matrix[head_pos_y][head_pos_x+1] == -1:
    #             moves.append(RIGHT)
    #     if head_pos_y > 0:
    #         if matrix[head_pos_y-1][head_pos_x] == 0 or matrix[head_pos_y-1][head_pos_x] == -1:
    #             moves.append(UP)
    #     if head_pos_y < HEIGHT_BOARD//CELL_SIZE-1: 
    #         if matrix[head_pos_y+1][head_pos_x] == 0 or matrix[head_pos_y+1][head_pos_x] == -1:
    #             moves.append(DOWN)

    #     return moves
    

# class DFS:
    
#     def __init__(self,snake_node):
#         self.snake_node = snake_node
#         self.snake_state = self.snake_node.CreateState()
#         self.moved_pos=[]
#         self.depth_limit=DEPTH_LIMIT
#         self.visited= set()  
#     def recursive_DFS(self,init_node:Node, path, depth):
#         if init_node.snakeX[0]== init_node.foodX and init_node.snakeY[0] == init_node.foodY :
#             return path
#         if depth == self.depth_limit:
#             return None
#         current_state= init_node.CreateState()
#         # print("----------------------------------")
#         # print(init_node.snakeX)
#         # print(init_node.snakeY)
#         # print(path)
#         # print(depth)
#         possible_moves = []
#         directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Dưới, Trên, Phải, Trái
#         direction_mapping = {(0, 1): RIGHT, (0, -1): LEFT, (1, 0): DOWN, (-1, 0): UP}
#         for dx, dy in directions:
#             next_x = init_node.getPos_Matrix(init_node.snakeX[0]) + dx
#             next_y = init_node.getPos_Matrix(init_node.snakeY[0]) + dy
#             if current_state[next_y][next_x] > EMPTY:
#                 continue
#             if current_state[next_y][next_x] == EMPTY:
#                 self.moved_pos.append((next_x,next_y))
#                 distance_to_food = abs(next_x - init_node.getPos_Matrix(init_node.foodX)) + abs(next_y - init_node.getPos_Matrix(init_node.foodY))
#                 possible_moves.append((distance_to_food, direction_mapping[(dy, dx)]))
#         if possible_moves:  
#             #np.random.shuffle(possible_moves) 
#             possible_moves.sort()
#             for d,move in possible_moves:
#                 new_node= init_node.move(move)         
#                 if new_node not in self.visited:
#                     self.visited.add(new_node)
#                     new_path = path + [move]
#                     result = self.recursive_DFS(new_node, new_path, depth + 1)
#                     if result:
#                         return result
#         else:
#             return None
    
#     def find_pos_dfs(self):
#         self.visited=set()
#         result = self.recursive_DFS(self.snake_node,[],0)
#         while result == None:
#             result = self.recursive_DFS(self.snake_node,[],0)
#         return result
# Call method
# X = [340, 335, 330, 325, 320, 315, 310, 305, 300, 295, 290, 285]
# Y =  [305, 305, 305, 305, 305, 305, 305, 305, 305, 305, 305, 305]
# food_x = 280
# food_y = 310

# X = [255, 260, 265, 270, 275, 280, 285, 290, 295, 300]
# Y = [220, 220, 220, 220, 220, 220, 220, 220, 220, 220]
# food_x = 250
# food_y = 225

# X = [775, 775, 770, 765, 760, 755, 750, 745, 740, 735, 730, 725, 720, 715, 710, 705, 700, 695, 690, 685, 680, 675, 670, 665, 660, 655, 650, 645, 640, 635, 630, 625, 620, 615, 610, 605, 600, 595, 590, 585, 580, 575, 570, 565]  
# Y = [600, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595] 
# food_x = 580
# food_y = 150

# d=DFS(Node(X, Y, food_x, food_y))
# solution = d.find_pos_dfs()
# print(solution)

# print(d.moved_pos)
