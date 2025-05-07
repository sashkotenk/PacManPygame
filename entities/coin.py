import pygame as pg
from constants import WHITE
class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos=(x,y)
        self.radius=4
    def draw(self,surf):
        pg.draw.circle(surf, WHITE, self.pos, self.radius)
class PowerPellet(Coin):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.radius=8