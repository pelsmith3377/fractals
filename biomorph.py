'''
    Much thanks to Mad Teddy at http://www.madteddy.com/biomorph.htm
'''

import pygame
import random
import screen_utils
import config
import math
import time
from numba import jit


@jit
def cosz(x, y, c_re, c_im):
    # Just plain slow.  jit will do the best it can
    xx = math.cos(x) * (math.e ** y + math.e ** -y) / 2
    yy = -(math.sin(x) * (math.e ** y - math.e ** -y) / 2)
    x = xx + c_re
    y = yy + c_im
    return x, y


def biomorph(screen):
    running = True
    width = screen.sizeX
    height = screen.sizeY
    aspect_ratio = width / height
    y_max = 2.5
    y_min = -y_max
    x_max = y_max * aspect_ratio
    x_min = -x_max
    if config.testing:
        # c_re = 1.5
        # c_im = -1.2
        c_re = 0
        c_im = 0
        color_scheme = 7
        bio_type = 8
    else:
        c_re = random.uniform(-2, 2)
        c_im = random.uniform(-2, 2)
        color_scheme = random.randint(0, 6)
        bio_type = random.randint(0, 10)
        # bio_type = 8
        if bio_type == 8:
            y_max = random.uniform(0.5, 8)
            y_max = round(y_max, 2)
            print(y_max)
            y_min = -y_max
            x_max = y_max * aspect_ratio
            x_min = -x_max

    max_iter = 40
    ilimit = height - 1
    jlimit = width - 1

    bio_name = ""
    ran_shift = random.randint(1, 21)  # You're better off not knowing

    '''One of the choices just does a modulo of the r/g/b components'''
    red = random.randint(50, 255)
    green = random.randint(50, 255)
    blue = random.randint(50, 255)
    '''Get a palette if needed.'''
    palette, palette_name = screen_utils.get_palette("search")
    # random_color = screen_utils.get_random_color()
    # random_color2 = screen_utils.get_random_color()
    random_color = palette[0]
    random_color2 = palette[1]

    start_time = time.time()
    for i in range(ilimit):
        for j in range(jlimit):
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

            x0 = x_min + (x_max - x_min) * j / jlimit
            y0 = -y_min - (y_max - y_min) * i / ilimit
            x = x0
            y = y0
            for n in range(max_iter):
                if bio_type == 0:
                    bio_name = "z^3, type 1"
                    xx = x * (x * x - 3 * y * y) + c_re
                    yy = y * (3 * x * x - y * y) + c_im
                    x = xx
                    y = yy
                elif bio_type == 1:
                    bio_name = "z^3, type 2"
                    xx = x * (x * x - 3 * y * y)
                    yy = y * (3 * x * x - y * y)
                    x = xx + c_re
                    y = yy + c_im
                elif bio_type == 2:
                    bio_name = "z^2, type 1"
                    xx = x * x - y * y + c_re
                    yy = 2 * x * y + c_im
                    x = xx
                    y = yy
                elif bio_type == 3:
                    bio_name = "z^2, type 2"
                    xx = x * x - y * y
                    yy = 2 * x * y
                    x = xx + c_re
                    y = yy + c_im
                elif bio_type == 4:
                    bio_name = "z^4, type 1"
                    xx = (x**4 - 6 * x**2 * y**2 + y**4) + c_re
                    yy = (4 * x * y * (x**2 - y**2)) + c_im
                    x = xx
                    y = yy
                elif bio_type == 5:
                    bio_name = "z^4, type 2"
                    xx = x**4 - 6 * x**2 * y**2 + y**4
                    yy = 4 * x * y * (x**2 - y**2)
                    x = xx + c_re
                    y = yy + c_im
                elif bio_type == 6:
                    bio_name = "z^5, type 1"
                    xx = (x**5 - 10 * x**3 * y**2 + 5 * x * y**4) + c_re
                    yy = (5 * x**4 * y - 10 * x**2 * y**3 + y**5) + c_im
                    x = xx
                    y = yy
                elif bio_type == 7:
                    bio_name = "z^5, type 2"
                    xx = x**5 - 10 * x**3 * y**2 + 5 * x * y**4
                    yy = 5 * x**4 * y - 10 * x**2 * y**3 + y**5
                    x = xx + c_re
                    y = yy + c_im
                elif bio_type == 8:
                    bio_name = "cos(z)"
                    # xx = math.cos(x) * (math.e**y + math.e**-y) / 2
                    # yy = -(math.sin(x) * (math.e**y - math.e**-y) / 2)
                    # x = xx + c_re
                    # y = yy + c_im
                    x, y = cosz(x, y, c_re, c_im)
                else:
                    bio_name = "z^7, type 2"
                    xx = x**7 - 21 * x**5 * y**2 + 35 * x**3 * y**4 - 7 * x * y**6
                    yy = 7 * x**6 * y - 35 * x**4 * y**3 + 21 * x**2 * y**5 - y**7
                    x = xx + c_re
                    y = yy + c_im
                if abs(x) > 10 or abs(y) > 10 or x * x + y * y > 100:
                    break

            if color_scheme == 0:
                n = int(abs(x)) % 255
                palette_name = "dark modulo"
                current_color = [red % (n + 1), green % (n + 1), blue % (n + 1)]
            elif color_scheme == 1:
                n = int(abs(x)) % max_iter
                palette_name = "fade"
                current_color = screen_utils.color_fade_from_palette("black", random_color, n, max_iter)
            elif color_scheme == 2:
                palette_name = "Raw x"
                color = abs(int(x))
                current_color = color
            elif color_scheme == 3:
                palette_name = "Woot{}".format(ran_shift)
                color = abs(int(x))
                current_color = (color << ran_shift) % 16581374
            elif color_scheme == 4:
                palette_name = "Mad Teddy's"
                if abs(x) < 10 and abs(y) < 10:
                    current_color = pygame.Color('yellow')
                elif abs(x) >= 10 and abs(y) < 10:
                    current_color = pygame.Color('red')
                elif abs(x) < 10 and abs(y) >= 10:
                    current_color = pygame.Color('green')
                else:
                    current_color = pygame.Color('black')
            elif color_scheme == 5:
                palette_name = palette_name  # 4 colors from previously chosen palette
                if abs(x) < 10 and abs(y) < 10:
                    current_color = pygame.Color(palette[0])
                elif abs(x) >= 10 and abs(y) < 10:
                    current_color = pygame.Color(palette[1])
                elif abs(x) < 10 and abs(y) >= 10:
                    current_color = pygame.Color(palette[2])
                else:
                    current_color = pygame.Color(palette[3])
            # if color_scheme == 0:
            #     n = int(abs(x)) % 1000
            #     palette_name = "bit shift"
            #     current_color = (n << 21) + (n << 10) + n * 8
            # elif color_scheme == 1:
            #     n = int(abs(x)) % 1000
            #     palette_name = "modulo"
            #     current_color = n % 4 * 64, n % 8 * 32, n % 16 * 16
            # elif color_scheme == 4:  # ugly
            #     palette_name = palette_name
            #     n = int(abs(x))
            #     current_color = pygame.color.Color(palette[n % len(palette)])
            else:
                palette_name = "black and white"
                if abs(x) < 10 or abs(y) < 10:
                    current_color = [0, 0, 0]
                else:
                    current_color = [200, 200, 200]

            screen.point(j, i, current_color)
    end_time = time.time()
    if config.verbose:
        elapsed_time = end_time - start_time
        print('Palette={}, C={}+{}i, biomorph type:{}, elapsed time={}'.format(palette_name, c_re, c_im,
                                                                               bio_name, elapsed_time))

    pygame.display.flip()
    screen.clock.tick(1)
    return running
