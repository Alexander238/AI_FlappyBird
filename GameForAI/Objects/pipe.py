import environment_variables as env
import pygame

class Pipe:
    def __init__(self, x, length, is_upside_down):
        self.x = x
        self.length = length + env.PIPE_HEAD_IMAGE.get_height()
        self.is_upside_down = is_upside_down
        self.passed = False

    def update(self):
        self.x -= env.PIPE_SPEED

    def render(self, screen):
        if self.is_upside_down:
            y_offset = 0
            while y_offset < self.length - env.PIPE_HEAD_IMAGE.get_height():
                screen.blit(env.PIPE_BODY_IMAGE, (self.x, y_offset))
                y_offset += env.PIPE_BODY_IMAGE.get_height()
            screen.blit(env.PIPE_HEAD_IMAGE, (self.x, self.length - env.PIPE_HEAD_IMAGE.get_height()))

            if env.SHOW_HITBOXES:
                # Show hitbox of top pipe
                pygame.draw.rect(screen, (255, 0, 0), (self.x, 0, env.PIPE_BODY_IMAGE.get_width(), self.length), 2)
        else:
            y_offset = env.SCREEN_HEIGHT - self.length
            while y_offset < env.SCREEN_HEIGHT:
                screen.blit(env.PIPE_BODY_IMAGE, (self.x, y_offset))
                y_offset += env.PIPE_BODY_IMAGE.get_height()
            screen.blit(env.PIPE_HEAD_IMAGE, (self.x, env.SCREEN_HEIGHT - self.length))

            if env.SHOW_HITBOXES:
                # Show hitbox of bottom pipe
                pygame.draw.rect(screen, (255, 0, 0), (self.x, env.SCREEN_HEIGHT - self.length, env.PIPE_BODY_IMAGE.get_width(), env.SCREEN_HEIGHT), 2)