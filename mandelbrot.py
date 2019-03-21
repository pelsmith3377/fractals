"""
 There's a lot of mandelbrot software out there, and I fiddled with much of it before visiting the following
 two sites:

    http://en.wikipedia.org/wiki/Mandelbrot_set
    logic from http://warp.povusers.org/Mandelbrot/

From these two I was able to build my own mandelbrot functions, and then finally understand what I was
trying to accomplish.  But is my understanding real, or is it just imaginary?  Who can tell.  It's all so complex.
"""

import pygame
import config
import time
import random
import screen_utils
from numba import jit


@jit
def mandelbrot_formula(x, y, min_re, re_factor, max_im, im_factor, max_iter):
    c_re = min_re + x * re_factor
    c_im = max_im - y * im_factor
    z_re = c_re
    z_im = c_im
    is_inside = True
    for n in range(max_iter):
        z_re2 = z_re * z_re
        z_im2 = z_im * z_im
        if z_re2 + z_im2 > 4:
            is_inside = False
            break
        z_im = 2 * z_re * z_im + c_im
        z_re = z_re2 - z_im2 + c_re
    return is_inside, n


@jit
def julia_formula(x, y, w, h, min_re, min_im, max_iter):
    z_re = 1.8 * (x - w / 2) / (0.5 * w)
    z_im = 1.3 * (y - h / 2) / (0.5 * h)
    c_re = min_re
    c_im = min_im
    is_inside = True
    for n in range(max_iter):
        z_re2 = z_re * z_re
        z_im2 = z_im * z_im
        if z_re2 + z_im2 > 4:
            is_inside = False
            break
        z_im = 2 * z_re * z_im + c_im
        z_re = z_re2 - z_im2 + c_re
    return is_inside, n


def mandelbrot(screen, mandelbrot_lifespan=20):
    running = config.running
    verbose = config.verbose
    width, height = screen.sizeX, screen.sizeY
    # w = width
    # h = height
    max_iter = 100
    iter_step = 20
    '''scale is the size of the viewing area within the mandelbrot set.  Smaller numbers means you are zooming
        in on a smaller subsection of the mandelbrot.'''
    scale = 1
    '''Explore the mandelbrot this many times before returning to main.'''
    # mandelbrot_lifespan = 40
    '''On the first pass, when drawing the entire mandelbrot, add in points near max iteration.  These
        are the most interesting places on the mandelbrot anyway.'''
    interesting_points = []
    julia = False

    for step in range(mandelbrot_lifespan):
        '''A random choice for various color schemes used by the program'''
        if config.testing:
            color_scheme = 4
        else:
            if not julia:
                color_scheme = random.randint(0, 5)
        random_color = screen_utils.get_random_color()
        '''One of the choices just does a modulo of the r/g/b components'''
        red = random.randint(50, 255)
        green = random.randint(50, 255)
        blue = random.randint(50, 255)
        '''Get a palette if needed.  Sending "search" to my get_palette function has it select
            text fields from THECOLORS.  Other choices can be real ugly'''
        palette, palette_name = screen_utils.get_palette("neon")
        '''Every 20th pass, just draw a full mandelbrot set'''
        if step % 20 == 0:
            min_im = -1.2
            max_im = 1.2
            min_re = -2.5
            max_re = 1.0
            re_factor = (max_re - min_re) / width
            im_factor = (max_im - min_im) / height
        else:
            if julia:
                p1 = random.randint(0, len(interesting_points) - 1)
            min_re = interesting_points[p1][0]
            max_re = min_re + scale
            min_im = interesting_points[p1][1]
            max_im = min_im + (max_re - min_re) * height / width
            re_factor = (max_re - min_re) / (width - 1)
            im_factor = (max_im - min_im) / (height - 1)
            # if verbose:
            #     print_screen("Zooming in on interesting point{}:{}".format(p1, interesting_points[p1]))

        start_time = time.time()
        for y in range(height):
            for x in range(width):
                screen_utils.check_event(screen)
                if julia:
                    is_inside, n = julia_formula(x, y, width, height, min_re, min_im, max_iter)
                else:
                    is_inside, n = mandelbrot_formula(x, y, min_re, re_factor, max_im, im_factor, max_iter)
                if is_inside:
                    '''Black for points inside the mandelbrot set'''
                    screen.point(x, y, [0, 0, 0])
                else:
                    if color_scheme == 0:
                        n = n % 1000
                        palette_name = "bit shift"
                        current_color = (n << 21) + (n << 10) + n * 8
                    elif color_scheme == 1:
                        n = n % 1000
                        palette_name = "modulo"
                        current_color = n % 4 * 64, n % 8 * 32, n % 16 * 16
                    elif color_scheme == 2:
                        palette_name = "dark modulo"
                        current_color = [red % (n + 1), green % (n + 1), blue % (n + 1)]
                    elif color_scheme == 3:
                        palette_name = "fade"
                        current_color = screen_utils.color_fade_from_palette("black", random_color, n, max_iter)
                    else:
                        current_color = pygame.color.Color(palette[n % len(palette)])
                        # current_color = palette[n % len(palette)]
                    screen.point(x, y, current_color)
                    '''If this is the first pass (drawing the entire mandelbrot), create a list
                        of interesting points for zooming in on'''
                    if step == 0:
                        if n >= max_iter - 5:
                            c_re = min_re + x * re_factor
                            c_im = max_im - y * im_factor
                            interesting_points.append((c_re, c_im))
        pygame.display.flip()
        end_time = time.time()
        if verbose:
            print("mandelbrot, palette:{}, iterations:{}, real:{} to {}, imag:{} "
                  "to {}, time: {}".format(
                                        palette_name, max_iter, round(min_re, 2), round(max_re, 2),
                                        round(min_im, 2), round(max_im, 2), round(end_time - start_time, 2)))
            # print_screen("number of interesting points:{}".format(len(interesting_points)))

        pygame.display.flip()
        '''Toggles between displaying a section of the mandelbrot or showing a julia set'''
        julia = not julia
        max_iter += iter_step
        if max_iter <= 200:
            scale = 0.1
        elif max_iter <= 300:
            scale = 0.01
        else:
            scale = 0.001
    screen.clear()
    return running
