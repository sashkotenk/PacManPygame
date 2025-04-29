import pygame

# Клас монети, яку можна зібрати
class Coin:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)  # Позиція монети
        self.radius = 5                       # Радіус кола монети
        self.collected = False                # Чи зібрана монета

    def draw(self, screen):
        # Малюємо монету, якщо вона ще не зібрана
        if not self.collected:
            pygame.draw.circle(screen, (255, 255, 0), (int(self.position.x), int(self.position.y)), self.radius)
