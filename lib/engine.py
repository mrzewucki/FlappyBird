#!/usr/bin/env python3
"""Flappy Bird - engine module"""

__author__ = "Marcin Rzewucki"
__copyright__ = "Copyright 2022"
__version__ = "0.0.1"
__maintainer__ = "Marcin Rzewucki"
__email__ = "marcin@rzewucki.com"
__status__ = "Development"

import random


# Generate pipes on the screen
def generate_pipes(window, pipe_image):
    window_width = window.get_width()
    window_height = window.get_height()
    pipe_height = pipe_image.get_height()
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

def move_pipes(upper,lower,v):
    for upperPipe, lowerPipe in zip(upper, lower):
        upperPipe['x'] += v
        lowerPipe['x'] += v

    return (upper,lower)