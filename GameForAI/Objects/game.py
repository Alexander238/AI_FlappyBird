import pygame
import random
import sys
import os 
env_Path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(env_Path)

import environment_variables as env
from Objects.bird import Bird
from pipe import Pipe


class Game:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.reset_game()

    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_over = False
        self.spawn_pipe()

    def spawn_pipe(self):
        upper_pipe_length = random.randint(100, env.SCREEN_HEIGHT // 2)
        lower_pipe_length = env.SCREEN_HEIGHT - upper_pipe_length - env.PIPE_GAP
        self.pipes.append(Pipe(env.SCREEN_WIDTH, upper_pipe_length, True))
        self.pipes.append(Pipe(env.SCREEN_WIDTH, lower_pipe_length, False))

    def update(self):
        if self.game_over:
            return

        self.bird.update()

        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > env.PIPE_SPAWN_INTERVAL:
            self.spawn_pipe()
            self.last_spawn_time = current_time

        for pipe in self.pipes:
            pipe.update()

        self.pipes = [pipe for pipe in self.pipes if pipe.x + env.PIPE_BODY_IMAGE.get_width() > 0]

        self.check_collisions()
        self.checkIfPipePassed()

    def checkIfPipePassed(self):
        for pipe in self.pipes:
            PIPE_X_POS = pipe.x + (env.PIPE_BODY_IMAGE.get_width() // 2)
            if PIPE_X_POS < self.bird.x and not pipe.is_upside_down and not pipe.passed:
                self.score += 1
                pipe.passed = True

    def check_collisions(self):
        for pipe in self.pipes:
            if pipe.is_upside_down:
                if self.bird.y < pipe.length and self.bird.x + self.bird.width > pipe.x and self.bird.x < pipe.x + env.PIPE_BODY_IMAGE.get_width():
                    self.game_over = True
            else:
                if self.bird.y + self.bird.height > env.SCREEN_HEIGHT - pipe.length and self.bird.x + self.bird.width > pipe.x and self.bird.x < pipe.x + env.PIPE_BODY_IMAGE.get_width():
                    self.game_over = True
        
        # check if bird is out of screen
        if self.bird.y <= 0 or self.bird.y + self.bird.height >= env.SCREEN_HEIGHT:
            self.game_over = True

    def render(self):
        self.screen.fill((0, 0, 0))
        self.bird.render(self.screen)

        for pipe in self.pipes:
            pipe.render(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            self.render_death_screen()

    def render_death_screen(self):
        death_screen_overlay = pygame.Surface((env.SCREEN_WIDTH, env.SCREEN_HEIGHT))
        death_screen_overlay.set_alpha(128)
        death_screen_overlay.fill((128, 128, 128))
        self.screen.blit(death_screen_overlay, (0, 0))

        game_over_text = self.font.render('Game Over', True, (255, 0, 0))
        self.screen.blit(game_over_text, (env.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, env.SCREEN_HEIGHT // 4))

        score_text = self.font.render(f'Your Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (env.SCREEN_WIDTH // 2 - score_text.get_width() // 2, env.SCREEN_HEIGHT // 2))

        play_again_text = self.font.render('Press ENTER to play again', True, (255, 255, 255))
        self.screen.blit(play_again_text, (env.SCREEN_WIDTH // 2 - play_again_text.get_width() // 2,env.SCREEN_HEIGHT // 2 + score_text.get_height() + 20))

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((env.SCREEN_WIDTH, env.SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    game = Game(screen, font)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.bird.flap()
                if event.key == pygame.K_RETURN and game.game_over:
                    game.reset_game()

        print(game.pipes.__len__())
        game.update()
        game.render()
        pygame.display.flip()
        clock.tick(env.FPS)