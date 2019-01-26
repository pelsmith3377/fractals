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
# import itertools
import screen_utils
from numba import jit

'''OK, yes, this function takes too many arguments.  But its just here so I could pull out the math and 
    JIT compile it for speed.'''


@jit
# def mandelbrot_formula(c_re, c_im, max_iter):
def mandelbrot_formula(x, min_re, c_im, max_iter, re_factor):
    c_re = min_re + x * re_factor
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
def julia_formula(x, y, w, h, c_x, c_y, max_iter):
    zx = 1.5 * (x - w / 2) / (0.5 * w)
    zy = 1.0 * (y - h / 2) / (0.5 * h)
    i = max_iter
    while zx * zx + zy * zy < 4 and i > 1:
        tmp = zx * zx - zy * zy + c_x
        zy = 2.0 * zx * zy + c_y
        zx = tmp
        i -= 1
    return i


def mandelbrot(screen):
    running = config.running
    verbose = config.verbose
    width, height = screen.sizeX, screen.sizeY
    '''The minimum and maximum real and imaginary boundries to draw the entire mandelbrot set'''
    # min_re = -2.5
    # max_re = 1.0
    # min_im = -1.2
    # if config.full_screen:
    #     max_im = min_im + (max_re - min_re) * height / width
    # else:
    # max_im = min_im + (max_re - min_re) * height / width
    # re_factor = (max_re - min_re) / (width - 1)
    # im_factor = (max_im - min_im) / (height - 1)
    # mouse_real = -1.0
    # mouse_imaginary = -1.0
    # n = 0
    '''Increase iterations by iter_step each time we run through the function lifespan.  That way you don't
        have to wait long for initial pictures, but can put them on the screen faster but with less detail.'''
    max_iter = 130
    iter_step = 20
    '''Actually, zoom is the field of view.  A smaller number means a smaller subsection of the mandelbrot.
        In other words, the smaller this number is, the more you are zoomed in.'''
    # zoom = 0.01
    zoom = 1
    '''Amount to move away from the bottom left corner.  An attempt to avoid zooming in on sections of the 
        mandelbrot that are all black except for a small speck in the bottom left corner.  For zoom < 0.001
        it seems best to leave adjust = 0'''
    adjust = 0
    # mouse_x = -1
    # mouse_y = -1
    '''Explore the mandelbrot this many times before returning to main.'''
    mandelbrot_lifespan = 20
    '''On the first pass, when drawing the entire mandelbrot, add in points near max iteration.  These
        are the most interesting places on the mandelbrot anyway.'''
    interesting_points = [(864, 611)]
    julia = False

    for step in range(mandelbrot_lifespan):
        '''A random choice for various color schemes used by the program'''
        if config.testing:
            color_scheme = 0
        else:
            color_scheme = random.randint(0, 3)
        '''One of the choices just does a modulo of the r/g/b components'''
        red = random.randint(50, 255)
        green = random.randint(50, 255)
        blue = random.randint(50, 255)
        '''Get a palette if needed.  Sending "search" to my get_palette function has it select
            text fields from THECOLORS.  Other choices can be real ugly'''
        palette, palette_name = screen_utils.get_palette("search")
        '''If this is the first pass, just draw a full mandelbrot set'''
        if step == 0:
            '''This reset of values is only needed if we are accepting mouse clicks.'''
            p1_real = min_re = -2.5
            p1_imaginary = max_re = 1.0
            min_im = -1.2
            '''Wide screen monitors might cut off part of the mandelbrot to keep the proper aspect ratio'''
            if config.full_screen:
                max_im = 1.2
            else:
                max_im = min_im + (max_re - min_re) * height / width
            re_factor = (max_re - min_re) / (width - 1)
            im_factor = (max_im - min_im) / (height - 1)
            '''If the mouse has been clicked in the mandelbrot, convert the x value on the screen to
                the real component, and the y value to the imaginary component, so they can be calculated
                within the complex plane.  Zoom in on that area.'''
            # elif mouse_x != -1 and mouse_y != -1:
            #     min_re = mouse_real
            #     max_re = min_re + zoom
            #     min_im = mouse_imaginary
            #     max_im = min_im + (max_re - min_re) * height / width
            #     re_factor = (max_re - min_re) / (width - 1)
            #     im_factor = (max_im - min_im) / (height - 1)
            #     # reset so we don't keep drawing this area
            #     mouse_x = -1.0
            #     mouse_y = -1.0
            '''If this is not the first pass, and we don't have a particular mouse click, then 
                choose a random interesting point and zoom in on it.'''
        else:
            '''reset before recalculating our new zoom area, otherwise you just keep zooming in
                further on the first one chosen.'''
            min_re = -2.5
            max_re = 1.0
            min_im = -1.2
            if config.full_screen:
                max_im = 1.2
            else:
                max_im = min_im + (max_re - min_re) * height / width
            re_factor = (max_re - min_re) / (width - 1)
            im_factor = (max_im - min_im) / (height - 1)
            '''Pick a random interesting point, set the surrounding parameters.'''
            p1 = random.randint(0, len(interesting_points) - 1)
            p1_x = interesting_points[p1][0] - adjust
            p1_y = interesting_points[p1][1] - adjust
            p1_real = min_re + p1_x * re_factor
            p1_imaginary = max_im - p1_y * im_factor
            min_re = p1_real
            max_re = min_re + zoom
            min_im = p1_imaginary
            max_im = min_im + (max_re - min_re) * height / width
            re_factor = (max_re - min_re) / (width - 1)
            im_factor = (max_im - min_im) / (height - 1)
            if verbose:
                print("Zooming in on interesting point{}:{}".format(p1, interesting_points[p1]))

        start_time = time.time()
        for y in range(height - 1):
            c_im = max_im - y * im_factor
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
                if julia == True:
                    i = julia_formula(x, y, width - 1, height - 1, p1_real, p1_imaginary, max_iter)
                    screen.point(x, y, (i << 21) + (i << 10) + i * 8)
                else:
                    # n = julia_formula(x, y, width - 1, height - 1, p1_real, p1_imaginary, max_iter)
                    is_inside, n = mandelbrot_formula(x, min_re, c_im, max_iter, re_factor)
                    #  is_inside, n = mandelbrot_formula(c_re, c_im, max_iter)
                    # is_inside = False
                    if is_inside:
                        '''Black for points inside the mandelbrot set'''
                        screen.point(x, y, [0, 0, 0])
                    else:
                        if color_scheme == 0 or step == 0:
                            n = n % 1000
                            palette_name = "bit shift"
                            current_color = (n << 21) + (n << 10) + n * 8
                        elif color_scheme == 1:
                            palette_name = "modulo"
                            current_color = [red % (n + 1), green % (n + 1), blue % (n + 1)]
                            # current_color = [(n + 1) % 255, (n + 1) % 255, (n + 1) % 255]
                        else:
                            current_color = pygame.color.Color(palette[n % len(palette)])
                        screen.point(x, y, current_color)
                        '''If this is the first pass (drawing the entire mandelbrot), create a list
                            of interesting points for zooming in on'''
                        if step == 0:
                            if n >= max_iter - 7:
                                interesting_points.append((x, y))
        pygame.display.flip()
        end_time = time.time()
        if verbose:
            print("mandelbrot, palette:{}, iterations:{}, real:{} to {}, imag:{} "
                  "to {}, time: {}".format(
                                        palette_name, max_iter, round(min_re, 2), round(max_re, 2),
                                        round(min_im, 2), round(max_im, 2), round(end_time - start_time, 2)))

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
