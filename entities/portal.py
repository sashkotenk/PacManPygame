import pygame as pg
class Portal(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.rect=pg.Rect(x,y,24,24)