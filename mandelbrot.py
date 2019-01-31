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


def mandelbrot(screen):
    running = config.running
    verbose = config.verbose
    width, height = screen.sizeX, screen.sizeY
    w = width - 1
    h = height - 1
    max_iter = 250
    iter_step = 20
    zoom = 1
    '''Explore the mandelbrot this many times before returning to main.'''
    mandelbrot_lifespan = 40
    '''On the first pass, when drawing the entire mandelbrot, add in points near max iteration.  These
        are the most interesting places on the mandelbrot anyway.'''
    interesting_points = []
    julia = False

    for step in range(mandelbrot_lifespan):
        '''A random choice for various color schemes used by the program'''
        if config.testing:
            color_scheme = 3
        else:
            color_scheme = random.randint(0, 5)
        random_color = screen_utils.get_random_color()
        '''One of the choices just does a modulo of the r/g/b components'''
        red = random.randint(50, 255)
        green = random.randint(50, 255)
        blue = random.randint(50, 255)
        '''Get a palette if needed.  Sending "search" to my get_palette function has it select
            text fields from THECOLORS.  Other choices can be real ugly'''
        palette, palette_name = screen_utils.get_palette("search")
        '''Every 10th pass, just draw a full mandelbrot set'''
        if step % 10 == 0:
            min_im = -1.2
            max_im = 1.2
            min_re = -2.5
            max_re = 1.0
            re_factor = (max_re - min_re) / (width - 1)
            im_factor = (max_im - min_im) / (height - 1)
        else:
            if julia:
                p1 = random.randint(0, len(interesting_points) - 1)
            min_re = interesting_points[p1][0]
            max_re = min_re + zoom
            min_im = interesting_points[p1][1]
            max_im = min_im + (max_re - min_re) * height / width
            re_factor = (max_re - min_re) / (width - 1)
            im_factor = (max_im - min_im) / (height - 1)
            if verbose:
                print("Zooming in on interesting point{}:{}".format(p1, interesting_points[p1]))

        start_time = time.time()
        for y in range(height - 1):
            for x in range(width - 1):
                '''Checking for events really slows down the program.  I should just lock the keyboard 
                    on startup so I can comment this section out. (just kidding)'''
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        screen_utils.close_window()
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            screen.clear()
                            return running
                        if event.key == pygame.K_ESCAPE:
                            screen_utils.close_window()
                            running = False
                    # elif event.type == pygame.MOUSEBUTTONDOWN:
                    #     mouse_x, mouse_y = pygame.mouse.get_pos()
                    #     mouse_real = min_re + mouse_x * re_factor
                    #     mouse_imaginary = max_im - mouse_y * im_factor
                    #     if verbose:
                    #         print("mouse: {}, {} / real: {}, imaginary {}".format(mouse_x, mouse_y,
                    #         mouse_real, mouse_imaginary))
                if julia:
                    is_inside, n = julia_formula(x, y, w, h, min_re, min_im, max_iter)
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
            print("number of interesting points:{}".format(len(interesting_points)))

        pygame.display.flip()
        '''Toggles between displaying a section of the mandelbrot or showing a julia set'''
        julia = not julia
        max_iter += iter_step
        if max_iter <= 200:
            zoom = 0.01
        elif max_iter <= 300:
            zoom = 0.001
        else:
            zoom = 0.0001
    screen.clear()
    return running
