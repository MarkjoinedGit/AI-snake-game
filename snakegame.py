import pygame
import numpy as np
from pygame.locals import *
from snake import *
from food import *
import buttons as btn
from static import *
from collections import deque
from bfs import *
from greedy import *
from ucs import *
from dfs import *
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()   
        pygame.display.set_caption('Snather')    
        pygame.display.flip()
        self.surface = pygame.display.set_mode((WIDTH_BOARD, HEIGHT_BOARD))
        #snake
        self.snake = Snake(self.surface)
        self.snake.draw()
        #food
        self.food = Food(self.surface)
        self.food.draw()
        
        self.play_background_music()
        self.clock = pygame.time.Clock()
        
        self.algorithm= NO_ALGORITHM
        self.actions = deque([])
        self.simulations=[]
        self.simulationImg=SIMULATION_IMG.convert_alpha()
        self.simulationImg_rect = self.simulationImg.get_rect()
        #menu
        self.menu_surf = pygame.image.load(r'assets\menu\menu-bg.png').convert()
        self.menu_rect = self.menu_surf.get_rect(topleft = (0, 47.73))
        self.sub_menu_surf = pygame.image.load(r'assets\menu\sub-menu-bg.png').convert_alpha()
        self.sub_mode_rect = self.sub_menu_surf.get_rect(topleft=(0, 48))
        self.sub_algorithm_rect = self.sub_menu_surf.get_rect(topleft=(300, 48))
        self.menu_mode = True

        #borders
        self.border_horizontal_top = pygame.Surface((WIDTH_BORDER_BOARD, HEIGHT_BORDER_BOARD))
        self.border_horizontal_top.fill(BODER_COLOR)
        self.border_horizontal_bottom = self.border_horizontal_top
        self.border_vertical_left = pygame.transform.rotate ( self.border_horizontal_top, 90)
        self.border_vertical_right =  self.border_vertical_left

        #nav_bar
        self.navbar = pygame.Surface((WIDTH_BOARD,HEIGHT_NAVBAR))
        self.navbar.fill(NAVBAR_COLOR)

        #logo
        self.logo_surf = pygame.image.load(r'assets\nav-bar\logo-main.png').convert_alpha()
        self.logo_rect = self.logo_surf.get_rect(center=(60, 23.865))
        #button
        self.btn_image = r'assets\btn.png'
        self.btn_surf = pygame.image.load(self.btn_image).convert_alpha()
        self.btn_rect = self.btn_surf.get_rect(center=(525, 375))
        self.btn_list_func = ['MENU', '0', 'PLAY', 'NEW']
        self.btn_list_mode = ['Basic', 'Auto play', 'Solo machine', 'Machine vs Machine', 'Slither.io']
        self.btn_list_algorithm = ['BFS', 'Greedy', 'UCS', 'A*']
        #text_font 
        self.text_font = pygame.font.Font(r'assets\font\Inknut_Antiqua\InknutAntiqua-Bold.ttf', 18)

        #buttons
        self.btn_menu_list = []
        for i in range(len(self.btn_list_func)):
            button = btn.Button(self.surface, self.text_font, f'{self.btn_list_func[i]}', 100, 40, (200 +i*200, 5), True, WHITE, GREEN_HOVER, WHITE, GREEN_HOVER)
            self.btn_menu_list.append(button)

        #buttons_sub_menu_mode
        self.btn_sub_mode_list = []
        for i in range(len(self.btn_list_mode)):
            button = btn.Button(self.surface, self.text_font, f'{self.btn_list_mode[i]}', 280, 76, (0, 54 + 79*i), False, BLACK, BLACK_BLUE, WHITE, GREEN_HOVER)
            self.btn_sub_mode_list.append(button)
        self.mode_menu_open = False

        #buttons_sub_menu_settings:
        self.btn_sub_algorithm_list = []
        for i in range(len(self.btn_list_algorithm)):
            button = btn.Button(self.surface,self.text_font, f'{self.btn_list_algorithm[i]}', 280, 76, (300, 54 + 79*i), False, BLACK, BLACK_BLUE, WHITE, GREEN_HOVER)
            self.btn_sub_algorithm_list.append(button)
        self.setting_menu_open = False

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
        self.food = Food(self.surface)

    def is_collision(self, x1, y1, x2, y2,d=0):
        if x1 >= x2-d and x1 < x2 + CELL_SIZE+d:
            if y1 >= y2-d and y1 <y2 + CELL_SIZE+d:
                return True
        return False

    def create_ValidFood(self):
        self.food.move()
        while self.food.x in self.snake.x and self.food.y in self.snake.y:
            self.food.move()

    def render_background(self):
        self.surface.fill('black')
        bg = BACKGROUND_IMG.convert_alpha()
        self.surface.blit(bg, (0,0))

    def play_algorithm(self):
        self.draw_display()
        self.food.draw() 
        self.snake.walk()
        
        self.display_score()
        pygame.display.flip()
        # print("-----------------------------------------------------------")
        # print(self.snake.x,self.snake.y,sep='\n')
        # print("Food: ",(self.food.x,self.food.y))
        # print(self.actions)
        self.check_collision_algorithm() 
                             
    def play_basic(self):
        self.draw_display()
        self.food.draw()
        self.snake.walk()
        self.display_score()
        pygame.display.flip()
        print("-----------------------------------------------------------")
        print(self.snake.x,self.snake.y,sep='\n')
        print("Food: ",(self.food.x,self.food.y))
        self.check_collision()   
    
    def check_collision(self):
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y,CELL_SIZE*2):      
            print("eat")
            self.play_sound("ding")
            self.snake.increase_length()
            self.food.move()  
        
        if self.snake.x[0] <= CELL_SIZE or self.snake.x[0]>= WIDTH_BOARD-CELL_SIZE or self.snake.y[0] <= CELL_SIZE+HEIGHT_NAVBAR or self.snake.y[0]>= HEIGHT_BOARD-CELL_SIZE:
            self.play_sound('crash')
            raise "Collision Occurred"
        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"
    
    def GreedyAlgorithm(self):
        greedy= Greedy(Node(self.snake.x,self.snake.y,self.food.x,self.food.y))
        self.actions = deque(greedy.find_pos_greedy())
        self.simulations= greedy.moved_pos
        self.draw_Simulations()
    def BFSAlgorithm(self):
        bfs = BFS(self.snake.x,self.snake.y,self.food.x,self.food.y)
        self.actions = deque(bfs.bfs())
        self.simulations= bfs.moved_pos
        self.draw_Simulations()
    def DFSAlgorithm(self):
        dfs = DFS(self.snake.x,self.snake.y,self.food.x,self.food.y)
        self.actions = deque(dfs.dfs())
        self.simulations= dfs.moved_pos
        self.draw_Simulations()
    def UCSAlgorithm(self):
        self.actions = deque(UCS(Node(self.snake.x,self.snake.y,self.food.x,self.food.y)).ucs_snake_game())
    
    def draw_Simulations(self):
        for simu in self.simulations:
            simu_posGame = np.array(simu)*CELL_SIZE
            self.simulationImg_rect.center = tuple(simu_posGame)
            self.surface.blit(self.simulationImg, self.simulationImg_rect)
            pygame.display.flip()
    
    def check_collision_algorithm(self):
        if len(self.actions)==0:      
            print("eat")
            self.play_sound("ding")
            self.snake.increase_length()   
            self.create_ValidFood()
            self.food.draw() 
            self.choose_Algorithm()
        if self.snake.x[0] <= CELL_SIZE or self.snake.x[0]>= WIDTH_BOARD-CELL_SIZE or self.snake.y[0] <= CELL_SIZE+HEIGHT_NAVBAR or self.snake.y[0]>= HEIGHT_BOARD-CELL_SIZE:
            print("Collision with Obstacle")
            self.play_sound('crash')
            raise "Collision Occurred"
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                print("Collision with itself")
                raise "Collision Occurred"       
            
    def draw_display(self):
        self.surface.fill('black')
        self.render_background() 
        self.surface.blit(self.navbar,(0,0))
        self.drawBorderBoard()
        if self.menu_mode:
            self.surface.blit(self.logo_surf, self.logo_rect)
            for btn in self.btn_menu_list:
                btn.draw()
            if self.mode_menu_open:
                self.mode_menu_open = self.draw_sub_menu(self.btn_sub_mode_list, self.btn_sub_algorithm_list, self.mode_menu_open)
                
    def display_score(self):
        self.btn_menu_list[1].text=f"{self.snake.length-10}"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()
        
    def drawBorderBoard(self):
        self.surface.blit(self.border_horizontal_top,POS_BORDER[0])
        self.surface.blit(self.border_horizontal_bottom,POS_BORDER[1])
        self.surface.blit(self.border_vertical_left,POS_BORDER[2])
        self.surface.blit(self.border_vertical_right,POS_BORDER[3])

    def draw_sub_menu(self, menu_list, btn_sub_algorithm_list, menu_open):
        self.surface.blit(self.sub_menu_surf, self.sub_mode_rect)
        self.surface.blit(self.sub_menu_surf, self.sub_algorithm_rect)
        for btn in menu_list:
            btn.draw()
            
        for btn in btn_sub_algorithm_list:
            btn.draw()
    
    def displayMovement(self,move):
        if move == LEFT:
            if self.snake.direction==UP or self.snake.direction==DOWN:
                self.snake.move_left()

        if move == RIGHT:
            if self.snake.direction==UP or self.snake.direction==DOWN:
                self.snake.move_right()

        if move == UP:
            if self.snake.direction==LEFT or self.snake.direction==RIGHT:
                self.snake.move_up()

        if move == DOWN:
            if self.snake.direction==LEFT or self.snake.direction==RIGHT:
                self.snake.move_down()
    
    def choose_Algorithm(self):
        if self.algorithm == GREEDY_ALGORITHM:
            self.GreedyAlgorithm()
        elif self.algorithm == BFS_ALGORITHM:
            self.BFSAlgorithm()
        elif self.algorithm == UCS_ALGORITHM:
            self.UCSAlgorithm()
        elif self.algorithm == DFS_ALGORITHM:
            self.DFSAlgorithm()
    
    def run_algorithm(self):
        running = True
        pause = False
        self.choose_Algorithm()
        while running:
            if(len(self.actions)>0):        
                move = self.actions.popleft()
                self.displayMovement(move)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if self.sub_mode_rect.collidepoint(pygame.mouse.get_pos()) == False and self.sub_algorithm_rect.collidepoint(pygame.mouse.get_pos()) == False:
                        self.mode_menu_open = False      
                        pause=False  
                    for btn in self.btn_menu_list:
                        btn.pressed = False
                    for btn in self.btn_menu_list:
                        if btn.check_click():   
                            if btn.text == 'MENU':
                                pause = True
                                print('get into menu')
                                self.mode_menu_open = True
                            if btn.text == 'PLAY':
                                pause= False
                    if self.logo_rect.collidepoint(pygame.mouse.get_pos()):
                        print('collide with logo')
                        self.show_game_over()
                        pause = True
                        self.reset()
                        return
            try:
                if not pause:
                    self.play_algorithm()
                else:
                    if self.menu_mode:
                        self.surface.blit(self.logo_surf, self.logo_rect)
                        for btn in self.btn_menu_list:
                            btn.draw()
                        if self.mode_menu_open:
                            self.draw_sub_menu(self.btn_sub_mode_list, self.btn_sub_algorithm_list, self.mode_menu_open)
                    pygame.display.flip()
            except Exception as e:
                print(e)
                print("----------------------------ERROR-------------------------")
                print(self.snake.x,self.snake.y,sep='\n')
                print("Food: ",(self.food.x,self.food.y))
                self.show_game_over()
                pause = True
                self.reset()
            self.clock.tick(60)
    
    def run_basic(self):
        running = True
        pause = False
       
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
                           self.displayMovement(LEFT)

                        if event.key == K_RIGHT:
                            self.displayMovement(RIGHT)

                        if event.key == K_UP:
                            self.displayMovement(UP)

                        if event.key == K_DOWN:
                            self.displayMovement(DOWN)
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if self.sub_mode_rect.collidepoint(pygame.mouse.get_pos()) == False and self.sub_algorithm_rect.collidepoint(pygame.mouse.get_pos()) == False:
                        self.mode_menu_open = False      
                        pause=False  
                    for btn in self.btn_menu_list:
                        btn.pressed = False
                    for btn in self.btn_menu_list:
                        if btn.check_click():   
                            if btn.text == 'MENU':
                                pause = True
                                print('get into menu')
                                self.mode_menu_open = True
                            if btn.text == 'PLAY':
                                pause= False
                    if self.logo_rect.collidepoint(pygame.mouse.get_pos()):
                        print('collide with logo')
                        self.show_game_over()
                        pause = True
                        self.reset()
                        return
            try:
                if not pause:
                    self.play_basic()
                else:
                    #self.snake.draw()
                    if self.menu_mode:
                        self.surface.blit(self.logo_surf, self.logo_rect)
                        for btn in self.btn_menu_list:
                            btn.draw()
                        if self.mode_menu_open:
                            self.draw_sub_menu(self.btn_sub_mode_list, self.btn_sub_algorithm_list, self.mode_menu_open)
                    pygame.display.flip()
            except Exception as e:
                print(e)
                self.show_game_over()
                pause = True
                self.reset()
            self.clock.tick(60)

    def start(self):
        self.algorithm=BFS_ALGORITHM
        self.run_algorithm()
        #self.run_basic()