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

def draw_initial_pipes(window, pipe_height):
    # Generate first two pipes
    pipe1 = generate_pipes(window, pipe_height)
    pipe2 = generate_pipes(window, pipe_height)

    # Create pair of upper pipes
    upper_pipes = [
        {'x': pipe1[0]['x'],'y': pipe1[0]['y'], 'img': None},
        {'x': pipe1[0]['x'] + 280,'y': pipe2[0]['y'], 'img': None},
    ]

    # Create pair of lower pipes
    lower_pipes = [
        {'x': pipe1[1]['x'], 'y': pipe1[1]['y'], 'img': None},
        {'x': pipe1[1]['x'] + 280,'y': pipe2[1]['y'], 'img': None},
    ]

    return(upper_pipes,lower_pipes)

def move_pipes(upper,lower,v):
    for upperPipe, lowerPipe in zip(upper, lower):
        upperPipe['x'] += v
        lowerPipe['x'] += v

    return (upper,lower)

def add_pipes(window, pipe_height, upper,lower):
    newpipe = generate_pipes(window, pipe_height)
    newpipe[0]['img'] = None
    upper.append(newpipe[0])
    newpipe[1]['img'] = None
    lower.append(newpipe[1])

    return (upper,lower)

def remove_pipes(upper,lower):
    upper.pop(0)
    lower.pop(0)

    return (upper,lower)

def redraw_pipes(window, upper_pipe_image, lower_pipe_image, lower_pipe_size, upper,lower):
    for upperPipe, lowerPipe in zip(upper, lower):
        if not upperPipe['img']:
            window.blit(upper_pipe_image,
                    (upperPipe['x'], upperPipe['y']))
            upperPipe['img'] = upper_pipe_image
        else:
            window.blit(upperPipe['img'],
                    (upperPipe['x'], upperPipe['y']))
            # print(f"({lowerPipe['x']}, {lowerPipe['y']+(lowerPipe['y'] - lower_pipe_size)}) {lowerPipe['y']}")
        if not lowerPipe['img']:
            lowerPipe['y'] += 320 - lower_pipe_size
            window.blit(lower_pipe_image,
                (lowerPipe['x'], lowerPipe['y']))
            lowerPipe['img'] = lower_pipe_image
        else:
            window.blit(lowerPipe['img'],
                    (lowerPipe['x'], lowerPipe['y']))

    return (upper,lower)

def generate_lower_pipe(pipe_image,lower_pipe_height):
    pipe_width = pipe_image.get_width()
    lower_pipe = pygame.transform.scale(pipe_image,(pipe_width,lower_pipe_height))

    return lower_pipe

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

def get_score(flappy_bird, pipe_width, upper, current_score):
    bird_pos = flappy_bird['pos_x'] + flappy_bird['width']/2
    for pipes in upper:
        pipeMidPos = pipes['x'] + pipe_width/2
        # Add point if bird passes a pipe
        if pipeMidPos <= bird_pos < pipeMidPos + 4:
            current_score += 1

    return current_score

def is_game_over(window_height, flappy_bird, pipe_height, pipe_width, upper, lower):
    elevation = window_height * 0.8
    # Game over if bird is too high or too low
    if flappy_bird['pos_y'] > elevation - 51 or flappy_bird['pos_y'] < 0:
        return True

    # Game over if bird hit upper pipe
    for pipes in upper:
        if (flappy_bird['pos_y'] < pipe_height + pipes['y'] and
           abs(flappy_bird['pos_x'] - pipes['x']) < pipe_width):
            return True

    # Game over if bird hit lower pipe
    for pipes in lower:
        if (flappy_bird['pos_y'] + flappy_bird['height'] > pipes['y']) and\
                abs(flappy_bird['pos_x'] - pipes['x']) < pipe_width:
            return True

    return False
