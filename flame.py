"""
Starting with https://github.com/theepicsnail/FlameFractal/blob/master/ff.py
then adding more variations from https://flam3.com/flame_draves.pdf
"""
import pygame
from math import sin, cos, tan, atan, sqrt, atan2, pi, e
import random
import screen_utils
import config
from numba import jit


def coord2px(x, y, screen):
    val = 5
    x += val
    x /= val * 2 * 4 / 3
    y += val
    y /= val * 2

    x *= screen.sizeX
    y *= screen.sizeY
    x = int(x)
    y = int(y)
    if 0 > x or screen.sizeX <= x:
        return None, None

    if 0 > y or screen.sizeY <= y:
        return None, None
    return x, y


def get_color(x, y, screen):
    x, y = coord2px(x, y, screen)
    if x is None:
        return 0, 0, 0
    return screen.window.get_at((x, y))


def set_color(x, y, c, screen):
    x, y = coord2px(x, y, screen)
    if x is None:
        return
    screen.window.set_at((x, y), c)


def join_colors(c1, c2):
    current_color = [((x + y) / 2) for x, y in
                     zip(c1, c2)]
    return current_color


def gen_coefficients():
    mi = 0.1
    ma = 1
    rnd = 2
    # return random.random(), random.random(), random.random(), \
    #        random.random(), random.random(), random.random()
    return round(random.uniform(mi, ma), rnd), round(random.uniform(mi, ma), rnd), round(random.uniform(mi, ma), rnd), \
           round(random.uniform(mi, ma), rnd), round(random.uniform(mi, ma), rnd), round(random.uniform(mi, ma), rnd)


def rand_j(table):
    r = random.random()
    for j, v in enumerate(table):
        if r <= v[0]:
            return j
        r -= v[0]
    print("Error finding a J")
    return 0


@jit
def flame_function(j, x, y, v, table):
    # print j, table[j]
    a, b, c, d, e, f = table[j][1]
    out_x = 0
    out_y = 0
    for wk, vk in v:
        px, py = vk(a * x + b * y + c, d * x + e * y + f)
        out_x += wk * px
        out_y += wk * py
    return out_x, out_y


@jit
def r(x, y):
    r_out = sqrt(x * x + y * y)
    return r_out


