import itertools
from collections import deque
import pygame
import random
import screen_utils
import config


def lines(screen, lines_lifespan=2000):
    verbose = config.verbose
    running = config.running
    palette, palette_name = screen_utils.get_palette()
    colors = itertools.cycle(palette)
    if verbose:
        print("lines, {}".format(palette_name))
    base_color = next(colors)
    next_color = next(colors)
    step = 0
    number_of_steps = 100

    screen_width = screen.sizeX
    screen_height = screen.sizeY

    line_size = 2
    number_of_lines = 100
    line = [0, 0, 0, 0, pygame.color.Color("black")]
    lines_list = deque([])
    for i in range(number_of_lines - 1):
        lines_list.append(line)
    x1 = random.randint(1, screen_width)
    x2 = random.randint(1, screen_width)
    y1 = random.randint(1, screen_height)
    y2 = random.randint(1, screen_height)
    line = [x1, y1, x2, y2, pygame.color.Color("black")]
    lines_list.append(line)
    min_move = 1
    max_move = 10
    dir_x1 = random.randint(min_move, max_move)
    dir_x2 = random.randint(min_move, max_move)
    dir_y1 = random.randint(min_move, max_move)
    dir_y2 = dir_x2 + 1
    screen.clear()
    for lifespan in range(lines_lifespan):
        screen_utils.check_event(screen)
        current_color = screen_utils.color_fade_from_palette(base_color, next_color, step, number_of_steps)
        if step >= number_of_steps:
            step = 1
            base_color = next_color
            next_color = next(colors)
        else:
            step += 1
            pass

        pygame.draw.line(screen.window, pygame.color.Color("black"), (lines_list[0][0], lines_list[0][1]),
                         (lines_list[0][2], lines_list[0][3]), line_size)
        if x1 <= 1 or x1 >= screen_width:
            dir_x1 = dir_x1 * -1
        if x2 <= 1 or x2 >= screen_width:
            dir_x2 = dir_x2 * -1
        if y1 <= 1 or y1 >= screen_height:
            dir_y1 = dir_y1 * -1
        if y2 <= 1 or y2 >= screen_height:
            dir_y2 = dir_y2 * -1

        x1 += dir_x1
        x2 += dir_x2
        y1 += dir_y1
        y2 += dir_y2
        line = [x1, y1, x2, y2, current_color]
        lines_list.append(line)
        for i in range(1, len(lines_list)):
            pygame.draw.line(screen.window, lines_list[i][4], (lines_list[i][0], lines_list[i][1]),
                             (lines_list[i][2], lines_list[i][3]), line_size)

        lines_list.popleft()
        pygame.display.update()
        screen.clock.tick(100)
    screen.clear()
    return running
