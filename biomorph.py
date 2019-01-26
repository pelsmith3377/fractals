import math
import pygame
import screen_utils
import config


def biomorph(screen):
    running = True
    width = screen.sizeX
    height = screen.sizeY
    c = complex(0, 0)
    z = complex(0, 0)
    min_re = -2.5
    max_re = 1
    min_im = -1
    max_im = 1
    re_factor = (max_re - min_re) / (width - 1)
    im_factor = (max_im - min_im) / (height - 1)
    max_iter = 35

    for x in range(width):
        for y in range(height):
            zx = x * re_factor
            zy = y * im_factor
            c = complex(zx, zy)
            # x = zx
            # y = zy
            trap_distance = 1000000
            iteration = 0
            while (zx * zx + zy * zy) < 4 and iteration < max_iter:
                z = complex(zx, zy)
                z = z * z
                z += c
                distance_to_x = abs(z.real)
            print(z)
            input()
    return running