def flame(screen, flame_lifespan=5):
    running = True
    # flame_lifespan = 5
    max_iter = 1000000
    flame_type = 0
    for span in range(flame_lifespan):
        seed = random.uniform(0.5, 1.2)
        v = []
        flame_name = ""
        flame_variations = ["linear", "sinusoidal", "spherical", "tangential", "swirl", "horseshoe", "polar",
                            "handkerchief", "heart", "disc", "diamond", "ex", "julia", "popcorn", "power"]
        flame_unused_variations = ["exponential"]
        if config.testing:
            num_combos = 2
        else:
            num_combos = random.randint(2, 3)
        for _ in range(num_combos):
            seed = random.uniform(0.5, 1.2)
            if config.testing:
                flame_var = "heart"
            else:
                flame_var = random.choice(flame_variations)
            if flame_var == "linear":
                v += [[seed, lambda x, y: (x, y)], ]
            elif flame_var == "sinusoidal":
                v += [[seed, lambda x, y: (sin(x), sin(y))], ]
            elif flame_var == "spherical":
                v += [[seed, lambda x, y: (x / float(x * x - y * y), y / float(x * x - y * y))], ]
            elif flame_var == "tangential":
                v += [[seed, lambda x, y: (tan(x), atan(y))], ]
            elif flame_var == "swirl":
                v += [[seed, lambda x, y: (x * sin(r(x, y) * r(x, y)) - y * cos(r(x, y) * r(x, y)),
                                           x * cos(r(x, y) * r(x, y)) + y * sin(r(x, y) * r(x, y)))], ]
            elif flame_var == "horseshoe":
                v += [[seed, lambda x, y: (1 / ((x - y) * (x + y) * r(x, y)), 2 * x * y * r(x, y))], ]
            elif flame_var == "polar":
                v += [[seed, lambda x, y: (atan2(x, y) * pi, r(x, y) - 1.0)]]
            elif flame_var == "handkerchief":
                v += [[seed, lambda x, y: (r(x, y) * sin(atan2(x, y) + r(x, y)), r(x, y) * cos(atan2(x, y) -
                                                                                               r(x, y)))], ]
            elif flame_var == "heart":
                aa = lambda x, y: atan2(x, y) * sqrt(x * x + y * y)
                v += [[seed, lambda x, y: (r(x, y) * sin(aa(x, y)), -r(x, y) * cos(aa(x, y)))], ]
            elif flame_var == "disc":
                a = lambda x, y: atan2(x * pi, y * pi) / pi
                v += [[seed, lambda x, y: (sin(r(x, y)) * a(x, y), cos(r(x, y)) * a(x, y))], ]
            elif flame_var == "diamond":
                v += [[seed, lambda x, y: (sin(atan2(x, y)) * cos(r(x, y)), cos(atan2(x, y)) * sin(r(x, y)))], ]
            elif flame_var == "ex":
                n0 = lambda x, y: sin(atan2(x, y) + r(x, y))
                n1 = lambda x, y: cos(atan2(x, y) - r(x, y))
                m0 = lambda x, y: r(x, y) * n0(x, y)**3
                m1 = lambda x, y: r(x, y) * n1(x, y)**3
                v += [[seed, lambda x, y: (m0(x, y) + m1(x, y), m0(x, y) - m1(x, y))], ]
            elif flame_var == "julia":
                aa = lambda x, y: atan2(x, y) / 2
                a3 = lambda x, y: aa(x, y) + pi if random.randint(0, 1) else aa(x, y)
                rr = lambda x, y: (x * x + y * y)**0.25
                v += [[seed, lambda x, y: (rr(x, y) * cos(a3(x, y)), rr(x, y) * sin(a3(x, y)))], ]
            elif flame_var == "popcorn":
                dy = lambda y: y + tan(10 * y)
                dx = lambda x: x + tan(10 * x)
                nx = lambda x: x - 0.05 * sin(dx(x))
                ny = lambda y: y - 0.05 * sin(dy(y))
                v += [[seed, lambda x, y: (nx(x), ny(y))], ]
            elif flame_var == "exponential":
                try:  # number too large exceptions - troubleshooting
                    dx = lambda x: e**(x - 1)
                except:
                    print("exception occurred")
                    dx = 30000
                dy = lambda y: pi * y
                v += [[seed, lambda x, y: (dx(x) * cos(dy(y)), dx(x) * sin(dy(y)))], ]
            elif flame_var == "power":
                v += [[seed, lambda x, y: (r(x, y)**sin(atan2(x, y)) * cos(atan2(x, y)),
                                           r(x, y)**sin(atan2(x, y)) * sin(atan2(x, y)))], ]
            else:  # how did we wind up here
                print("How did we wind up here? #2")
                flame_name = flame_name + "linear" + " "
                v += [[seed, lambda x, y: (x, y)], ]
            flame_name = flame_name + flame_var + " "
        table = [
            # p	  a	 b  c  d  e  f , color
            # swapped in a neon palette
            [.1, gen_coefficients(), (255, 175, 190)],
            [.1, gen_coefficients(), (230, 10, 150)],
            [.1, gen_coefficients(), (255, 240, 0)],
            [.1, gen_coefficients(), (25, 255, 70)],
            [.1, gen_coefficients(), (10, 165, 225)],
            [.1, gen_coefficients(), (155, 75, 160)],
            [.1, gen_coefficients(), (140, 200, 70)],
            [.1, gen_coefficients(), (215, 225, 65)],
            [.1, gen_coefficients(), (245, 130, 40)],
            [.1, gen_coefficients(), (210, 20, 70)],
            #
            # [.2, gen_coefficients(), (0, 255, 255)],
            # [.2, coefficients[1], (255, 0, 255)],
            # [.2, coefficients[2], (255, 255, 0)],
            # [.1, coefficients[3], (0, 0, 255)],
            # [.1, coefficients[4], (255, 0, 0)],
            # [.1, coefficients[5], (0, 255, 0)],
            # [.1, coefficients[6], (255, 255, 255)],
            #
        ]
        print("flame, type:{}, a:{}".format(flame_name, seed))
        for iterate in range(max_iter):

            px = random.random() * 2 - 1
            py = random.random() * 2 - 1
            pc = get_color(px, py, screen)
            for i in range(2):
                j = rand_j(table)
                px, py = flame_function(j, px, py, v, table)
                pc = join_colors(pc, table[j][2])
            c = join_colors(pc, get_color(px, py, screen))
            set_color(px, py, c, screen)
            screen_utils.check_event()
            if iterate % 5000 == 0:
                pygame.display.update()
        screen.clear()
        flame_type = (flame_type + 1) % 6
    return running

