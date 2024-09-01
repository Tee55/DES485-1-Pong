import pygame
import random

class Item:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.spawn_time = 0
        self.spawn_interval = random.uniform(5, 8)

        self.is_active = False

    def spawn(self):
        x = random.randint(0, self.width - self.rect.width)
        y = random.randint(100, self.height - self.rect.height)
        self.rect.topleft = (x, y)
        self.is_active = True

    def render(self):
        if self.is_active:
            pygame.draw.rect(self.screen, (0, 255, 0), self.rect)