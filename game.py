#!/usr/bin/env python3
"""Flappy Bird"""

__author__ = "Marcin Rzewucki"
__copyright__ = "Copyright 2022"
__version__ = "0.0.1"
__maintainer__ = "Marcin Rzewucki"
__email__ = "marcin@rzewucki.com"
__status__ = "Development"

import pygame

from lib import core
from lib import engine

game = core.game_setup()

def welcome_screen():
    global game
    game['window'].blit(game['background'], (0, 0))
    game['window'].blit(game['bird'], (game['bird_horizontal'], game['bird_vertical']))
    game['window'].blit(game['COUNTER_FONT'].render("Get Ready!", True, core.GREEN),
                (int(game['window_width']/2)-150, int(game['window_height']/3)))
    game['window'].blit(game['WELCOME_FONT'].render("Press UP key to start", True,
                core.YELLOW), (int(game['window_width']/2)-130, int(game['window_height']/2)))
    game['window'].blit(game['COUNTER_FONT'].render("0", True, core.WHITE),
                (int(game['window_width']/2)-25, int(game['window_height']/5)))

def game_over_screen(points):
    global game
    game['window'].blit(game['WELCOME_FONT'].render("Press a key to continue", True,
                core.YELLOW), (int(game['window_width']/2)-150, int(game['window_height']/2+game['scorebox_height']/2)))
    game['window'].blit(game['GAME_OVER_FONT'].render(str(game['bestresult']), True, core.WHITE),
                    (int(game['window_width']/2)+40, int(game['window_height']/2 - 35)))
    game['window'].blit(game['GAME_OVER_FONT'].render(str(int(points)), True, core.WHITE),
                    (int(game['window_width']/2)+40, int(game['window_height']/2 - 85)))

def start_game():
    global game
    pipes = {
        'height': game['pipe_height'],
        'width': game['pipe_width'],
        'pipe': game['pipe'],
        'upper_pipe': game['upper_pipe'],
        'lower_pipe': game['pipe'],
        'lower_pipe_height': game['pipe_height'],
        'velocity': -4,
        'upper': [],
        'lower': []
    }
    flappy_bird = {
        'score': 0,
        'height': game['bird_height'],
        'width': game['bird_width'],
        'pos_y': game['bird_vertical'],
        'pos_x': game['bird_horizontal'],
        'velocity': -9,
        'max_velocity': 10,
        'speed': 1,
        'flap_velocity': -8,
        'flapped': False
    }

    pipes = engine.draw_initial_pipes(game['window'],pipes)

    while True:
        event = core.quit_or_play(flappy_bird['score'])
        if event and event.key == pygame.K_UP:
            engine.bird_flap(flappy_bird)

        engine.bird_move(game['window_height'], flappy_bird)
        flappy_bird = engine.get_score(flappy_bird, pipes)
        game_over = engine.is_game_over(game['window_height'], flappy_bird, pipes)
        if game_over:
            scorebox_y = 10
            points = 0
            while True:
                game['window'].blit(game['background'], (0, 0))
                game['window'].blit(game['COUNTER_FONT'].render("Game Over", True, core.RED),
                    (int(game['window_width']/2)-150, int(150)))
                game['window'].blit(game['scorebox'], (game['window_width']/4, game['window_height']-scorebox_y))

                if scorebox_y < game['window_height']/2 + game['scorebox_height']:
                    scorebox_y += 10
                    game['clock'].tick(32)
                else:
                    game_over_screen(points)
                    if points < flappy_bird['score']:
                        points += 1
                        game['clock'].tick(5)
                    else:
                        game['clock'].tick(32)
                        # Quit or play again
                        event = core.quit_or_play(flappy_bird['score'])
                        if event:
                            return

                pygame.display.update()

        pipes = engine.move_pipes(pipes)

        # Generate new pipe when some of them is about to leave the screen
        if 0 < pipes['upper'][0]['x'] < 5:
            pipes = engine.add_pipes(game['window'], pipes)

        # If the pipe is out, remove it
        if pipes['upper'][0]['x'] < -pipes['width']:
            pipes = engine.remove_pipes(pipes)
            # Generate random size lower pipe
            pipes = engine.generate_lower_pipe(pipes)

        game['window'].blit(game['background'], (0, 0))
        game['window'].blit(game['COUNTER_FONT'].render(str(int(flappy_bird['score'])), True, core.WHITE),
                    (int(game['window_width']/2)-25, int(game['window_height']/5)))
        game['window'].blit(game['bird'], (game['bird_horizontal'], flappy_bird['pos_y']))
        pipes = engine.redraw_pipes(game['window'], pipes)

        pygame.display.update()
        game['clock'].tick(32)


def main():
    while True:
        welcome_screen()
        event = core.quit_or_play(0)
        if event and event.key == pygame.K_UP:
            start_game()
        pygame.display.update()
        game['clock'].tick(10)

main()
