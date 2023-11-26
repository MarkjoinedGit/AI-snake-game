import numpy as np
from node import *
from static import *
import time

class Greedy:
    
    def __init__(self,snake_node):
        self.snake_node = snake_node
        self.snake_state = self.snake_node.CreateState()
        food_pos = np.where(self.snake_state == -1)
        head_snake_pos = np.where(self.snake_state == 1)
        self.snake_x  = head_snake_pos[1][0]
        self.snake_y = head_snake_pos[0][0]
        self.food_x = food_pos[1][0]
        self.food_y  = food_pos[0][0]
        self.moved_pos=set()
    
    # def not_around(self,next_y, next_x, direct):
    #     snake_new_node = self.move(direct)
    #     state = snake_new_node.CreateState()
    #     state_row = state[next_y][:]
    #     state_col = state[:][next_x]
    #     count = 0
    #     for i in range(next_x+1, len(state_row)):
    #         if state_row[i] >1 :
    #             count = count+1
    #             break
            
    #     for i in range(next_x-1, 0,-1):
    #         if state_row[i] >1:
    #             count = count+1
    #             break
            
    #     for i in range(next_y+1, len(state_col)):
    #         if state_col[i] >1:
    #             count = count+1
    #             break
            
    #     for i in range(next_y-1, 0,-1):
    #         if state_col[i] >1:
    #             count = count+1
    #             break
    #     print(count)
    #     return count < 4
    
    def greedy_direct(self):
        possible_moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Dưới, Trên, Phải, Trái
        direction_mapping = {(0, 1): RIGHT, (0, -1): LEFT, (1, 0): DOWN, (-1, 0): UP}
        for dx, dy in directions:
            next_x = self.snake_x + dx
            next_y = self.snake_y + dy
            if self.snake_state[next_y][next_x] > EMPTY or self.snake_state[next_y][next_x] == OBSTACLE:
                continue
            if self.snake_state[next_y][next_x] == FOOD:
                return direction_mapping[(dx, dy)]
            if self.snake_state[next_y][next_x] == EMPTY:
                self.moved_pos.add((next_x,next_y))
                distance_to_food = abs(next_x - self.food_x) + abs(next_y - self.food_y)
                possible_moves.append((distance_to_food, direction_mapping[(dy, dx)]))
        if possible_moves:
            possible_moves.sort()  # Sắp xếp theo khoảng cách tăng dần
            next_move = possible_moves[0][1]
            return next_move
        else:
            # Không có hướng di chuyển hợp lệ
            return None
    
    def dist(self,state, goal):
        dist = abs(goal[0] - state[0]) + abs(goal[1] - state[1])
        return dist
    
    def move(self, move):
        snakeX = self.snake_node.snakeX
        snakeY = self.snake_node.snakeY

        head_x, head_y = snakeX[0], snakeY[0]

        snakeX = np.roll(snakeX, 1)
        snakeY = np.roll(snakeY, 1)
    
        speed = CELL_SIZE
        if move == LEFT :
            snakeY[0] = head_y
            snakeX[0] = head_x - speed
        if move == RIGHT:
            snakeY[0] = head_y 
            snakeX[0] = head_x + speed 
        if move == UP:
            snakeX[0] = head_x
            snakeY[0] = head_y - speed
        if move == DOWN:
            snakeX[0] = head_x 
            snakeY[0] = head_y + speed
        new_node = Node(snakeX, snakeY, self.snake_node.foodX, self.snake_node.foodY)
        return new_node

    def updateNode(self, snake_new_node):
        self.snake_node = snake_new_node
        self.snake_state = self.snake_node.CreateState()
        food_pos = np.where(self.snake_state == -1)
        head_snake_pos = np.where(self.snake_state == 1)
        self.snake_x  = head_snake_pos[1][0]
        self.snake_y = head_snake_pos[0][0]
        self.food_x = food_pos[1][0]
        self.food_y  = food_pos[0][0]

    def find_pos_greedy(self):
        directs = []
        # while not (self.snake_x == self.food_x and self.snake_y == self.food_y):
        while not self.is_collision(self.snake_x,self.snake_y, self.food_x, self.food_y):
            direct = self.greedy_direct()
            directs.append(direct)
            if self.dist([self.snake_y, self.snake_x], [self.food_y, self.food_x]) <=1:
                break
            snake_new_node = self.move(direct)
            self.updateNode(snake_new_node)
        return directs
    
    def is_collision(self, x1, y1, x2, y2,d=1):
        if x1 >= x2-d and x1 < x2 + CELL_SIZE+d:
            if y1 >= y2-d and y1 <y2 + CELL_SIZE+d:
                return True
        return False
    
# snakeX = [255, 260, 265, 270, 275, 280, 285, 290, 295, 300]
# snakeY = [220, 220, 220, 220, 220, 220, 220, 220, 220, 220]
# foodX = 250
# foodY = 250

# foodX = 580
# foodY = 150
# snakeX = [775, 775, 770, 765, 760, 755, 750, 745, 740, 735, 730, 725, 720, 715, 710, 705, 700, 695, 690, 685, 680, 675, 670, 665, 660, 655, 650, 645, 640, 635, 630, 625, 620, 615, 610, 605, 600, 595, 590, 585, 580, 575, 570, 565]  
# snakeY = [600, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595] 
# greedy = Greedy(Node(snakeX,snakeY,foodX,foodY))
# state = greedy.snake_state


# start_time = time.time()
# p=greedy.find_pos_greedy()
# print(f'path({len(p)})= ',p) 
# # print(greedy.moved_pos)
# end_time = time.time()

# # Tính thời gian chạy bằng cách lấy hiệu của thời điểm kết thúc và thời điểm bắt đầu
# elapsed_time = end_time - start_time
# print(f"Thời gian chạy: {elapsed_time} giây")

