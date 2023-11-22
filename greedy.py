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
        self.moved_pos=[]
    
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
                self.moved_pos.append((next_x,next_y))
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
            direct = self.greedy_direct()
            directs.append(direct)
            if self.dist([self.snake_y, self.snake_x], [self.food_y, self.food_x]) <=1:
                break
            snake_new_node = self.move(direct)
            self.updateNode(snake_new_node)
        return directs



# foodX = 580
# foodY = 150
# snakeX = [775, 775, 770, 765, 760, 755, 750, 745, 740, 735, 730, 725, 720, 715, 710, 705, 700, 695, 690, 685, 680, 675, 670, 665, 660, 655, 650, 645, 640, 635, 630, 625, 620, 615, 610, 605, 600, 595, 590, 585, 580, 575, 570, 565]  
# snakeY = [600, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595, 595] 
# greedy = Greedy(Node(snakeX,snakeY,foodX,foodY))
# state = greedy.snake_state


# start_time = time.time()
# print(greedy.find_pos_greedy()) 
# print(greedy.moved_pos)
# end_time = time.time()

# # Tính thời gian chạy bằng cách lấy hiệu của thời điểm kết thúc và thời điểm bắt đầu
# elapsed_time = end_time - start_time
# print(f"Thời gian chạy: {elapsed_time} giây")

