import pygame as pg
from constants import BLUE, TILE
class Wall(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pg.Surface((TILE,TILE))
        self.image.fill(BLUE)
        self.rect=self.image.get_rect(topleft=(x,y))