#!/usr/bin/env python3
"""Flappy Bird - core module"""

__author__ = "Marcin Rzewucki"
__copyright__ = "Copyright 2022"
__version__ = "0.0.1"
__maintainer__ = "Marcin Rzewucki"
__email__ = "marcin@rzewucki.com"
__status__ = "Development"

import os
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
bestresult = 0

def game_setup():
    game = {}
    # Load background image
    background = pygame.image.load(BACKGROUND_IMAGE)
    # Get background height and width
    game['window_height'] = background.get_height()
    game['window_width'] = background.get_width()

    window = pygame.display.set_mode((game['window_width'], game['window_height']))
    # Set title for game window
    pygame.display.set_caption("Flappy Bird")
    pygame.init()
    game['window'] = window
    # Define screen fonts
    game['COUNTER_FONT'] = pygame.font.SysFont('Verdana', 60)
    game['GAME_OVER_FONT'] = pygame.font.SysFont('Verdana', 30)
    game['WELCOME_FONT'] = pygame.font.SysFont('Arial', 30)
    game['background'] = load_image(BACKGROUND_IMAGE)
    game['bird'] = load_image(BIRD_IMAGE)
    game['bird_height'] = game['bird'].get_height()
    game['bird_width'] = game['bird'].get_width()
    game['pipe'] = load_image(PIPE_IMAGE)
    game['pipe_height'] = game['pipe'].get_height()
    game['pipe_width'] = game['pipe'].get_width()
    game['scorebox'] = load_image(SCOREBOX_IMAGE)
    game['scorebox_height'] = game['scorebox'].get_height()
    game['scorebox_width'] = game['scorebox'].get_width()
    game['upper_pipe'] = pygame.transform.rotate(game['pipe'], 180)
    # Resize bird image
    game['bird'] = pygame.transform.scale(game['bird'], (60, 50))
    game['clock'] = pygame.time.Clock()
    # Set bird starting position
    game['bird_horizontal'] = int(game['window_width']/2) - 30
    game['bird_vertical'] = int((game['window_height'] - game['bird_height'])/2) - 50
    game['bestresult'] = read_best_result()

    return game

def load_image(name):
    return pygame.image.load(name)

def quit_game(result):
    global bestresult

    if int(result) > int(bestresult):
        write_best_result(result)

    pygame.quit()
    sys.exit()

def quit_or_play(result):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game(result)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game(result)
            else:
                if int(result) > int(bestresult):
                    write_best_result(result)
                return event

def read_best_result():
    global bestresult

    filename = 'bestresult.txt'
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                bestresult = f.read()
            f.close()
        except:
            print("File read error")
            sys.exit()

    return int(bestresult)

def write_best_result(result):
    filename = 'bestresult.txt'
    try:
        with open(filename, 'w') as f:
            f.write(str(result))
        f.close()
    except:
        print("File write error")
        sys.exit()
