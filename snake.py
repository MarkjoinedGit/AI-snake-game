import pygame
from pygame.locals import *
import time
import random
import math
'''

'''

WINDOW_WIDTH=1200
WINDOW_HEIGTH=750
SIZE = 25


BACKGROUND_IMG=pygame.image.load(r'assets\background.png')

SNAKE_BLOCK_IMG = pygame.image.load(r'assets\snake\body-anaconda.png')

SNAKE_HEAD_IMG = {
    'left':pygame.image.load(r'assets\snake\head-anaconda-left.png'),
    'right':pygame.image.load(r'assets\snake\head-anaconda-right.png'),
    'up':pygame.image.load(r'assets\snake\head-anaconda-up.png'),
    'down':pygame.image.load(r'assets\snake\head-anaconda-down.png')
}

FOOD_IMG = (
    pygame.image.load(r'assets\foods\food-0.png'),
    pygame.image.load(r'assets\foods\food-1.png'),
    pygame.image.load(r'assets\foods\food-2.png'),
    pygame.image.load(r'assets\foods\food-3.png'),
    pygame.image.load(r'assets\foods\food-4.png'),
    pygame.image.load(r'assets\foods\food-5.png'),
    pygame.image.load(r'assets\foods\food-6.png')   
)

class Food:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = FOOD_IMG[0].convert_alpha()
        self.rect = self.image.get_rect()
        self.x = 120
        self.y = 120
        

    def draw(self):
        self.rect.center = (self.x, self.y)
        self.parent_screen.blit(self.image, self.rect)
        pygame.display.flip()

    def move(self):
        self.x = random.randint(10,WINDOW_WIDTH)
        self.y = random.randint(10,WINDOW_HEIGTH)

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        
        self.direction = 'down'
        self.block = SNAKE_BLOCK_IMG.convert_alpha()
        self.block_rect = self.block.get_rect(center=(-100, -100))
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()
        self.head_rect = self.head.get_rect(center=(-100, -100))
        self.length = 10
        self.x = [SIZE]*self.length
        self.y = [SIZE]*self.length

    def move_left(self):
        self.direction = 'left'
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()

    def move_right(self):
        self.direction = 'right'
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()

    def move_up(self):
        self.direction = 'up'
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()

    def move_down(self):
        self.direction = 'down'
        self.head = SNAKE_HEAD_IMG[self.direction].convert_alpha()

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        speed = SIZE//5
        # update head
        if self.direction == 'left':
            if(self.x[0]<0):
                self.x[0] = WINDOW_WIDTH
            else:
                self.x[0] -= speed
            
        if self.direction == 'right':
            if(self.x[0]>WINDOW_WIDTH):
                self.x[0] = 0               
            else:
                self.x[0] += speed
            
        if self.direction == 'up':
            if(self.y[0]<0):
                self.y[0] = WINDOW_HEIGTH
            else:
                self.y[0] -= speed
        if self.direction == 'down':
            if(self.y[0]> WINDOW_HEIGTH):
                self.y[0] = 0
            else:
                self.y[0] += speed

        self.draw()

    def draw(self):
        d=22
        for i in range(self.length):         
            if self.direction=='left':
                self.block_rect.center = (self.x[i]+d, self.y[i])
                self.head_rect.center = (self.x[i]+d//3, self.y[i])        
            elif self.direction=='right':
                self.block_rect.center = (self.x[i]-d, self.y[i])
                self.head_rect.center = (self.x[i]-d//3, self.y[i])        
            elif self.direction=='up':
                self.block_rect.center = (self.x[i], self.y[i]+d)
                self.head_rect.center = (self.x[i], self.y[i]+d//3)        

            elif self.direction=='down':
                self.block_rect.center = (self.x[i], self.y[i]-d)
                self.head_rect.center = (self.x[i], self.y[i]-d//3)                    
            if(i==0):                  
                self.parent_screen.blit(self.head, self.head_rect)
            elif(i>0 and i<self.length-1):   
                self.parent_screen.blit(self.block, self.block_rect)

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self, screen):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")
        pygame.mixer.init()
        self.play_background_music()

        self.surface = screen
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Food(self.surface)
        self.apple.draw()



    def play_background_music(self):
        pygame.mixer.music.load(r'assets\sounds\forest.wav')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound(r'assets\sounds\crash.wav')
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound(r'assets\sounds\ding.wav')

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Food(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return False
        return False

    def render_background(self):
        bg = BACKGROUND_IMG.convert_alpha()
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.snake.head_rect.colliderect(self.apple.rect):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            if self.snake.direction=='up' or self.snake.direction=='down':
                                self.snake.move_left()

                        if event.key == K_RIGHT:
                            if self.snake.direction=='up' or self.snake.direction=='down':
                                self.snake.move_right()

                        if event.key == K_UP:
                            if self.snake.direction=='left' or self.snake.direction=='right':
                                self.snake.move_up()

                        if event.key == K_DOWN:
                            if self.snake.direction=='left' or self.snake.direction=='right':
                                self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
                
            clock.tick(60)