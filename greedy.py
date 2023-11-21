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
    
    def greedy_direct(self):
        possible_moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Dưới, Trên, Phải, Trái
        direction_mapping = {(0, 1): RIGHT, (0, -1): LEFT, (1, 0): DOWN, (-1, 0): UP}
        for dx, dy in directions:
            next_x = self.snake_x + dx
            next_y = self.snake_y + dy
            if self.snake_state[next_y][next_x] > EMPTY:
                continue
            if self.snake_state[next_y][next_x] == FOOD:
                return direction_mapping[(dx, dy)];
            if self.snake_state[next_y][next_x] == EMPTY:
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
        
        print(move)
        speed = 5
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
        while not (self.snake_x == self.food_x and self.snake_y == self.food_y):
            print("đầu: ", end='')
            print(self.snake_y, self.snake_x)
            print("thức ăn: ", end='')
            print(self.food_y, self.food_x)
            direct = self.greedy_direct()
            directs.append(direct)
            if self.dist([self.snake_y, self.snake_x], [self.food_y, self.food_x]) <=1:
                break
            snake_new_node = self.move(direct)
            self.updateNode(snake_new_node)
        return directs


# OBSTACLE = -2
# FOOD = -1
# HEAD = 1
# EMPTY = 0

# foodX = 600
# foodY = 550
# snakeY = [610, 610, 610, 610, 610, 610, 610, 610, 610, 610, 610, 610, 610, 610, 610]
# snakeX = [505, 500, 495, 490, 485, 480, 475, 470, 465, 460, 455, 450, 445, 440, 435]
# greedy = Greedy(Node(snakeX,snakeY,foodX,foodY))
# state = greedy.snake_state

# # print(greedy.snake_x)
# # print(greedy.snake_y)
# # print(greedy.food_x)
# # print(greedy.food_y)
# # '''
# # 64
# # 50
# # 49
# # 49
# # '''
# start_time = time.time()
# # print(self.snake_y, self.snake_x)
# print(greedy.find_pos_greedy()) 

# end_time = time.time()

# # Tính thời gian chạy bằng cách lấy hiệu của thời điểm kết thúc và thời điểm bắt đầu
# elapsed_time = end_time - start_time
# print(f"Thời gian chạy: {elapsed_time} giây")

