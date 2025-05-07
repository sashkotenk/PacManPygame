import pygame as pg
from math import copysign
from constants import TILE

class Character(pg.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.image = pg.Surface((TILE, TILE), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.dir = pg.Vector2(0,0)
        self.speed = speed
    def update(self, dt, walls):
        if self.dir.length_squared():
            move = self.dir.normalize()*self.speed*dt
            self.rect.x += move.x; self._collide(walls, axis="x")
            self.rect.y += move.y; self._collide(walls, axis="y")
    def _collide(self, walls, axis):
        hits = [w for w in walls if self.rect.colliderect(w.rect)]
        for w in hits:
            if axis=="x":
                if self.dir.x>0: self.rect.right = w.rect.left
                elif self.dir.x<0: self.rect.left = w.rect.right
            else:
                if self.dir.y>0: self.rect.bottom = w.rect.top
                elif self.dir.y<0: self.rect.top = w.rect.bottom