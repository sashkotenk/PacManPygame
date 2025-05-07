import pygame as pg
from pygame.math import Vector2
from constants import TILE, RED, PINK, CYAN, ORANGE, BLUE
from .character import Character

class Ghost(Character):
    """
    Привид із тайловим рухом:
    - завжди працює в grid-режимі (мінімізує/максимізує мангеттенську відстань)
    - tie-break між рівними напрямками задається ротацією залежно від idx
    """
    COLORS = [RED, PINK, CYAN, ORANGE]
    DIRECTIONS = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]

    def __init__(self, pos, idx, speed, walls):
        super().__init__(pos, speed)
        self.start_pos = Vector2(pos)
        self.color = self.COLORS[idx % len(self.COLORS)]
        self.frightened_timer = 0.0
        # **Вимкнули реліз-режим** — одразу grid-логіка
        self.released = True
        # Заблоковані клітини (стіни)
        self.blocked = {
            (w.rect.centerx // TILE, w.rect.centery // TILE)
            for w in walls
        }
        # Ротація order of DIRECTIONS для кожного idx (щоб tie-break розходився)
        rot = idx % len(self.DIRECTIONS)
        self.dirs = self.DIRECTIONS[rot:] + self.DIRECTIONS[:rot]
        self.dir = Vector2(0, 0)

    def set_frightened(self, duration: float):
        """Увімкнути frightened режим на кількість секунд."""
        self.frightened_timer = duration

    def respawn(self):
        """Повернутися на стартову позицію і скинути режими."""
        self.rect.center = self.start_pos
        self.frightened_timer = 0.0
        self.dir = Vector2(0, 0)

    def update(self, dt, walls, player):
        # Оновлюємо таймер frightened
        if self.frightened_timer > 0:
            self.frightened_timer = max(0.0, self.frightened_timer - dt)

        # Якщо ми в центрі тайла — обираємо новий напрямок
        if self._at_tile_center():
            gx = self.rect.centerx // TILE
            gy = self.rect.centery  // TILE
            px = player.rect.centerx // TILE
            py = player.rect.centery  // TILE

            best = None
            for d in self.dirs:
                # не розвертатися назад
                if d == -self.dir:
                    continue
                nx, ny = gx + int(d.x), gy + int(d.y)
                if (nx, ny) in self.blocked:
                    continue
                dist = abs(nx - px) + abs(ny - py)
                # frightened = біжимо геть → хочемо великий dist
                # chase = переслідуємо → хочемо малий dist
                score = dist if self.frightened_timer > 0 else -dist
                if best is None or score > best[0]:
                    best = (score, d)
            if best:
                self.dir = best[1]

        # Рухаємось і перевіряємо колізії зі стінами
        self._move(dt, walls)

    def _move(self, dt, walls):
        if self.dir.length_squared():
            move = self.dir.normalize() * self.speed * dt
            self.rect.x += move.x
            self._collide(walls, axis='x')
            self.rect.y += move.y
            self._collide(walls, axis='y')

    def _at_tile_center(self) -> bool:
        cx, cy = self.rect.centerx, self.rect.centery
        return ((cx - TILE//2) % TILE == 0) and ((cy - TILE//2) % TILE == 0)

    def _collide(self, walls, axis):
        hits = [w for w in walls if self.rect.colliderect(w.rect)]
        for w in hits:
            if axis == 'x':
                if self.dir.x > 0:
                    self.rect.right = w.rect.left
                elif self.dir.x < 0:
                    self.rect.left  = w.rect.right
            else:
                if self.dir.y > 0:
                    self.rect.bottom = w.rect.top
                elif self.dir.y < 0:
                    self.rect.top    = w.rect.bottom

    def draw(self, surf):
        col = BLUE if self.frightened_timer > 0 else self.color
        pg.draw.rect(surf, col, self.rect)
