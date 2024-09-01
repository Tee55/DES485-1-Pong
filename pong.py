import pygame
import sys
import time

from Paddle import Paddle
from Ball import Ball
from Obstacle import Obstacle
from Item import Item
from constant import *

class GameMain:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.hit_sound = pygame.mixer.Sound('sounds/hit.wav')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.small_font = pygame.font.Font('fonts/font.ttf', 24)
        self.large_font = pygame.font.Font('fonts/font.ttf', 48)
        self.score_font = pygame.font.Font('fonts/font.ttf', 96)

        self.player1 = Paddle(self.screen, 30, 90, 15, 60)
        self.player2 = Paddle(self.screen, WIDTH - 30, HEIGHT - 90, 15, 60)
        self.ball = Ball(self.screen, WIDTH / 2 - 6, HEIGHT / 2 - 6, 12, 12)

        self.obstacle_1 = Obstacle(self.screen, WIDTH / 2 + 250, HEIGHT / 2, 15, 100)
        self.obstacle_2 = Obstacle(self.screen, WIDTH / 2 - 250, HEIGHT / 2, 15, 100)

        self.item = Item(self.screen, WIDTH, HEIGHT)

        self.game_state = 'start'
        self.ball_started = False

        self.AI_LEVEL = "Easy"

    def update(self, delta_time, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_state == 'start':
                        self.game_state = 'play'
                    elif self.game_state == 'play' and self.ball_started:
                        self.ball.Reset()
                        self.ball_started = False
                    elif self.game_state == 'play' and not self.ball_started:
                        self.ball_started = True

        if not self.item.is_active and time.time() - self.item.spawn_time >= self.item.spawn_interval:
            self.item.spawn()
            self.item.spawn_time = time.time()

        key = pygame.key.get_pressed()
        # Player 1 movement
        if key[pygame.K_w]:
            self.player1.dy = -PADDLE_SPEED
        elif key[pygame.K_s]:
            self.player1.dy = PADDLE_SPEED
        else:
            self.player1.dy = 0

        if self.player1.score >= 1:
            self.AI_LEVEL = "Hard"

        # Player 2 movement (Weak AI)
        if self.AI_LEVEL == "Easy":
            if abs(self.player2.rect.centerx - self.ball.rect.centerx) < 200:
                if self.player2.rect.centery < self.ball.rect.centery:
                    self.player2.dy = PADDLE_SPEED
                elif self.player2.rect.centery > self.ball.rect.centery:
                    self.player2.dy = -PADDLE_SPEED
            else:
                self.player2.dy = 0

        # Player 2 movement (Strong AI)
        if self.AI_LEVEL == "Hard":
            self.player2.rect.centery = self.ball.rect.centery

        # Check player 2 paddle boundaries
        if self.player2.rect.top < 0:
            self.player2.rect.top = 0
        if self.player2.rect.bottom > self.screen.get_height():
            self.player2.rect.bottom = self.screen.get_height()

        # Item collision
        if self.item.is_active and self.ball.rect.colliderect(self.item.rect):
            self.item.is_active = False
            self.ball.boost()

        # Ball collision top and bottom
        if self.ball.rect.top < 0 or self.ball.rect.bottom > HEIGHT:
            self.ball.dy = -self.ball.dy

        # Ball collision (Paddle)
        if self.player1.check_collision(self.ball):
            self.ball = self.player1.check_collision(self.ball)
            self.hit_sound.play()

        if self.player2.check_collision(self.ball):
            self.ball = self.player2.check_collision(self.ball)
            self.hit_sound.play()

        if self.obstacle_1.check_collision(self.ball):
            self.ball = self.obstacle_1.check_collision(self.ball)
            self.hit_sound.play()

        if self.obstacle_2.check_collision(self.ball):
            self.ball = self.obstacle_2.check_collision(self.ball)
            self.hit_sound.play()

        # Score 
        if self.ball.rect.left <= 0:
            self.player2.score += 1
            self.ball.Reset()
            self.ball_started = False

        if self.ball.rect.right >= WIDTH:
            self.player1.score += 1
            self.ball.Reset()
            self.ball_started = False

        if self.game_state == 'play' and self.ball_started:
            self.ball.update(delta_time)

        self.player1.update(delta_time)
        self.player2.update(delta_time)
        self.obstacle_1.update(delta_time)
        self.obstacle_2.update(delta_time)

    def render(self):
        if self.game_state == 'start':
            self.screen.fill((40, 45, 52))
            title_text = self.large_font.render('Welcome Pong', True, (255, 255, 255))
            start_text = self.small_font.render('Press Enter to Start', True, (255, 255, 255))
            
            # Draw text on the screen
            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
            self.screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        
        elif self.game_state == 'play':
            self.screen.fill((40, 45, 52))

            # Display score
            t_score = self.score_font.render('{:02d} - {:02d}'.format(self.player1.score, self.player2.score), False, (255, 255, 255))
            text_rect = t_score.get_rect(center=(WIDTH / 2, 60))
            self.screen.blit(t_score, text_rect)

            # Display AI Level
            text = self.small_font.render('AI level: {}'.format(self.AI_LEVEL), True, (255, 255, 255))
            # Top right
            text_rect = text.get_rect(topright=(WIDTH - 10, 10))
            self.screen.blit(text, text_rect)

            # Display dev name
            text = self.small_font.render('By: Teerapath Sattabongkot', True, (255, 255, 255))
            # Top left
            text_rect = text.get_rect(topleft=(10, 10))
            self.screen.blit(text, text_rect)

            self.ball.render()
            self.player1.render()
            self.player2.render()
            self.obstacle_1.render()
            self.obstacle_2.render()
            self.item.render()

if __name__ == '__main__':
    main = GameMain()

    clock = pygame.time.Clock()

    while True:

        pygame.display.set_caption('Pong game running with {:d} FPS'.format(int(clock.get_fps())))

        events = pygame.event.get()
        delta_time = clock.tick(MAX_FRAME_RATE) / 1000

        main.update(delta_time, events)
        main.render()

        pygame.display.update()