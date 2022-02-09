#!/usr/bin/env python3
"""Flappy Bird - engine module"""

__author__ = "Marcin Rzewucki"
__copyright__ = "Copyright 2022"
__version__ = "0.0.1"
__maintainer__ = "Marcin Rzewucki"
__email__ = "marcin@rzewucki.com"
__status__ = "Development"

import pygame
import random

# Generate pipes on the screen
def generate_pipes(window, pipe_height):
    window_width = window.get_width()
    window_height = window.get_height()
    # skip bottom part of the screen
    bottom_offset = 63
    # start pipe from the ground
    yB = bottom_offset + pipe_height
    # skip left part of the screen
    left_offset = 50

    x = window_width + left_offset
    yU = pipe_height - random.randrange(100, int(0.3*window_height))
    pipe = [
        # upper pipe coords
        {'x': x, 'y': -yU},
        # lower pipe coords
        {'x': x, 'y': yB}
    ]

    return pipe

def draw_initial_pipes(window, pipes):
    # Generate first two pipes
    pipe1 = generate_pipes(window, pipes['height'])
    pipe2 = generate_pipes(window, pipes['height'])

    # Create pair of upper pipes
    pipes['upper'] = [
        {'x': pipe1[0]['x'],'y': pipe1[0]['y'], 'img': None},
        {'x': pipe1[0]['x'] + 280,'y': pipe2[0]['y'], 'img': None}
    ]

    # Create pair of lower pipes
    pipes['lower'] = [
        {'x': pipe1[1]['x'], 'y': pipe1[1]['y'], 'img': None},
        {'x': pipe1[1]['x'] + 280,'y': pipe2[1]['y'], 'img': None}
    ]

    return pipes

def move_pipes(pipes):
    for upperPipe, lowerPipe in zip(pipes['upper'], pipes['lower']):
        upperPipe['x'] += pipes['velocity']
        lowerPipe['x'] += pipes['velocity']

    return pipes

def add_pipes(window, pipes):
    newpipe = generate_pipes(window, pipes['height'])
    newpipe[0]['img'] = None
    pipes['upper'].append(newpipe[0])
    newpipe[1]['img'] = None
    pipes['lower'].append(newpipe[1])

    return pipes

def remove_pipes(pipes):
    pipes['upper'].pop(0)
    pipes['lower'].pop(0)

    return pipes

def redraw_pipes(window, pipes):
    for upperPipe, lowerPipe in zip(pipes['upper'], pipes['lower']):
        if not upperPipe['img']:
            window.blit(pipes['upper_pipe'],
                    (upperPipe['x'], upperPipe['y']))
            upperPipe['img'] = pipes['upper_pipe']
        else:
            window.blit(upperPipe['img'],
                    (upperPipe['x'], upperPipe['y']))
            # print(f"({lowerPipe['x']}, {lowerPipe['y']+(lowerPipe['y'] - lower_pipe_size)}) {lowerPipe['y']}")
        if not lowerPipe['img']:
            lowerPipe['y'] += 320 - pipes['lower_pipe_height']
            window.blit(pipes['lower_pipe'],
                (lowerPipe['x'], lowerPipe['y']))
            lowerPipe['img'] = pipes['lower_pipe']
        else:
            window.blit(lowerPipe['img'],
                    (lowerPipe['x'], lowerPipe['y']))

    return pipes

def generate_lower_pipe(pipes):
    pipes['lower_pipe_height'] = random.randint(160,pipes['height'])
    pipes['lower_pipe'] = pygame.transform.scale(pipes['pipe'],(pipes['width'],pipes['lower_pipe_height']))

    return pipes

def bird_move(window_height, flappy_bird):
    elevation = window_height * 0.8
    if flappy_bird['velocity'] < flappy_bird['max_velocity'] and not flappy_bird['flapped']:
        flappy_bird['velocity'] += flappy_bird['speed']

    if flappy_bird['flapped']:
        flappy_bird['flapped'] = False

    flappy_bird['pos_y'] += \
        min(flappy_bird['velocity'], elevation - flappy_bird['pos_y'] - flappy_bird['height'])

def bird_flap(flappy_bird):
    if flappy_bird['pos_y'] > 0:
        flappy_bird['velocity'] = flappy_bird['flap_velocity']
        flappy_bird['flapped'] = True

def get_score(flappy_bird, pipes, current_score):
    bird_pos = flappy_bird['pos_x'] + flappy_bird['width']/2
    for pipe in pipes['upper']:
        pipeMidPos = pipe['x'] + pipes['width']/2
        # Add point if bird passes a pipe
        if pipeMidPos <= bird_pos < pipeMidPos + 4:
            current_score += 1

    return current_score

def is_game_over(window_height, flappy_bird, pipes):
    elevation = window_height * 0.8
    # Game over if bird is too high or too low
    if flappy_bird['pos_y'] > elevation - 51 or flappy_bird['pos_y'] < 0:
        return True

    # Game over if bird hit upper pipe
    for pipe in pipes['upper']:
        if (flappy_bird['pos_y'] < pipes['height'] + pipe['y'] and
           abs(flappy_bird['pos_x'] - pipe['x']) < pipes['width']):
            return True

    # Game over if bird hit lower pipe
    for pipe in pipes['lower']:
        if (flappy_bird['pos_y'] + flappy_bird['height'] > pipe['y']) and\
                abs(flappy_bird['pos_x'] - pipe['x']) < pipes['width']:
            return True

    return False
