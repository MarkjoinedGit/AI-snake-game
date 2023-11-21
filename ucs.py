import heapq
import numpy as np
from node import *
from static import *
import time

class UCS:
    def __init__(self, snake_node):
        self.snake_node = snake_node
        self.snake_state = self.snake_node.CreateState()
        food_pos = np.where(self.snake_state == -1)
        head_snake_pos = np.where(self.snake_state == 1)
        self.snake_x  = head_snake_pos[1][0]
        self.snake_y = head_snake_pos[0][0]
        self.food_x = food_pos[1][0]
        self.food_y  = food_pos[0][0]

    def is_goal(self,y, x):
        return self.food_y == y and self.food_x == x
    
    def is_valid(self,value):
        return FOOD <= value and value <= EMPTY

    def find_priority_move(self):
        priority = (-1 if self.snake_y - self.food_y < 0 else 1,\
                    -1 if self.snake_x - self.food_x > 0 else 1)
        if self.snake_y == self.food_y:  # Điểm nằm ngang với điểm thức ăn
            priority = (0, priority[1])
        elif self.snake_x == self.food_x:  # Điểm nằm dọc với điểm thức ăn
            priority = (priority[0], 0)
        else:  # Điểm nằm ở một góc so với điểm thức ăn
            priority = (priority[0], priority[1])
            
        priority_move = {( 1, 1):[(-1, 0),(0, 1)], # Thức ăn nằm bên phải trên
                         ( 1,-1):[(-1, 0),(0,-1)], # Thức ăn nằm bên trái trên
                         (-1,-1):[( 0,-1),(1, 0)], # Thức ăn nằm bên trái dưới
                         (-1, 1):[( 0, 1),(1, 0)], # Thức ăn nằm bên phải dưới
                         ( 0, 1):[( 0, 1)],  # Thức ăn nằm bên phải
                         ( 0,-1):[( 0,-1)],  # Thức ăn nằm bên trái
                         ( 1, 0):[(-1, 0)],  # Thức ăn nằm phía trên
                         (-1, 0):[( 1, 0)]}  # Thức ăn nằm phía dưới

        return priority_move[priority]

    def move(self, move):
        snakeX = self.snake_node.snakeX
        snakeY = self.snake_node.snakeY

        head_x, head_y = snakeX[0], snakeY[0]

        snakeX = np.roll(snakeX, 1)
        snakeY = np.roll(snakeY, 1)
        
        # print(move)
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

    def dist(self,state, goal):
        dist = abs(goal[0] - state[0]) + abs(goal[1] - state[1])
        return dist

    def ucs_snake_game(self):
        directs = []
        
        # Khởi tạo hàng đợi ưu tiên
        priority_queue = [(0, (self.snake_y, self.snake_x, []))]  # (cost, (x, y, path))
        visited = set()
        
        while priority_queue:
            cost, (x, y, path) = heapq.heappop(priority_queue)
            if (x, y) not in visited:
                visited.add((y, x))
                path = path + [(y, x)]
                # directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                directions = self.find_priority_move()
                # print(directions)
                direction_mapping = {(0, 1): RIGHT, (0, -1): LEFT, (1, 0): DOWN, (-1, 0): UP}
                direction_mapping = {key: value for key, value in direction_mapping.items() if key in directions}
                for dy, dx in directions:
                    new_x, new_y = x + dx, y + dy
                    if self.is_valid(self.snake_state[new_y,new_x]) and (new_y, new_x) not in visited:
                        heapq.heappush(priority_queue, (cost + 1, (new_y, new_x, path)))
                        directs.append(direction_mapping[(dy, dx)])
                        if self.dist([self.snake_y, self.snake_x], [self.food_y, self.food_x]) <=1:
                            return directs
                        snake_new_node = self.move(direction_mapping[(dy, dx)])
                        self.updateNode(snake_new_node)
        return None
    # Hàm kiểm tra xem điểm có nằm trong biên của ma trận không
    


# foodX = 300
# foodY = 350
# snakeY = [610, 610, 610, 610, 610, 610, 610, 610, 610, 610, 610, 610, 610, 610, 610]
# snakeX = [505, 500, 495, 490, 485, 480, 475, 470, 465, 460, 455, 450, 445, 440, 435]
# ucs = UCS(Node(snakeX,snakeY,foodX,foodY))
# state = ucs.snake_state


# start_time = time.time()
# # print(self.snake_y, self.snake_x)
# print(ucs.ucs_snake_game()) 

# end_time = time.time()

# # Tính thời gian chạy bằng cách lấy hiệu của thời điểm kết thúc và thời điểm bắt đầu
# elapsed_time = end_time - start_time
# print(f"Thời gian chạy: {elapsed_time} giây")


