"""
Most of these functions are from https://github.com/ActiveState/code
"""

import random
import pygame
import math
import screen_utils
import config
import time
import cmath


def fern(screen, current_color, iterations=10000):
    # fern_size_x = random.randint(30, 100)
    # fern_size_y = random.randint(30, 100)
    # fern_x = random.randint(0, screen.sizeX - fern_size_x)
    # fern_y = random.randint(0, screen.sizeY)
    fern_x = screen.sizeX
    fern_y = screen.sizeY
    update_counter = 0

    # Fractint IFS definition of Fern
    mat = [[0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01],
           [0.85, 0.04, -0.04, 0.85, 0.0, 1.6, 0.85],
           [0.2, -0.26, 0.23, 0.22, 0.0, 1.6, 0.07],
           [-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07]]

    xa = -5.5
    xb = 6.5
    ya = -0.5
    yb = 10.5
    x = 0.0
    y = 0.0
    # for k in range(fern_x * fern_y):
    for k in range(iterations):
        screen_utils.check_event(screen)
        p = random.random()
        if p <= mat[0][6]:
            i = 0
        elif p <= mat[0][6] + mat[1][6]:
            i = 1
        elif p <= mat[0][6] + mat[1][6] + mat[2][6]:
            i = 2
        else:
            i = 3

        x0 = x * mat[i][0] + y * mat[i][1] + mat[i][4]
        y = x * mat[i][2] + y * mat[i][3] + mat[i][5]
        x = x0
        jx = int((x - xa) / (xb - xa) * (fern_x - 1))
        jy = (fern_y - 1) - int((y - ya) / (yb - ya) * (fern_y - 1))
        screen.point(jx, jy, current_color)
        update_counter += 1
        if update_counter >= 50:
            pygame.display.flip()
            update_counter = 0


def triangle(x0, y0, x1, y1, x2, y2, screen, current_color):
    a = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    b = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    c = math.sqrt((x0 - x2) ** 2 + (y0 - y2) ** 2)
    if (a < 2) or (b < 2) or (c < 2):
        return
    x3 = (x0 + x1) / 2
    y3 = (y0 + y1) / 2
    x4 = (x1 + x2) / 2
    y4 = (y1 + y2) / 2
    x5 = (x2 + x0) / 2
    y5 = (y2 + y0) / 2

    pygame.draw.line(screen.window, current_color, (int(x3), int(y3)), (int(x4), int(y4)))
    # pygame.draw.line(screen.window, [0, 255, 0], (int(x4), int(y4)), (int(x5), int(y5)))
    # pygame.draw.line(screen.window, [0, 0, 255], (int(x5), int(y5)), (int(x3), int(y3)))
    triangle(x0, y0, x3, y3, x5, y5, screen, current_color)
    triangle(x3, y3, x1, y1, x4, y4, screen, current_color)
    triangle(x5, y5, x4, y4, x2, y2, screen, current_color)
    screen_utils.check_event(screen)
    pygame.display.flip()


def snowflake(ax, ay, bx, by, screen, current_color):
    f = math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)
    if f < 1:
        return
    f3 = f / 3
    cs = (bx - ax) / f
    sn = (by - ay) / f
    cx = ax + cs * f3
    cy = ay + sn * f3
    h = f3 * math.sqrt(3) / 2
    dx = (ax + bx) / 2 + sn * h
    dy = (ay + by) / 2 - cs * h
    ex = bx - cs * f3
    ey = by - sn * f3
    triangle(cx, cy, dx, dy, ex, ey, screen, current_color)
    snowflake(ax, ay, cx, cy, screen, current_color)
    snowflake(cx, cy, dx, dy, screen, current_color)
    snowflake(dx, dy, ex, ey, screen, current_color)
    snowflake(ex, ey, bx, by, screen, current_color)
    screen_utils.check_event(screen)


def koch(screen, current_color):
    imgx = screen.sizeX
    imgy = screen.sizeY
    # imgx = 512
    # imgy = 512
    mx2 = imgx / 2
    my2 = imgy / 2
    r = my2
    a = 2 * math.pi / 3
    for k in range(3):
        x0 = mx2 + r * math.cos(a * k)
        y0 = my2 + r * math.sin(a * k)
        x1 = mx2 + r * math.cos(a * (k + 1))
        y1 = my2 + r * math.sin(a * (k + 1))
        snowflake(x0, y0, x1, y1, screen, current_color)

    x2 = mx2 + r * math.cos(a)
    y2 = my2 + r * math.sin(a)
    triangle(x0, y0, x1, y1, x2, y2, screen, current_color)


def percolate(screen):
    imgx = 512
    imgy = 512
    maxIt = int(imgx * imgy / 1.25)
    for i in range(maxIt):
        x = random.randint(0, imgx - 1)
        y = random.randint(0, imgy - 1)
        r = random.randint(1, 255)
        g = random.randint(1, 255)
        b = random.randint(1, 255)
        r2 = random.randint(1, 255)
        g2 = random.randint(1, 255)
        b2 = random.randint(1, 255)
        screen.point(x, y, [r, g, b])
        # image.putpixel((x, y), (r, g, b))
        # ImageDraw.floodfill(image, (x, y), (r2, g2, b2), (0, 0, 0))


