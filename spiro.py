"""
Of all the python programs to draw spirographs, it seems I started out with the code from here:
https://huffton.wordpress.com/2012/07/04/raspberry-pi-python-introduction-part-3-sharing-nicely/

It's hard for me to tell, since this is one of the first modules I played with when teaching myself
python after many years away from programming.  It has been heavily modified (probably for the worse),
but still, credit to the author for the logic that ultimately makes the spirograph.
"""

import pygame
import math
import itertools
import random
import screen_utils
import config


def spiro(screen):
    testing = config.testing
    verbose = config.verbose
    ''' Amount of line segments to draw per spirograph before clearing the screen
        and starting over.'''
    spiro_cycles = 35000
    palette, palette_name = screen_utils.get_palette()
    colors = itertools.cycle(palette)
    base_color = next(colors)
    next_color = next(colors)
    current_color = pygame.color.Color(base_color)
    steps_till_color_change = random.randint(100, int(spiro_cycles / 3))
    step = 1
    '''
     k is the ratio of the distance of the small circle from the big circle
     j is the ratio of the small circles radius (to the hole with the pen in)
     to the distance from the centre of the large circle.
    '''
    max_j = 1
    max_k = 2
    if testing:
        j = .99
        k = 1.911
    else:
        j = round(random.uniform(0.2, max_j), 2)
        k = round(random.uniform(0.2, max_k), 3)
    mid_width = int(screen.sizeX / 2)
    mid_height = int(screen.sizeY / 2)
    '''Do some scaling to make sure the spiro fits in the screen.  I tried to come up with a more
        elegant solution, for perfect scaling, but math.'''
    if screen.sizeX <= screen.sizeY:
        radius = mid_width
    else:
        radius = mid_height
    if j + k > 2.5:
        radius = radius / 3
    elif j + k > 2:
        radius = radius / 2
    i = 0
    x = 0
    y = 0
    if testing:
        print("step=%i" % step + ",l=%f" % j + ",k=%f" % k)
    if verbose:
        print("Spiro: palette={}, color change at {}, j={}, k={}".format(palette_name, steps_till_color_change, j, k))
    running = True
    screen.clear()
    for _ in range(spiro_cycles):
        screen_utils.check_event()
        t = math.radians(i)
        new_x = radius * ((1 - k) * math.cos(t) + j * k * math.cos((1 - k) * t / k))
        new_y = radius * ((1 - k) * math.sin(t) - j * k * math.sin((1 - k) * t / k))
        '''If starting the first loop, don't draw a line from 0,0 to the first point.'''
        if x == 0 and y == 0:
            pass
        else:
            pygame.draw.line(screen.window, current_color, (x + mid_width, y + mid_height),
                             (new_x + mid_width, new_y + mid_height), 2)
        x = new_x
        y = new_y
        i += 1  # this is how far the points jump
        step += 1
        if step < steps_till_color_change:
            current_color = screen_utils.color_fade_from_palette(base_color, next_color, step, steps_till_color_change)
        else:
            step = 1
            base_color = next_color
            next_color = next(colors)
        pygame.display.flip()
    screen.clear()
    return running
