"""
I believe this code originally came from https://github.com/ActiveState/code
"""

import math
import cmath
import pygame
import random
import time
import screen_utils
import config
from numba import jit


@jit
# put any complex function here to generate a fractal for it!
def z_function(z, c):
    # c = z**(c+1) - 1.0
    if c == 0: c = z**3 - 1.0
    elif c == 1: c = z**3 - 10
    elif c == 2: c = cmath.tan(z**3) - 1.0
    elif c == 3: c = cmath.acos(z**3) - 1.0
    elif c == 4: c = (z * cmath.sin(z)) - 1.0
    elif c == 5: c = z * cmath.cos(z) - 1.0
    elif c == 6: c = z**math.pi - 1.0
    elif c == 7: c = z**18 - 1.0
    elif c == 8: c = (cmath.sin(z) + 0.5 * z)**1.77 - 1.0
    elif c == 9: c = z**5 - z**3 - 1.0
    elif c == 10: c = z**5 + z**3 - 1.0
    elif c == 11: c = (0.5 * z)**3 - 1.0
    # Rest are ugly
    elif c == 12: c = 0.25 * (1 + 4 * z - (1 + 2 * z) * cmath.cos(math.pi * z))  #
    elif c == 13: c = z**3 - cmath.sin(z) - 1  #
    elif c == 14: c = cmath.sin(z) * cmath.cos(z) - 1.0  # math error
    elif c == 15: c = cmath.sin(z) * cmath.cos(z) * 2 - 1.0  #
    elif c == 16: c = cmath.log(z)  #
    elif c == 17: c = z**math.e - 1.0  #
    elif c == 18: c = z**4 + z - 1.0  #
    elif c == 19: c = z**3 + 2 * z * z + z + 3
    else: c = z**10 - 1.0
    # print_screen(c)
    return c


def newton(screen):
    # Newton fractals
    # FB - 201003291
    running = True
    size_x = screen.sizeX
    size_y = screen.sizeY

    # drawing area
    xa = -1.0
    xb = 1.0
    ya = -1.0
    yb = 1.0

    max_iterations = 20  # max iterations allowed
    h = 1e-6  # step size for numerical derivative
    eps = 1e-3  # max error allowed

    # newton_lifespan = 1

    # for c in range(newton_lifespan):
    start_time = time.time()
    if config.testing:
        c = 19
    else:
        c = random.randint(0, 11)
    if config.verbose:
        print("Newton, starting c={} with {} iterations".format(c, max_iterations))
    # screen.clear()
    # draw the fractal
    for y in range(size_y):
        zy = y * (yb - ya) / (size_y - 1) + ya
        for x in range(size_x):
            zx = x * (xb - xa) / (size_x - 1) + xa
            z = complex(zx, zy)
            for i in range(max_iterations):
                screen_utils.check_event(screen)
                # complex numerical derivative
                dz = (z_function(z + complex(h, h), c) - z_function(z, c)) / complex(h, h)
                z0 = z - z_function(z, c) / (dz + 0.00001) # Newton iteration
                if abs(z0 - z) < eps: # stop when close enough to any root
                    break
                z = z0
            screen.point(x, y, (i % 4 * 64, i % 8 * 32, i % 16 * 16))
    pygame.display.flip()
    end_time = time.time()
    if config.verbose:
        print("c={} completed in {}".format(c, end_time - start_time))
    time.sleep(4)
    return running