# Random Spiral IFS Fractals
# FB - 20130928
def spiral(screen, current_color):
    running = True
    # current_color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    update_counter = 0
    imgx = screen.sizeX
    imgy = screen.sizeY
    maxIt = imgx * imgy
    maxIt = 300000
    n = random.randint(2, 9)
    a = 2.0 * math.pi / n
    t = 2.0 * math.pi * random.random() # rotation angle of central copy
    ts = math.sin(t)
    tc = math.cos(t)
    r1 = 0.2 * random.random() + 0.1 # scale factor of outmost copies on the spiral arms
    r0 = 1.0 - r1  # scale factor of central copy
    p0 = r0 ** 2.0 / (n * r1 ** 2.0 + r0 ** 2.0) # probability of central copy
    x = 0.0; y = 0.0
    for i in range(maxIt):
        screen_utils.check_event(screen)
        if random.random() < p0:  # central copy
            x *= r0
            y *= r0 # scaling
            # rotation
            h = x * tc - y * ts
            y = x * ts + y * tc
            x = h
        else: # outmost copies on the spiral arms
            k = random.randint(0, n - 1) # select an arm
            c = k * a  # angle
            # scaling and translation
            x = x * r1 + math.cos(c)
            y = y * r1 + math.sin(c)
        kx = int((x + 2.0) / 4.0 * (imgx - 1))
        ky = int((y + 2.0) / 4.0 * (imgy - 1))
        screen.point(kx, ky, current_color)
        if update_counter >= 40:
            pygame.display.flip()
            update_counter = 0
        else:
            update_counter += 1
    return running


def popcorn(screen, palette):
    base_color = random.choice(palette)
    next_color = random.choice(palette)
    max_iter = random.randint(20, 60)
    h = random.uniform(0.01, 0.1)
    tan_factor = random.uniform(0.1, 4)
    wxmin = -4.0
    wxmax = 4.0
    wymin = -3.0
    wymax = 3.0
    wwid = (wxmax - wxmin)
    whgt = (wymax - wymin)
    dxmin = 0
    dxmax = screen.sizeX
    dymin = 0
    dymax = screen.sizeY
    dwid = (dxmax - dxmin)
    dhgt = (dymax - dymin)

    x_step = 10
    y_step = 10


    zoom = 1
    for x in range(0, screen.sizeX, x_step):
        for y in range(0, screen.sizeY, y_step):
            wx = wxmin + wwid * (x - dxmin) / dwid
            wy = wymin + whgt * (y - dymin) / dhgt
            for i in range(max_iter):
                screen_utils.check_event(screen)
                newx = wx - h * math.sin(wy + math.tan(tan_factor * wy))
                newy = wy - h * math.sin(wx + math.tan(tan_factor * wx))
                wx, wy = newx, newy
                dx = int(dxmin + dwid * (wx - wxmin) / wwid)
                dy = int(dymin + dhgt * (wy - wymin) / whgt)
                if (0 <= dx < dxmax) and (0 <= dy < dymax):
                    current_color = screen_utils.color_fade_from_palette(base_color, next_color, i, max_iter)
                    screen.point(dx, dy, current_color)

                #print_screen(wx, wy, "--", newx, newy, "-----", dx, dy)
            pygame.display.flip()


# Apollonian Gasket Fractal using IFS
# FB - 20120114
def gasket(screen, current_color):
    maxIt = 500000  # of iterations
    imgx = screen.sizeX
    imgy = screen.sizeY

    s = math.sqrt(3.0)

    def f(z):
        return 3.0 / (1.0 + s - z) - (1.0 + s) / (2.0 + s)
    iterated_function_system = ["f(z)", "f(z) * complex(-1.0, s) / 2.0", "f(z) * complex(-1.0, -s) / 2.0"]

    xa = -0.6
    xb = 0.9
    ya = -0.75
    yb = 0.75

    z = complex(0.0, 0.0)
    for i in range(maxIt):
        screen_utils.check_event(screen)
        z = eval(iterated_function_system[random.randint(0, 2)])
        kx = int((z.real - xa) / (xb - xa) * (imgx - 1))
        ky = int((z.imag - ya) / (yb - ya) * (imgy - 1))
        if kx >=0 and kx < imgx and ky >= 0 and ky < imgy:
            # image.putpixel((kx, ky), (255, 255, 255))
            screen.point(kx, ky, current_color)
            if i % 50 == 0:
                pygame.display.flip()


def ifs(screen):
    running = True
    if config.testing:
        choice = 3
    else:
        choice = random.randint(0, 4)
    screen.clear()
    palette, palette_name = screen_utils.get_palette()
    if config.verbose:
        print("IFS, Palette:{}".format(palette_name))
    current_color = screen_utils.get_color_from_palette(palette)

    if choice == 0:
        spiral(screen, current_color)
    elif choice == 1:
        fern(screen, current_color, 1000000)
        current_color = screen_utils.get_color_from_palette(palette)
        fern(screen, current_color, 200000)
    elif choice == 2:
        for _ in range(10):
            palette, palette_name = screen_utils.get_palette()
            if config.verbose:
                print("Popcorn - Palette:{}".format(palette_name))
            popcorn(screen, palette)
            time.sleep(2)
            screen.clear()
    elif choice == 3:
        gasket(screen, current_color)
    else:
        koch(screen, current_color)
    time.sleep(4)
    screen.clear()
    return running
