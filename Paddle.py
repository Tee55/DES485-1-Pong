import pygame
from constant import *

class Paddle:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.dy = 0
        self.score = 0

    def update(self, delta_time):
        if self.dy > 0:
            if self.rect.y + self.rect.height < HEIGHT:
                self.rect.y += self.dy * delta_time
        else:
            if self.rect.y > 0:
                self.rect.y += self.dy * delta_time

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
        pygame.draw.rect(self.screen, (255, 255, 0), self.rect)