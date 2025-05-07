import pygame as pg
from constants import TILE, YELLOW
from .character import Character

class PacMan(Character):
    def __init__(self, pos, speed):
        super().__init__(pos, speed)
        # зберігаємо стартову позицію для респавну
        self.start_pos = pos
        # трохи зменшуємо, щоб заповнювати весь коридор без застрягання
        self.radius = TILE//2 - 1
        size = self.radius * 2
        self.image = pg.Surface((size, size), pg.SRCALPHA)
        self.rect  = self.image.get_rect(center=pos)
        self.dir   = pg.Vector2(0, 0)

    def handle_input(self):
        keys = pg.key.get_pressed()
        self.dir.x = keys[pg.K_RIGHT] - keys[pg.K_LEFT]
        self.dir.y = keys[pg.K_DOWN]  - keys[pg.K_UP]

    def update(self, dt, walls):
        self.handle_input()
        super().update(dt, walls)
        # центруємо по сітці, щоб не з’їжджав з коридорів
        if self.dir.x != 0:
            row = self.rect.centery // TILE
            self.rect.centery = row * TILE + TILE//2
        elif self.dir.y != 0:
            col = self.rect.centerx // TILE
            self.rect.centerx = col * TILE + TILE//2

    def respawn(self):
        """Повернути Пакмена в стартову точку."""
        self.rect.center = self.start_pos
        self.dir = pg.Vector2(0, 0)

    def draw(self, surf):
        pg.draw.circle(surf, YELLOW, self.rect.center, self.radius)
