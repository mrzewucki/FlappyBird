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
rotated_pipe = pygame.transform.rotate(pipe, 180)

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
    lower_pipe = pipe

    # Generate first two pipes
    pipe1 = engine.generate_pipes(window, pipe)
    pipe2 = engine.generate_pipes(window, pipe)

    # Create pair of lower pipes
    lower_pipes = [
        {'x': pipe1[1]['x'], 'y': pipe1[1]['y'],'img': None},
        {'x': pipe1[1]['x'] + vertical,'y': pipe2[1]['y'],'img': None},
    ]

    # Create pair of upper pipes
    upper_pipes = [
        {'x': pipe1[0]['x'],'y': pipe1[0]['y'],'img': None},
        {'x': pipe1[0]['x'] + vertical + 50,'y': pipe2[0]['y'],'img': None},
    ]

    pipe_velocity = -4
    lower_pipe_size = pipe.get_height()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        (upper_pipes,lower_pipes) = engine.move_pipes(upper_pipes,lower_pipes,pipe_velocity)

        # Generate new pipe when some of them is about to leave the screen
        if 0 < upper_pipes[0]['x'] < 5:
            newpipe = engine.generate_pipes(window, pipe)
            newpipe[0]['img'] = None
            upper_pipes.append(newpipe[0])
            newpipe[1]['img'] = None
            lower_pipes.append(newpipe[1])

        # If the pipe is out, remove it
        if upper_pipes[0]['x'] < -pipe.get_width():
            lower_pipe_size = random.randint(160,pipe.get_height())
            upper_pipes.pop(0)
            lower_pipes.pop(0)
            if lower_pipe_size != pipe.get_height():
                lower_pipe = pygame.transform.scale(pipe,(pipe.get_width(),lower_pipe_size))
            else:
                lower_pipe = pipe

        window.blit(background, (0, 0))
        for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
            if not upperPipe['img']:
                window.blit(rotated_pipe,
                    (upperPipe['x'], upperPipe['y']))
                upperPipe['img'] = rotated_pipe
            else:
                window.blit(upperPipe['img'],
                    (upperPipe['x'], upperPipe['y']))
            # print(f"({lowerPipe['x']}, {lowerPipe['y']+(lowerPipe['y'] - lower_pipe_size)}) {lowerPipe['y']}")
            if not lowerPipe['img']:
                lowerPipe['y'] += 320 - lower_pipe_size
                window.blit(lower_pipe,
                    (lowerPipe['x'], lowerPipe['y']))
                lowerPipe['img'] = lower_pipe
            else:
                window.blit(lowerPipe['img'],
                    (lowerPipe['x'], lowerPipe['y']))

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
