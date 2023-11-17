import numpy as np
from node import *
import time

class Greedy:
    
    def __init__(self,snake_node):
        self.snake_node = snake_node
        self.snake_state = self.snake_node.CreateState()
        self.snake_x  = snake_node.getPos_Matrix(snake_node.snakeY[0])
        self.snake_y = snake_node.getPos_Matrix(snake_node.snakeX[0])
        self.food_x = snake_node.getPos_Matrix(snake_node.foodY)
        self.food_y  = snake_node.getPos_Matrix(snake_node.foodX)
    
    def greedy_direct(self):

        directs = [DOWN, UP, LEFT, RIGHT]
        pos_distances = np.array([[1, 0], [-1, 0], [0, -1], [0, 1]])

        
        dict_directs = {tuple(distance): direction for distance, direction in zip(pos_distances, directs)}
        not_direct = ""
        for y, x in pos_distances:
            if self.snake_state[self.snake_y + y][self.snake_x + x] != EMPTY and self.snake_state[self.snake_y + y][self.snake_x + x] != FOOD:
                not_direct=dict_directs[(y,x)]
        dict_directs = [key for key, value in dict_directs.items() if value != not_direct]
        
        distances = []
        
        for x,y in dict_directs:
            distances.append(self.dist([self.snake_y+y, self.snake_x+x], [self.food_y, self.food_x]))
        dict_distances = { direct: direction for direct, direction in zip(directs, distances)}
        return min(dict_distances, key=dict_distances.get)

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
        self.__init__(snake_new_node)

    def nearFood(foodY, foodX, snakeY, snakeX, distance_threshold=1):
        # Tính khoảng cách Manhattan giữa đầu rắn và thức ăn
        distance = abs(foodY - snakeY) + abs(foodX - snakeX)
        
        # Kiểm tra xem khoảng cách có nhỏ hơn ngưỡng cho trước hay không
        return distance <= distance_threshold

    def find_pos_greedy(self):
        start_time = time.time()
        directs = []
        while not (self.snake_x == self.food_x and self.snake_y == self.food_y):
            if(time.time()-start_time>=TIME_LIMIT):
                raise TimeoutError(f"over {TIME_LIMIT}s")
            direct = self.greedy_direct()
            directs.append(direct)
            if self.dist([self.snake_y, self.snake_x], [self.food_y, self.food_x]) <=1:
                break
            snake_new_node = self.move(direct)
            self.updateNode(snake_new_node)
        return directs


# snakeX = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
# snakeY = [325, 320, 315, 310, 305, 300, 295, 290, 285, 280]

# foodX = 400
# foodY = 400


# greedy = Greedy(Node(snakeX,snakeY,foodX,foodY))

# print(greedy.snake_x)
# print(greedy.snake_y)
# print(greedy.food_x)
# print(greedy.food_y)
# '''
# 64
# 50
# 49
# 49
# '''
# start_time = time.time()
# print(greedy.find_pos_greedy()) 

# end_time = time.time()

# # Tính thời gian chạy bằng cách lấy hiệu của thời điểm kết thúc và thời điểm bắt đầu
# elapsed_time = end_time - start_time
# print(f"Thời gian chạy: {elapsed_time} giây")
