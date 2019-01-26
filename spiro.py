import pygame
# import random
import math
import itertools
import random
import screen_utils
import config


def spiro(screen):
    testing = config.testing
    verbose = config.verbose
    # colors = itertools.cycle(['green', 'blue', 'purple', 'pink', 'red', 'orange'])
    ''' Number of spirographs to draw before returning to main'''
    spiro_lifespan = 10
    ''' Amount of line segments to draw per spirograph before clearing the screen
        and starting over.'''
    spiro_cycles = 35000
    '''Clear the screen every other spirograph. (Allow 2 on screen at one time'''
    # every_other = True

    # for _ in range(spiro_lifespan):
    palette, palette_name = screen_utils.get_palette()
    colors = itertools.cycle(palette)
    base_color = next(colors)
    next_color = next(colors)
    current_color = pygame.color.Color(base_color)
    steps_till_color_change = random.randint(100, int(spiro_cycles / 3))
    step = 1
    '''
     k and l are numbers between 0 and 1. :)
     k is the ratio of the distance of the small circle from the big circle
     l is the ratio of the small circles radius (to the hole with the pen in)
     to the distance from the centre of the large circle.
    '''
    max_j = 1
    max_k = 2
    j = round(random.uniform(0.2, max_j), 3)
    k = round(random.uniform(0.2, max_k), 3)
    # j = .999
    # k = 1.999
    mid_width = int(screen.sizeX / 2)
    mid_height = int(screen.sizeY / 2)
    '''Do some scaling to make sure the spiro fits in the screen.  I tried to come up with a more
        elegant solution, for perfect scaling, but math.'''
    if screen.sizeX <= screen.sizeY:
        radius = mid_width
    else:
        radius = mid_height
    if j + k > 2.5:
        radius = radius - 260
    elif j + k > 2:
        radius = radius - 200
    elif j + k > 1.5:
        radius = radius - 100
    elif j + k > 1:
        radius = radius - 50
    # j = 0.4
    # k = 1.256
    # k = abs(2 - j)
    i = 0
    x = 0
    y = 0
    if testing:
        print("step=%i" % step + ",l=%f" % j + ",k=%f" % k)
    if verbose:
        print("palette={}, color change at {}, j={}, k={}".format(palette_name, steps_till_color_change, j, k))
    running = True
    for _ in range(spiro_cycles):
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
        # clock.tick(2000)
        pygame.display.flip()
    #if every_other:
    screen.clear()
    # every_other = not every_other
    #     every_other = False
    # else:
    #     every_other = True
    # screen.clear()
    return running
