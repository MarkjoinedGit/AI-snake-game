import numpy as np
from node import *
import time

# Ghi lại thời điểm bắt đầu



class Greedy:
    
    def __init__(self,snake_node):
        self.snake_node = snake_node
        self.snake_state = self.snake_node.CreateState()
        food_pos = np.where(self.snake_state == -1)
        head_snake_pos = np.where(self.snake_state == 1)
        self.snake_x  = head_snake_pos[0][0]
        self.snake_y = head_snake_pos[1][0]
        self.food_x = food_pos[0][0]
        self.food_y  = food_pos[1][0]
    
    def greedy_direct(self):

        directs = [DOWN, UP, LEFT, RIGHT]
        pos_distances = np.array([[1, 0], [-1, 0], [0, -1], [0, 1]])

        
        dict_directs = {tuple(distance): direction for distance, direction in zip(pos_distances, directs)}
        not_direct = ""
        for y, x in pos_distances:
            if self.snake_state[self.snake_y + y][self.snake_x + x] != EMPTY and snake_state[self.snake_y + y][self.snake_x + x] != FOOD:
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


EMPTY = 0
FOOD = -1
HEAD = 1

snakeX = [745, 740, 735, 730, 725, 720, 715, 710, 705, 700, 695, 690, 685, 680, 675, 670, 665, 660]
snakeY = [405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405, 405]

foodX = 635
foodY = 325

snake_node = Node(snakeX,snakeY,foodX,foodY)
DOWN = 'DOWN'
UP = 'UP'
LEFT = 'LEFT'
RIGHT = 'RIGHT'


greedy = Greedy(snake_node)

start_time = time.time()

print(greedy.find_pos_greedy())

end_time = time.time()

# Tính thời gian chạy bằng cách lấy hiệu của thời điểm kết thúc và thời điểm bắt đầu
elapsed_time = end_time - start_time
print(f"Thời gian chạy: {elapsed_time} giây")
