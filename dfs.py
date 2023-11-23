from node import *
from collections import deque
import numpy as np
from queue import PriorityQueue
from static import *
from queue import Queue
import time
class DFS:
    def __init__(self, initial_X, initial_Y, food_x, food_y):
        self.X = initial_X
        self.Y = initial_Y
        self.food_x = food_x
        self.food_y = food_y
        self.node = Node(self.X, self.Y, self.food_x, self.food_y)
        self.matrix_state = self.node.CreateState()
        self.moved_pos=[]    
        self.src = ((self.Y[0]//CELL_SIZE)-1, (self.X[0]//CELL_SIZE)-1)
        self.dest = ((self.food_y//CELL_SIZE)-1, (self.food_x//CELL_SIZE)-1)
        self.depth_limit=DEPTH_LIMIT
        self.visited= set()  
        self.stack=[]
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
        return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0])) and (mat[row][col] != -2) and not visited[row][col]
   
    def recursive_DFS(self,matrix,tempX,tempY, path, depth):
        if tempX[0] == self.food_x and tempY[0] == self.food_y:
            print("AAAAAAAAAAAA FInish")
            return path
        if depth == self.depth_limit:
            print("AAAAAAAAAAAA depth_limit")
            return None
        for d in DIRECTIONS:
            move = d[2]
            new_matrix , new_tempX , new_tempY = self.perform_move(matrix,move,tempX,tempY)
            newRow=new_tempX[0]
            newCol=new_tempY[0]
            print(move)
            print(new_tempX)
            print(new_tempY)
            print(path)
            new_state= (newCol,newRow)
            self.moved_pos.append(new_state)
            if new_state not in self.visited:
                self.visited.add(tuple(new_state))
                new_path = path + [move]
                result = self.recursive_DFS(new_matrix,new_tempX,new_tempY, new_path, depth + 1)
                if result:
                    return result
    def dfs(self): 
        self.visited=set()
        self.stack=[]  
        self.stack.append((self.matrix_state, [])) 
        while self.stack:
            current_state, path = self.stack.pop()
            result = self.recursive_DFS(current_state,self.X,self.Y,path,0)
            if result:
                return result
        return None
# Call method
X = [340, 335, 330, 325, 320, 315, 310, 305, 300, 295, 290, 285]
Y =  [305, 305, 305, 305, 305, 305, 305, 305, 305, 305, 305, 305]
food_x = 220
food_y = 110
# X = [255, 260, 265, 270, 275, 280, 285, 290, 295, 300]
# Y = [220, 220, 220, 220, 220, 220, 220, 220, 220, 220]
# food_x = 250
# food_y = 250

d=DFS(X, Y, food_x, food_y)
solution = d.dfs()
print(solution)
