#!/usr/bin/env python3
"""Flappy Bird"""

__author__ = "Marcin Rzewucki"
__copyright__ = "Copyright 2022"
__version__ = "0.0.1"
__maintainer__ = "Marcin Rzewucki"
__email__ = "marcin@rzewucki.com"
__status__ = "Development"

import pygame
import random
import sys

from lib import core
from lib import engine


window = core.game_setup()
window_width = window.get_width()
window_height = window.get_height()

pygame.init()
background = core.load_image(core.BACKGROUND_IMAGE)
bird = core.load_image(core.BIRD_IMAGE)
pipe = core.load_image(core.PIPE_IMAGE)
upper_pipe = pygame.transform.rotate(pipe, 180)

# Resize bird image
bird = pygame.transform.scale(bird, (60, 50))
clock = pygame.time.Clock()
counterFont = pygame.font.SysFont('Verdana', 60)
welcomeFont = pygame.font.SysFont('Arial', 30)

# Set bird starting position
horizontal = int(window_width/2) - 30
vertical = int((window_height - bird.get_height())/2) - 50


def start_game():
    global horizontal
    global vertical
    pipe_height = pipe.get_height()
    pipe_width = pipe.get_width()
    lower_pipe = pipe
    pipe_velocity = -4
    lower_pipe_height = pipe_height
    score = 0
    flappy_bird = {
        'height': bird.get_height(),
        'width': bird.get_width(),
        'pos_y': vertical,
        'pos_x': horizontal,
        'velocity': -9,
        'max_velocity': 10,
        'speed': 1,
        'flap_velocity': -8,
        'flapped': False
    }

    (upper_pipes,lower_pipes) = engine.draw_initial_pipes(window,pipe_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    engine.bird_flap(flappy_bird)

        engine.bird_move(window_height, flappy_bird)
        score = engine.get_score(flappy_bird,pipe_width,upper_pipes,score)
        game_over = engine.is_game_over(window_height, flappy_bird, 
                                        pipe_height, pipe_width,
                                        upper_pipes,
                                        lower_pipes)
        if game_over:
            return

        (upper_pipes,lower_pipes) = engine.move_pipes(upper_pipes,lower_pipes,pipe_velocity)

        # Generate new pipe when some of them is about to leave the screen
        if 0 < upper_pipes[0]['x'] < 5:
            (upper_pipes,lower_pipes) = engine.add_pipes(window,pipe_height,upper_pipes,lower_pipes)

        # If the pipe is out, remove it
        if upper_pipes[0]['x'] < -pipe_width:
            (upper_pipes,lower_pipes) = engine.remove_pipes(upper_pipes,lower_pipes)
            # Generate random size lower pipe
            lower_pipe_height = random.randint(160,pipe_height)
            lower_pipe = engine.generate_lower_pipe(pipe,lower_pipe_height)

        window.blit(background, (0, 0))
        window.blit(counterFont.render(str(int(score)), True, core.WHITE),
                    (int(window_width/2)-25, int(window_height/5)))
        window.blit(bird, (horizontal, flappy_bird['pos_y']))
        (upper_pipes,lower_pipes) = engine.redraw_pipes(window, upper_pipe, lower_pipe, lower_pipe_height, upper_pipes, lower_pipes)

        pygame.display.update()
        clock.tick(32)

while True:
    window.blit(background, (0, 0))
    window.blit(bird, (horizontal, vertical))
    window.blit(counterFont.render("Get Ready!", True, core.GREEN),
                (int(window_width/2)-150, int(window_height/3)))
    window.blit(welcomeFont.render("Press UP to start", True,
                core.YELLOW), (int(window_width/2)-110, int(window_height/2)))
    window.blit(counterFont.render(str(int(0)), True, core.WHITE),
                (int(window_width/2)-25, int(window_height/5)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_UP:
                start_game()

    pygame.display.update()
    clock.tick(10)
