import pygame

class Coin:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.radius = 5
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, (255, 255, 0), (int(self.position.x), int(self.position.y)), self.radius)
