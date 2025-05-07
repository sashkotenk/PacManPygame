import pygame as pg
from constants import ORANGE, RED

class Menu:
    def __init__(self, screen, font=None):
        self.screen = screen
        self.font = font or pg.font.Font(None, 48)
        self.options = []
        self.selected = 0

    def draw(self):
        w, h = self.screen.get_size()
        # початкова вертикальна позиція трохи нижче логотипу
        start_y = h // 2 - (len(self.options) * 40) // 2
        for i, opt in enumerate(self.options):
            # усі пункти помаранчеві; вибраний — червоний
            color = RED if i == self.selected else ORANGE
            text = self.font.render(opt, True, color)
            rect = text.get_rect(center=(w//2, start_y + i * 60))
            self.screen.blit(text, rect)

    def handle_event(self, e):
        if e.type == pg.KEYDOWN:
            if e.key in (pg.K_UP, pg.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif e.key in (pg.K_DOWN, pg.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif e.key == pg.K_RETURN:
                return self.options[self.selected]
        return None
