from pathlib import Path
import pygame

asset_folder = Path(__file__).resolve().parent / 'Assets'

# Load and scale images
BIRD_IMAGE = pygame.image.load(asset_folder / 'bird.png')
BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (BIRD_IMAGE.get_width() // 10, BIRD_IMAGE.get_height() // 10))

PIPE_HEAD_IMAGE = pygame.image.load(asset_folder / 'pipe_head.png')
PIPE_HEAD_IMAGE = pygame.transform.scale(PIPE_HEAD_IMAGE, (PIPE_HEAD_IMAGE.get_width() // 10, PIPE_HEAD_IMAGE.get_height() // 10))

PIPE_BODY_IMAGE = pygame.image.load(asset_folder / 'pipe_body.png')
PIPE_BODY_IMAGE = pygame.transform.scale(PIPE_BODY_IMAGE, (PIPE_BODY_IMAGE.get_width() // 10, PIPE_BODY_IMAGE.get_height() // 10))


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PIPE_GAP = 400
PIPE_SPEED = 5
PIPE_SPAWN_INTERVAL = 2000  # in milliseconds
BIRD_GRAVITY = 0.5
BIRD_LIFT = -10
FPS = 120

SHOW_HITBOXES = False

DEATH_SCREEN_BACKGROUND = (100, 100, 100)