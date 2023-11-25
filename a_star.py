import numpy as np
from node import *
from static import *
import time
from queue import PriorityQueue 

class AStar:
    def __init__(self,snake_node:Node):
        self.snake_node = snake_node
        self.snake_state = self.snake_node.CreateState()
        self.moved_pos=[]
        self.depth_limit=DEPTH_LIMIT
        self.visited= set()
        self.path=[]  
    
    def find_pos_a_star(self):
        self.frontier = PriorityQueue()
        self.explored_set = []
        self.visited=[]
        self.frontier.put(self.snake_node)
        runing=True
        
        while not self.frontier.empty() and runing == True :          
            lowest_node = self.frontier.get()
            # print(f"================================={self.frontier.qsize()}==================================")
            # lowest_node.print('lowest_node')
            current_state = lowest_node.CreateState()
            if lowest_node.is_collision():
                # lowest_node.print('final')
                return lowest_node.get_path()
            directions = [LEFT,RIGHT,UP,DOWN]
            
            self.explored_set.append(lowest_node)
            for move in directions:  
                
                neighbor = lowest_node.move(move)
                next_x= posGame_to_posMatrix(neighbor.snakeX[0])
                next_y= posGame_to_posMatrix(neighbor.snakeY[0])
                
                if current_state[next_y][next_x] > EMPTY or current_state[next_y][next_x] == OBSTACLE or neighbor in self.explored_set:
                    # neighbor.print('continue-neighbor')
                    # print((next_x,next_y))
                    # print(current_state[next_y][next_x])
                    # print(current_state[next_y][next_x])
                    # print(neighbor in self.explored_set)
                    continue
                
                self.moved_pos.append((next_x,next_y))

                g = lowest_node.g + 1
                best = False
                
                nodes= np.array(self.frontier)
                if neighbor not in nodes:
                    neighbor.dist()  
                    self.frontier.put(neighbor)             
                    best = True
                elif lowest_node.g < neighbor.g:
                    
                    best = True  
                if best:
                    neighbor.parent = lowest_node
                    neighbor.g = g
                    neighbor.f = neighbor.g + neighbor.h      
                     
                       
                # neighbor.print('neighbor')   
        return None   

        
            

# Call method
# X = [340, 335, 330, 325, 320, 315, 310, 305, 300, 295, 290, 285]
# Y =  [305, 305, 305, 305, 305, 305, 305, 305, 305, 305, 305, 305]
# food_x = 280
# food_y = 310

# X = [255, 260, 265, 270, 275, 280, 285, 290, 295, 300]
# Y = [220, 220, 220, 220, 220, 220, 220, 220, 220, 220]
# food_x = 410
# food_y = 305

# X =[255, 255, 255, 255, 255, 255, 255, 260, 265, 270]
# Y =[250, 245, 240, 235, 230, 225, 220, 220, 220, 220]
# food_x,food_y= (250, 250)

# X = [775, 775, 770, 765, 760, 755, 750, 745, 740, 735, 730, 725, 720, 715, 710, 705, 700, 695, 690, 685, 680, 675, 670, 665, 660, 655, 650, 645, 640, 635, 630, 625, 620, 615, 610, 605, 600, 595, 590, 585, 580, 575, 570, 565]  
# Y = [600, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595] 
# food_x = 580
# food_y = 150
# X =posMatrix_to_posGame_list([20,21,22,22,22,22,21,20,20,20]) 
# Y =posMatrix_to_posGame_list([20,20,20,19,18,17,17,17,16,15]) 
# food_x,food_y= tuple(posMatrix_to_posGame_list([8,20]) )
# d=AStar(Node(X, Y, food_x, food_y))
# solution = d.find_pos_a_star()
# print(d.moved_pos)




