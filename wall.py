import pygame

class Wall:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
