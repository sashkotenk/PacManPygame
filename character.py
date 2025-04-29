import pygame

class Character:
    def __init__(self, x=0, y=0, speed=2.5):
        self.position = pygame.Vector2(x, y)
        self.speed = speed
        self.direction = pygame.Vector2(0, 0)

    def move(self):
        self.position += self.direction * self.speed

    def update(self):
        self.move()

    def draw(self, screen, color=(255, 255, 0)):
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), 10)
