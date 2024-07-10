import environment_variables as env
import pygame

class Bird:
    def __init__(self):
        self.image = env.BIRD_IMAGE
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = 50
        self.y = env.SCREEN_HEIGHT // 2
        self.velocity = 0

    def update(self):
        self.velocity += env.BIRD_GRAVITY
        self.y += self.velocity

        if self.y < 0:
            self.y = 0
            self.velocity = 0

        if self.y + self.height > env.SCREEN_HEIGHT:
            self.y = env.SCREEN_HEIGHT - self.height
            self.velocity = 0

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

        # show hitbox of bird
        if env.SHOW_HITBOXES:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)

    def flap(self):
        self.velocity = env.BIRD_LIFT