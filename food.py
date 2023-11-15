from static import *
import random
class Food:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = FOOD_IMG[0].convert_alpha()
        self.rect = self.image.get_rect()
        self.x = CELL_SIZE*50
        self.y = CELL_SIZE*50        

    def draw(self):
        self.rect.center = (self.x, self.y)
        self.parent_screen.blit(self.image, self.rect)
        pygame.display.flip()

    def move(self):
        self.x = random.randint(2,(WIDTH_BOARD-CELL_SIZE*2)//CELL_SIZE)*CELL_SIZE
        self.y = random.randint(HEIGHT_NAVBAR//CELL_SIZE,(HEIGHT_BOARD-CELL_SIZE)//CELL_SIZE)*CELL_SIZE