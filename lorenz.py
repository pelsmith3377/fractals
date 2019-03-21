"""
Converted from META-L to python from code at http://freymanart.com/Metal/index.htm

Original header from the author as follows:

'Lorenz attractor ©2010 Ivan Freyman  - FreymanArt.com
'For best results, set screen to MILLIONS of colors and let the program
'run for a few minutes.

"""

import screen_utils
import pygame
import config
import random
import itertools


def lorenz(screen):
    running = True
    sx = screen.sizeX
    sy = screen.sizeY
    dt = 0.0005
    x = 1.1
    y = 1.2
    z = 1

    lorenz_cycles = 1000000
    palette, palette_name = screen_utils.get_palette()
    colors = itertools.cycle(palette)
    base_color = next(colors)
    next_color = next(colors)
    current_color = pygame.color.Color(base_color)
    steps_till_color_change = random.randint(100, int(lorenz_cycles / 300))
    step = 1

    if config.verbose:
            print("lorenz, palette:{}".format(palette_name))
    for t2 in range(lorenz_cycles):
        screen_utils.check_event(screen)
        xn = x + 10 * (y - x) * dt
        yn = y + (26 * x - y - x * z) * dt
        zn = z + (x * y - (8 / 3) * z) * dt

        xp = x * sx / 36 + sx / 2
        yp = sy - z * sy / 48 - 20
        # get pixel xp, yp
        # r = r + rr / (1 + r / 40000)
        # color function
        screen.point(int(xp), int(yp), current_color)
        x = xn
        y = yn
        z = zn
        if t2 % 20 == 0:
            pygame.display.flip()

        step += 1
        if step < steps_till_color_change:
            current_color = screen_utils.color_fade_from_palette(base_color, next_color, step, steps_till_color_change)
        else:
            step = 1
            base_color = next_color
            next_color = next(colors)

    return running
