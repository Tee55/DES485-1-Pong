import pygame
from constant import *
import random

class Obstacle:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)

        self.velocity_y = random.choice([-1, 1]) * 200

    def update(self, delta_time):
        self.rect.y += self.velocity_y * delta_time

        # Check for collision with screen boundaries and reverse direction
        if self.rect.top <= 0 or self.rect.bottom >= self.screen.get_height():
            self.velocity_y *= -1

    def check_collision(self, ball):
        if ball.rect.colliderect(self.rect):
            if abs(ball.rect.right - self.rect.left) < abs(ball.rect.left - self.rect.right) and ball.rect.centery > self.rect.top and ball.rect.centery < self.rect.bottom:
                ball.dx = -abs(ball.dx)
            elif abs(ball.rect.left - self.rect.right) < abs(ball.rect.right - self.rect.left) and ball.rect.centery > self.rect.top and ball.rect.centery < self.rect.bottom:
                ball.dx = abs(ball.dx)
            elif abs(ball.rect.bottom - self.rect.top) < abs(ball.rect.top - self.rect.bottom) and \
                ball.rect.centerx > self.rect.left and ball.rect.centerx < self.rect.right:
                ball.dy = -abs(ball.dy)
            elif abs(ball.rect.top - self.rect.bottom) < abs(ball.rect.bottom - self.rect.top) and \
                ball.rect.centerx > self.rect.left and ball.rect.centerx < self.rect.right:
                ball.dy = abs(ball.dy)

            return ball

        return None

    def render(self):
        pygame.draw.rect(self.screen, (255, 0, 255), self.rect)