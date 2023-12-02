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
from a_star import *
from hill_climbing import *
from ids import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()   
        pygame.display.set_caption('Snather')    
        #pygame.display.flip()
        self.surface = pygame.display.set_mode((WIDTH_BOARD, HEIGHT_BOARD))
        self.skin_Snake=SKIN_2
        self.init_NewStateGame()
        
        self.mode=BASIC_MODE
        self.algorithm= BFS_ALGORITHM
        self.obstacles=set()
        self.paths_pos=[]
        self.play_background_music()
        self.clock = pygame.time.Clock()
        
        self.simulationImg=SIMULATION_IMG.convert_alpha()
        self.simulationImg_rect = self.simulationImg.get_rect()
        
        self.pathImg=PATH_IMG.convert_alpha()
        self.pathImg_rect = self.pathImg.get_rect()
        
        self.obstacleImg=OBSTACLE_IMG.convert_alpha()
        self.obstacleImg_rect = self.simulationImg.get_rect()
        
        self.run_time = 0
        
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
        self.btn_list_func = ['MENU', '0','0ms','0','0', 'PLAY', 'NEW']
        self.btn_list_mode = ['Basic','Algorithm', 'Skin', 'Map','Draw-Map', 'Simulations']
        self.btn_list_otps = []
        self.btn_list_otps = []
        #text_font 
        self.text_font = pygame.font.Font(r'assets\font\Inknut_Antiqua\InknutAntiqua-Bold.ttf', 18)
        self.init_menu()
        
        self.mode_is_click=False
        self.otp_is_click = False
        self.choose_algorithm=False
        self.choose_skin=False
        self.choose_map=False
        self.is_Draw_Map_Mode = False
        self.is_Simulations_Mode = False

        #data
        self.actions_total = []
        self.moved_pos_total = []
        self.actions_total_count=0
        self.moved_pos_total_count=0

    def init_NewStateGame(self):
        #snake
        self.snake = Snake(self.surface)
        self.snake.changeSkin(self.skin_Snake)
        self.snake.draw()
        #food
        self.food = Food(self.surface)
        self.food.draw()
        
        self.simulations=[]
        self.actions = deque([])
        
        self.choose_algorithm=False
        self.choose_skin=False
        self.choose_map=False
        self.otp_is_click=False
    def init_menu(self):
         #buttons
        self.btn_menu_list = []
        for i in range(len(self.btn_list_func)):
            button = btn.Button(self.surface, self.text_font, f'{self.btn_list_func[i]}', 140, 40, (150 +i*150, 5), True, WHITE, GREEN_HOVER, WHITE, GREEN_HOVER)
            self.btn_menu_list.append(button)

        #buttons_sub_menu_mode
        self.btn_sub_mode_list = []
        for i in range(len(self.btn_list_mode)):
            button = btn.Button(self.surface, self.text_font, f'{self.btn_list_mode[i]}', 280, 76, (0, 54 + 79*i), False, BLACK, BLACK_BLUE, WHITE, GREEN_HOVER)
            self.btn_sub_mode_list.append(button)
        self.mode_menu_open = False

        #buttons_sub_menu_settings:
        self.btn_sub_opts_list = []
        for i in range(len(self.btn_list_otps)):
            button = btn.Button(self.surface,self.text_font, f'{self.btn_list_otps[i]}', 280, 76, (300, 54 + 79*i), False, BLACK, BLACK_BLUE, WHITE, GREEN_HOVER)
            self.btn_sub_opts_list.append(button)
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
        pos_not_valid= set(zip(self.snake.x , self.snake.y)).union(self.obstacles)
        while (self.food.x,self.food.y) in pos_not_valid:
            self.food.move()

    def render_background(self):
        bg = BACKGROUND_IMG.convert_alpha()
        self.surface.blit(bg, (0,0))

    def play_algorithm(self):

        self.draw_display()
        self.food.draw()
        self.snake.walk()
        self.display_score()
        self.display_score()
        
        self.display_score()        
        
        self.check_collision_algorithm() 
        if len(self.actions)==0:
            self.choose_Algorithm()
        
        self.display_runtime()
        self.display_count_path()
        self.display_count_visited()
        pygame.display.flip()
                        
    def play_basic(self):
        self.draw_display()
        self.food.draw()
        self.draw_obstacles()
        self.snake.walk()
        self.display_score()
        pygame.display.flip()
        self.check_collision()   
    
    def check_collision(self):
        
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y,0):     
            self.snake.increase_length()
            self.food.move()  
        
        if self.snake.x[0] <= CELL_SIZE or self.snake.x[0]>= WIDTH_BOARD-CELL_SIZE or self.snake.y[0] <= CELL_SIZE+HEIGHT_NAVBAR or self.snake.y[0]>= HEIGHT_BOARD-CELL_SIZE or (self.snake.x[0],self.snake.y[0]) in self.obstacles:
            self.play_sound('crash')
            raise "Collision Occurred"
        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"
    
    def GreedyAlgorithm(self):
        greedy= GREEDY(self.snake.x,self.snake.y,self.food.x,self.food.y,self.obstacles)
        self.actions = deque(greedy.greedy())
        self.run_time=greedy.run_time
        self.simulations=greedy.moved_pos
        self.paths_pos=path_to_pos(self.snake.x[0],self.snake.y[0],np.array(self.actions))
        self.draw_Simulations_vip()
           
    def BFSAlgorithm(self):
        bfs = BFS(self.snake.x,self.snake.y,self.food.x,self.food.y,self.obstacles)
        self.actions = deque(bfs.bfs())
        self.run_time=bfs.run_time
        self.simulations= bfs.moved_pos
        self.paths_pos=path_to_pos(self.snake.x[0],self.snake.y[0],np.array(self.actions))
        self.draw_Simulations_vip()
    
    def DFSAlgorithm(self):
        dfs = DFS(self.snake.x,self.snake.y,self.food.x,self.food.y,self.obstacles)
        self.actions = deque(dfs.dfs())
        self.run_time=dfs.run_time
        self.simulations= dfs.moved_pos
        del dfs
        self.paths_pos=path_to_pos(self.snake.x[0],self.snake.y[0],np.array(self.actions))
        self.draw_Simulations_vip()

    def IDSAlgorithm(self):
        ids = IDS(self.snake.x,self.snake.y,self.food.x,self.food.y,self.obstacles)
        self.actions = deque(ids.ids())
        self.run_time=ids.run_time
        self.simulations= ids.moved_pos
        del ids
        self.paths_pos=path_to_pos(self.snake.x[0],self.snake.y[0],np.array(self.actions))
        self.draw_Simulations_vip()
    
    def UCSAlgorithm(self):
        ucs=UCS(self.snake.x,self.snake.y,self.food.x,self.food.y,self.obstacles)
        self.actions = deque(ucs.ucs())
        self.run_time=ucs.run_time
        self.simulations= ucs.moved_pos
        self.paths_pos=path_to_pos(self.snake.x[0],self.snake.y[0],np.array(self.actions))
        self.draw_Simulations_vip()
        
    def AStarAlgorithm(self):
        astar=ASTAR(self.snake.x,self.snake.y,self.food.x,self.food.y,self.obstacles)
        self.actions = deque(astar.a_star())
        self.run_time=astar.run_time
        self.simulations= astar.moved_pos
        self.paths_pos=path_to_pos(self.snake.x[0],self.snake.y[0],np.array(self.actions))
        self.draw_Simulations_vip()

    def HillClimbingAlgorithm(self):
        hill=HillClimbing(self.snake.x,self.snake.y,self.food.x,self.food.y,self.obstacles)
        self.actions = deque(hill.hill_climbing())
        self.run_time=hill.run_time
        self.simulations= hill.moved_pos
        self.paths_pos=path_to_pos(self.snake.x[0],self.snake.y[0],np.array(self.actions))
        self.draw_Simulations_vip()
    
    def draw_Simulations(self):
        if self.is_Simulations_Mode==False:
            return
        for simu in self.simulations:
            pos = tuple(posMatrix_to_posGame_list(simu))
            if pos in self.paths_pos:
                self.pathImg_rect.center = tuple(pos)
                pathimg = PATH_IMG.convert_alpha()
                self.surface.blit(pathimg, self.pathImg_rect)
            else:
                pos = tuple(posMatrix_to_posGame_list(simu))
                self.simulationImg_rect.center = tuple(pos)
                simuimg = SIMULATION_IMG.convert_alpha()
                self.surface.blit(simuimg, self.simulationImg_rect)
    
    def draw_Simulations_vip(self):
        if self.is_Simulations_Mode==False:
            return
        for simu in self.simulations:
            pos = tuple(posMatrix_to_posGame_list(simu))
            self.simulationImg_rect.center = tuple(pos)
            simuimg = SIMULATION_IMG.convert_alpha()
            self.surface.blit(simuimg, self.simulationImg_rect)
            pygame.display.update()
        for pos in self.paths_pos:
            self.pathImg_rect.center = tuple(pos)
            pathimg = PATH_IMG.convert_alpha()
            self.surface.blit(pathimg, self.pathImg_rect)
            pygame.display.update()

    def check_collision_algorithm(self):
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y,0):      
            self.play_sound("ding")
            self.snake.increase_length()   
            self.create_ValidFood()
            self.food.draw() 
        
        if self.snake.x[0] < CELL_SIZE or self.snake.x[0]> WIDTH_BOARD-CELL_SIZE or self.snake.y[0] < CELL_SIZE+HEIGHT_NAVBAR or self.snake.y[0]> HEIGHT_BOARD-CELL_SIZE or (self.snake.x[0], self.snake.y[0]) in self.obstacles:
            self.play_sound('crash')
            raise "Collision Occurred"
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"       
            
    def draw_display(self):
        self.render_background() 
        self.surface.blit(self.navbar,(0,0))
        self.drawBorderBoard()
        if len(self.actions):
            self.draw_Simulations()
        self.draw_obstacles()  
        if self.menu_mode:
            self.surface.blit(self.logo_surf, self.logo_rect)
            for btn in self.btn_menu_list:
                btn.draw()
            if self.mode_menu_open:
                self.mode_menu_open = self.draw_sub_menu(self.btn_sub_mode_list, self.btn_sub_opts_list, self.mode_menu_open)
                
    def display_score(self):
        self.btn_menu_list[1].text=f"{self.snake.length-10}"
        
    def display_runtime(self):
        self.btn_menu_list[2].text=f"{int(self.run_time)}ms"
        
    def display_count_visited(self):
        self.btn_menu_list[3].text=f"{len(self.simulations)}"
        
    def display_count_path(self):
        self.btn_menu_list[4].text=f"{len(self.paths_pos)}"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length-10}", True, (255, 255, 255))
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

    def draw_sub_menu(self, menu_list, btn_sub_opts_list, menu_open):
        self.surface.blit(self.sub_menu_surf, self.sub_mode_rect)
        self.surface.blit(self.sub_menu_surf, self.sub_algorithm_rect)
        for btn in menu_list:
            btn.draw()
            
        for btn in btn_sub_opts_list:
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
        elif self.algorithm==IDS_ALGORITHM:
            self.IDSAlgorithm()
        elif self.algorithm == UCS_ALGORITHM:
            self.UCSAlgorithm()
        elif self.algorithm == DFS_ALGORITHM:
            self.DFSAlgorithm()
        elif self.algorithm==ASTAR_ALGORITHM:
            self.AStarAlgorithm()
        elif self.algorithm==HILL_CLIMBING_ALGORITHM:
            self.HillClimbingAlgorithm()
    
    def get_obstacles(self):
        running=True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running= False
            self.draw_display()    
            self.handle_mouse_events()  
            self.draw_obstacles()  
            pygame.display.flip() 
            self.clock.tick(FPS)
        
    def handle_mouse_events(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            self.obstacles.add((mouse_x// CELL_SIZE * CELL_SIZE, mouse_y// CELL_SIZE * CELL_SIZE))
        if pygame.mouse.get_pressed()[2]:
            self.obstacles.discard((mouse_x// CELL_SIZE * CELL_SIZE, mouse_y// CELL_SIZE * CELL_SIZE))
    
    def draw_obstacles(self):
        if len(self.obstacles)==0:
            return
        for obstacle in self.obstacles:
            self.obstacleImg_rect.center = obstacle
            self.surface.blit(self.obstacleImg, self.obstacleImg_rect)
    
    def run_algorithm(self):
        running = True
        pause = False
        pygame.display.flip()
        
        if self.is_Draw_Map_Mode:
            self.get_obstacles()
            self.is_Draw_Map_Mode=False
        # start_time= time.time()
        self.choose_Algorithm()
        while running:
            if self.actions==None:
                running=False
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
                                self.mode_menu_open = True
                                self.btn_sub_opts_list.clear()
                                self.choose_algorithm=False
                                self.choose_skin=False
                                self.is_Draw_Map_Mode=False
                            if btn.text == 'PLAY':
                                pause= False
                            break
                        
                    if self.mode_menu_open==True:
                        for btn in self.btn_sub_mode_list:
                            btn.pressed = False
                        for btn in self.btn_sub_mode_list:
                            if btn.check_click():   
                                if btn.text == 'Basic':
                                    self.mode=BASIC_MODE
                                    self.mode_menu_open = False
                                    self.otp_is_click=True
                                    pause= True 
                                if btn.text == 'Algorithm':
                                    self.mode=ALGORITHM_MODE
                                    self.btn_list_otps=list(ALGORITHMS.keys())
                                    self.choose_algorithm=True
                                elif btn.text =='Skin':
                                    self.btn_list_otps=list(SKINS.keys())
                                    self.choose_skin=True
                                elif btn.text =='Map':
                                    self.btn_list_otps=list(MAPS.keys())
                                    self.choose_map=True  
                                elif btn.text=='Draw-Map':       
                                    self.is_Draw_Map_Mode=True
                                    self.otp_is_click=True
                                    self.mode_menu_open = False
                                    pause= True 
                                elif btn.text=='Simulations':
                                    if self.is_Simulations_Mode:
                                        self.is_Simulations_Mode=False
                                    else:
                                        self.is_Simulations_Mode=True
                                    self.otp_is_click=True
                                    self.mode_menu_open = False
                                    pause= True 
                                self.init_menu()
                                self.draw_sub_menu(self.btn_sub_mode_list, self.btn_sub_opts_list, self.mode_menu_open)
                                self.mode_is_click=True
                                
                    if self.mode_is_click:
                        for btn in self.btn_sub_opts_list:
                            btn.pressed = False
                        for btn in self.btn_sub_opts_list:
                            if btn.check_click():   
                                if self.choose_algorithm:
                                    self.algorithm=ALGORITHMS[btn.text]
                                elif self.choose_skin:
                                    self.skin_Snake=SKINS[btn.text]                      
                                elif self.choose_map:
                                    self.obstacles=MAPS[btn.text] 
                                    self.create_ValidFood()
                                self.otp_is_click=True
                                self.mode_menu_open = False
                                # pause= True 
                                break       
                    if self.logo_rect.collidepoint(pygame.mouse.get_pos()):
                        self.show_game_over()
                        pause = True
                        self.reset()
                        self.mode_menu_open = True
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
                            self.draw_sub_menu(self.btn_sub_mode_list, self.btn_sub_opts_list, self.mode_menu_open)
                        elif self.otp_is_click:
                            self.init_NewStateGame()
                            self.btn_sub_opts_list=[]
                            self.init_menu()
                            return
                    pygame.display.flip()
            except Exception as e:
                print(e)
                print(self.run_time)
                self.show_game_over()
                pause = True
                self.reset()

            self.clock.tick(FPS)
    
    def run_basic(self):
        running = True
        pause = False
        pygame.display.flip()
        
        if self.is_Draw_Map_Mode:
            self.get_obstacles()
            self.is_Draw_Map_Mode=False
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
                        self.choose_algorithm=False
                        self.choose_skin=False
                        self.is_Draw_Map_Mode=False
                        self.otp_is_click=False
                        self.mode_menu_open = False      
                        pause=False  
                    for btn in self.btn_menu_list:
                        btn.pressed = False
                    for btn in self.btn_menu_list:
                        if btn.check_click():   
                            if btn.text == 'MENU':
                                pause = True
                                self.mode_menu_open = True
                                self.btn_sub_opts_list.clear()
                            if btn.text == 'PLAY':
                                pause= False
                            break
                    if self.mode_menu_open==True:
                        for btn in self.btn_sub_mode_list:
                            btn.pressed = False
                        for btn in self.btn_sub_mode_list:
                            if btn.check_click():   
                                if btn.text == 'Basic':
                                    self.mode=BASIC_MODE
                                    self.mode_menu_open = False
                                elif btn.text == 'Algorithm':
                                    self.mode=ALGORITHM_MODE
                                    self.btn_list_otps=list(ALGORITHMS.keys())
                                    self.choose_algorithm=True
                                elif btn.text =='Skin':
                                    self.btn_list_otps=list(SKINS.keys())
                                    self.choose_skin=True
                                elif btn.text =='Map':
                                    self.btn_list_otps=list(MAPS.keys())
                                    self.choose_map=True  
                                elif btn.text=='Draw-Map':
                                    if self.is_Draw_Map_Mode:
                                        self.is_Draw_Map_Mode=False
                                    else:
                                        self.is_Draw_Map_Mode=True
                                    self.otp_is_click=True
                                    self.mode_menu_open = False
                                    pause= True 
                                elif btn.text=='Simulations':
                                    if self.is_Simulations_Mode:
                                        self.is_Simulations_Mode=False
                                    else:
                                        self.is_Simulations_Mode=True
                                    self.otp_is_click=True
                                    self.mode_menu_open = False
                                    pause= True 
                                self.init_menu()
                                self.draw_sub_menu(self.btn_sub_mode_list, self.btn_sub_opts_list, self.mode_menu_open)
                                pygame.display.flip()
                                self.mode_is_click=True
                                
                    if self.mode_is_click:
                        for btn in self.btn_sub_opts_list:
                            btn.pressed = False
                        for btn in self.btn_sub_opts_list:
                            if btn.check_click():   
                                if self.choose_algorithm:
                                    self.algorithm=ALGORITHMS[btn.text]
                                elif self.choose_skin:
                                    self.skin_Snake=SKINS[btn.text]                      
                                elif self.choose_map:
                                    self.obstacles=MAPS[btn.text] 
                                    self.create_ValidFood()
                                self.otp_is_click=True
                                self.mode_menu_open = False
                                pause= True 
                                break             
                    if self.logo_rect.collidepoint(pygame.mouse.get_pos()):
                        self.show_game_over()
                        pause = True
                        self.reset()
                        self.mode_menu_open = True
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
                            self.draw_sub_menu(self.btn_sub_mode_list, self.btn_sub_opts_list, self.mode_menu_open)
                        elif self.otp_is_click:
                            self.init_NewStateGame()
                            self.btn_sub_opts_list=[]
                            self.init_menu()
                            return
                    pygame.display.flip()
            except Exception as e:
                print(e)
                self.show_game_over()
                pause = True
                self.reset()
            self.clock.tick(FPS//2)

    def start(self):
        while True:
            if(self.mode==ALGORITHM_MODE):
                self.run_algorithm()
            else:
                self.run_basic()
