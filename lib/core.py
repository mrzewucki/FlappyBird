#!/usr/bin/env python3
"""Flappy Bird - core module"""

__author__ = "Marcin Rzewucki"
__copyright__ = "Copyright 2022"
__version__ = "0.0.1"
__maintainer__ = "Marcin Rzewucki"
__email__ = "marcin@rzewucki.com"
__status__ = "Development"

import pygame
import sys

# Define image files
PIPE_IMAGE = 'images/pipe.png'
BACKGROUND_IMAGE = 'images/background.jpg'
BIRD_IMAGE = 'images/bird.png'
SCOREBOX_IMAGE = 'images/scorebox.png'

# Define font colors (in RGB)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)

# Define global game window
window = None

def game_setup():
    # Load background image
    imageObject = pygame.image.load(BACKGROUND_IMAGE)
    # Get background height and width
    height = imageObject.get_height()
    width = imageObject.get_width()

    window = pygame.display.set_mode((width, height))
    # Set title for game window
    pygame.display.set_caption("Flappy Bird")

    return window

def load_image(name):
    return pygame.image.load(name)

def quit_or_play():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            else:
                return event
