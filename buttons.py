
import pygame as pg
import color as col

class Button():
    def __init__(self, screen, text_font, text, width, height, pos, border_true, color_bg, color_hover_bg, def_color_text, color_hover_text):
        self.border_state = border_true
        self.pressed = False
        self.screen = screen
        self.text_font = text_font
        #top rect
        self.top_rect = pg.Rect(pos, (width, height))
        self.color_bg = color_bg
        self.color_hover_bg = color_hover_bg
        self.top_color = self.color_bg
        #text
        self.text = text
        self.def_color_text = def_color_text
        self.color_text = self.def_color_text
        self.color_hover_text = color_hover_text
        self.text_surf = text_font.render(self.text, True, col.WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
    def draw(self):
        self.text_surf = self.text_font.render(self.text, True, self.color_text)
        if self.border_state:
            pg.draw.rect(self.screen, self.top_color, self.top_rect, width=1)
        else:
            pg.draw.rect(self.screen, self.top_color, self.top_rect)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.color_hover_bg
            self.color_text = self.color_hover_text
            if pg.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    print(f'Click {self.text}')
                    self.pressed = False
        else:
            self.top_color = self.color_bg
            self.color_text = self.def_color_text
        return self.pressed


