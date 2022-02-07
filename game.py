#!/usr/bin/env python3
"""Flappy Bird"""

__author__ = "Marcin Rzewucki"
__copyright__ = "Copyright 2022"
__version__ = "0.0.1"
__maintainer__ = "Marcin Rzewucki"
__email__ = "marcin@rzewucki.com"
__status__ = "Development"

import pygame
import sys

from lib import core

window = core.game_setup()
window_width = window.get_width()
window_height = window.get_height()

pygame.init()
background = core.load_image(core.BACKGROUND_IMAGE)
bird = core.load_image(core.BIRD_IMAGE)
bird = pygame.transform.scale(bird,(60,50))
clock = pygame.time.Clock()
counterFont = pygame.font.SysFont('Verdana', 60)
welcomeFont = pygame.font.SysFont('Arial', 30)

horizontal = int(window_width/2) - 30
vertical = int((window_height - bird.get_height())/2) - 50

while True:
    window.blit(background, (0, 0))
    window.blit(bird,(horizontal,vertical))
    window.blit(counterFont.render("Get Ready!", True, core.GREEN), (int(window_width/2)-150, int(window_height/3)))
    window.blit(welcomeFont.render("Press UP to start", True, core.YELLOW), (int(window_width/2)-110, int(window_height/2)))
    window.blit(counterFont.render(str(int(0)), True, core.WHITE), (int(window_width/2)-25, int(window_height/5)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.update()
    clock.tick(10)
