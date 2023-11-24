import pygame
import queue
import time

# Khởi tạo màn hình game
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Khởi tạo rắn và mồi
snake = [(20, 20)]
food = (10, 10)

# Hàm vẽ rắn và mồi
def draw_window():
    win.fill((0,0,0))
    for pos in snake:
        pygame.draw.rect(win, (0,255,0), (pos[0]*20, pos[1]*20, 20, 20))
    pygame.draw.rect(win, (255,0,0), (food[0]*20, food[1]*20, 20, 20))
    pygame.display.update()

# Hàm tìm đường đi ngắn nhất từ rắn đến mồi sử dụng BFS
def bfs():
    dist = {food: 0}
    prev = {food: None}
    q = queue.Queue()
    q.put(food)
    while not q.empty():
        node = q.get()
        x, y = node
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_node = (x+dx, y+dy)
            if next_node not in dist and next_node not in snake:
                dist[next_node] = dist[node] + 1
                prev[next_node] = node
                q.put(next_node)
    return prev

# Hàm di chuyển rắn
def move_snake():
    prev = bfs()
    if snake[0] not in prev:
        return
    while snake[0] != food:
        draw_window()
        snake.insert(0, prev[snake[0]])
        if snake[0] != food:
            snake.pop()
        time.sleep(0.1)

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        move_snake()
    pygame.quit()

if __name__ == "__main__":
    main()
