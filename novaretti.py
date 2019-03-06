"""
from a post at https://www.reddit.com/r/FractalPorn/comments/52g4vm/elena_novaretti_i_1920_x_1080_oc
by bryceguy72, that he credits to Elena Novaretti.  His post supplied the core logic.
"""

import config
import screen_utils
import pygame
import random
import math
from numba import jit


@jit
def novaretti_formula(x, y, w, h, cr, ci, field, max_iter):
    # r = 1.8 * (x - w / 2) / (0.5 * w)
    # i = 1.3 * (y - h / 2) / (0.5 * h)
    r = field * (x - w / 2) / (0.5 * w)
    i = field * (y - h / 2) / (0.5 * h)
    if config.testing:
        cr = .012104
        ci = -.01549

    s = 0
    for n in range(max_iter):
        t1 = r * r * r - 3 * r * i * i
        t2 = 3 * r * r * i - i * i * i
        t3 = t1 + t1 - cr
        t4 = t2 + t2 - ci
        t5 = t3 * t3 - t4 * t4
        t4 = 2 * t3 * t4
        t3 = t5
        t1 = (-t1 - cr) * 6
        t2 = (-t2 - ci) * 6
        t5 = t1 * r - t2 * i
        t2 = t1 * i + t2 * r
        t1 = t5
        t5 = 1 / (t3 * t3 + t4 * t4)
        r = (t3 * t1 + t4 * t2) * t5
        i = (t3 * t2 - t4 * t1) * t5

        s = s + math.log(r * r + i * i)
    return int(abs(s))


def novaretti(screen, novaretti_lifespan=5):
    running = True
    verbose = config.verbose
    width, height = screen.sizeX, screen.sizeY
    # novaretti_lifespan = 40
    fade = 200
    for step in range(novaretti_lifespan):
        palette, palette_name = screen_utils.get_palette("search")
        color_1 = screen_utils.get_random_color("dark")
        color_2 = screen_utils.get_random_color("light")
        # cr = round(random.uniform(-0.01, 0.01), 5)
        # ci = round(random.uniform(-0.01, 0.01), 5)
        cr = round(random.uniform(-0.05, 0.05), 5)
        ci = round(random.uniform(-0.05, 0.05), 5)
        field = round(random.uniform(1, 10), 2)
        max_iter = random.randint(3, 20)
        if max_iter < 10:
            palette_name = "dark/light"
        # field = 15
        if verbose:
            print("novaretti, palette:{} real={}, imag={}, field={}, "
                  "iter={}".format(palette_name, cr, ci, field, max_iter))
        for y in range(height - 1):
            for x in range(width - 1):
                screen_utils.check_event()
                n = novaretti_formula(x, y, width, height, cr, ci, field, max_iter)
                n = n % fade
                # if n < 26:
                #     current_color = screen_utils.color_fade_from_palette(color_1, color_2, n, fade)
                # else:
                #     current_color = screen_utils.color_fade_from_palette(color_3, color_4, n, fade)

                if max_iter < 10:
                    current_color = pygame.color.Color(palette[n % (len(palette) - 1)])
                else:
                    current_color = screen_utils.color_fade_from_palette(color_1, color_2, n, fade)

                screen.point(x, y, current_color)
        pygame.display.flip()
    screen.clear()
    return running
