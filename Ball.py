import pygame
import random
from constant import *
import time

class Ball:
    def __init__(self, screen, x, y, width, height) -> None:
        self.screen = screen

        self.rect = pygame.Rect(x, y, width, height)

        self.normal_speed = 300
        self.boost_speed = 500
        self.dx = self.normal_speed * random.choice([-1, 1])
        self.dy = self.normal_speed * random.uniform(-1, 1)

        self.is_boosted = False
        self.boost_starttime = 0

    def Reset(self):
        self.rect.x = WIDTH / 2 - 6
        self.rect.y = HEIGHT / 2 -6

        self.dx = self.normal_speed * random.choice([-1, 1])
        self.dy = self.normal_speed * random.uniform(-1, 1)

    def update(self, delta_time):
        if self.is_boosted and time.time() - self.boost_starttime >= 3:
            current_speed = (self.dx**2 + self.dy**2) ** 0.5
            direction_x = self.dx / current_speed
            direction_y = self.dy / current_speed

            self.dx = direction_x * self.normal_speed
            self.dy = direction_y * self.normal_speed

            self.is_boosted = False

        self.rect.x += self.dx * delta_time
        self.rect.y += self.dy * delta_time

    def boost(self):
        current_speed = (self.dx**2 + self.dy**2) ** 0.5

        direction_x = self.dx / current_speed
        direction_y = self.dy / current_speed

        self.dx = direction_x * self.boost_speed
        self.dy = direction_y * self.boost_speed

        self.is_boosted = True
        self.boost_starttime = time.time()  

    def render(self):
        if self.is_boosted:
            pygame.draw.rect(self.screen, (255, 0, 0), self.rect)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect)