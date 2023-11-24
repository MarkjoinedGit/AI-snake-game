import numpy as np
from node import *
from static import *
import time

class AStar:
    def __init__(self,snake_node:Node):
        self.snake_node = snake_node
        self.snake_state = self.snake_node.CreateState()
        self.moved_pos=[]
        self.depth_limit=DEPTH_LIMIT
        self.visited= set()  
    
    def find_pos_a_star(self):
        self.frontier = []
        self.explored_set = []
        self.path = []
        self.visited=[]
        self.frontier.append(self.snake_node)
        start=time.time()
        runing=True
        
        while len(self.frontier) >0 and runing == True :
            if(time.time()-start>TIME_LIMIT):
                runing=False 
                
            lowest_index = 0
            for i in range(len(self.frontier)):
                if self.frontier[i].f < self.frontier[0].f:
                    lowest_index = i
                    
            print("--------------<3-----------------")
            print(len(self.frontier))
            lowest_node = self.frontier.pop(lowest_index)
        
            print("X= ",lowest_node.snakeX)
            print("Y= ",lowest_node.snakeY)
            print("Food= ",(lowest_node.foodX,lowest_node.foodY))
            print("direction= ",lowest_node.direction)
            print("g= ",lowest_node.g)
            print("h= ",lowest_node.h)
            print("f= ",lowest_node.f)
            
            # if lowest_node.snakeX[0] == lowest_node.foodX and lowest_node.snakeY[0] == lowest_node.foodY :
            if self.is_collision(lowest_node.snakeX[0],lowest_node.snakeY[0],lowest_node.foodX,lowest_node.foodY):
                print("Finishhhhhhhhhhhhhhhhhhhh!")
                return self.get_path(lowest_node)
            self.explored_set.append(lowest_node)  # mark visited
   
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Dưới, Trên, Phải, Trái
            direction_mapping = {(0, 1): RIGHT, (0, -1): LEFT, (1, 0): DOWN, (-1, 0): UP}
            for dx, dy in directions:
                next_x = lowest_node.getPos_Matrix(lowest_node.snakeX[0]) + dx
                next_y = lowest_node.getPos_Matrix(lowest_node.snakeY[0]) + dy
                move=direction_mapping[(dy,dx)]
                neighbor = lowest_node.move(move)
                current_state = lowest_node.CreateState()
                if current_state[next_y][next_x] > EMPTY or neighbor in self.explored_set:
                    print("continue")
                    continue
                if current_state[next_y][next_x] == EMPTY:
                    self.moved_pos.append((next_x,next_y))
                    g = lowest_node.g + 1
                    best = False
                    if neighbor not in self.frontier:
                        neighbor.h = abs(next_x - neighbor.getPos_Matrix(neighbor.foodX)) + abs(next_y - neighbor.getPos_Matrix(neighbor.foodY))
                        self.frontier.append(neighbor)
                        best = True
                    elif lowest_node.g < neighbor.g:  # has already been visited
                        best = True  
                    if best:
                        neighbor.parent = lowest_node
                        neighbor.g = g
                        neighbor.f = neighbor.g + neighbor.h
                    
        return None   
    def is_collision(self, x1, y1, x2, y2,d=0):
        if x1 >= x2-d and x1 < x2 + CELL_SIZE+d:
            if y1 >= y2-d and y1 <y2 + CELL_SIZE+d:
                return True
        return False
    
    def get_path(self, node:Node):
        if node.parent == None:
            return node.direction
        while node.parent.parent != None:
            self.path.append(node.direction)
            node = node.parent
        return  self.path
    def manhattan_distance(self, nodeA, nodeB):
        distance_1 = abs(nodeA.x - nodeB.x)
        distance_2 = abs(nodeA.y - nodeB.y)
        return distance_1 + distance_2
# # Call method
# # X = [340, 335, 330, 325, 320, 315, 310, 305, 300, 295, 290, 285]
# # Y =  [305, 305, 305, 305, 305, 305, 305, 305, 305, 305, 305, 305]
# # food_x = 280
# # food_y = 310

# X = [255, 260, 265, 270, 275, 280, 285, 290, 295, 300]
# Y = [220, 220, 220, 220, 220, 220, 220, 220, 220, 220]
# food_x = 250
# food_y = 225

# # # X = [775, 775, 770, 765, 760, 755, 750, 745, 740, 735, 730, 725, 720, 715, 710, 705, 700, 695, 690, 685, 680, 675, 670, 665, 660, 655, 650, 645, 640, 635, 630, 625, 620, 615, 610, 605, 600, 595, 590, 585, 580, 575, 570, 565]  
# # # Y = [600, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595] 
# # # food_x = 580
# # # food_y = 150

# d=AStar(Node(X, Y, food_x, food_y))
# solution = d.find_pos_a_star()
# print(solution)

