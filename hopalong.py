import math
import screen_utils
import config
import random
import pygame


def get_hopalong_params(function):
    a = b = c = 10
    scale = 1
    if function == "Pelican":
        a = random.uniform(-10, 10)
        b = random.uniform(-10, 10)
        c = random.uniform(-10, 10)
        scale = random.uniform(3.5, 10)
    elif function == "Pelican2":
        a = random.uniform(-10, 100)
        b = random.uniform(-100, 100)
        c = random.uniform(-10, 10)
        scale = random.randint(1, 10)
    elif function == "Pelican3":
        a = random.uniform(-10, 10)
        b = random.uniform(-10, 10)
        c = random.uniform(-10, 10)
        scale = random.uniform(3.5, 10)
    elif function == "Gingerbread":
        a = random.uniform(0.8, 41.3)
        b = random.uniform(1, 1.2)
        c = random.uniform(0, 0.5)
        scale = 3.0
    elif function == "Martin1":
        a = random.uniform(40, 1540)
        b = random.uniform(3, 20)
        c = random.uniform(100, 3100)
        scale = 1.0
    elif function == "Martin2":
        a = random.uniform(3.0715927, 3.2115927)
        b = 0
        c = 0
        scale = 4.0
    elif function == "Martin3":  # 1,2,0,10
        a = random.uniform(0.7, 1.2)
        b = random.uniform(1.8, 2.2)
        # c = 0
        c = random.uniform(0, 3)
        scale = 10.0
    elif function == "Ejk1":
        a = random.uniform(0, 500)
        b = random.uniform(0, .4)  # warning: big numbers = infinity errors
        c = random.uniform(10, 110)
        scale = 1.0
    elif function == "Ejk2":
        a = random.uniform(0, 500)
        b = pow(10.0, 6.9)
        c = pow(10.0, 0.945)
        scale = 1.0
    elif function == "Ejk3":
        a = random.uniform(0, 50)
        b = random.uniform(10.35, 110.50)
        c = random.uniform(30, 110)
        scale = 1.2
    elif function == "Ejk4":
        a = random.uniform(0, 90)
        b = random.uniform(1, 10)
        c = random.uniform(30, 70)
        scale = random.uniform(0.1, 0.5)
    elif function == "Ejk5":  # warning, infinity errors possible if b > 1
        a = random.uniform(0, 600)
        b = random.uniform(0.5, 1)
        c = random.uniform(20, 110)
        scale = random.uniform(0.3, 1)
    elif function == "Ejk6":
        # a = random.uniform(550, 650)
        # b = random.uniform(0.5, 1.5)
        # c = 0
        # scale = 1.2
        a = random.uniform(1, 99)
        b = random.uniform(0.5, 11.5)
        c = 0
        scale = 1.2
    else:  # how did we wind up here?
        print("How did we wind up here? #1")
        a = 10
        b = 1
        c = 1
        scale = 1
    return a, b, c, scale, 0, 0


def hopalong(screen):
    testing = config.testing
    verbose = config.verbose
    # OG hop types = ("Martin1", "Martin2", "Ejk1", "Ejk2", "Ejk3", "Ejk4", "Ejk5", "Ejk6")
    # Weight toward choosing favorites.
    hop_favorites = ("Pelican", "Pelican3", "Martin1", "Ejk1", "Ejk2", "Ejk4")
    hop_not_favorites = ("Pelican2", "Martin2", "Martin3", "Ejk3", "Ejk5", "Gingerbread")
    hop_sucks = ("Ejk6")  # just plain ugly
    testing_counter = 0
    if testing:
        function = "Pelican3"
    else:
        favor_weight = random.randint(0, 1000)
        if favor_weight < 970:
            function = random.choice(hop_favorites)
        elif favor_weight < 998:
            function = random.choice(hop_not_favorites)
        else:
            function = random.choice(hop_sucks)
    a, b, c, scale, x, y = get_hopalong_params(function)
    palette_choice, palette_name = screen_utils.get_palette()
    active_color = screen_utils.get_color_from_palette(palette_choice)
    running = True
    xx = yy = 0
    start_over_counter = 160
    color_change = 40000
    if verbose:
        print("function = {}, palette = {}, a = {}, b = {}, c = {}, "
              "scale = {}".format(function, palette_name, a, b, c, scale))
    screen.clear()
    for step in range(start_over_counter):
        for i in range(color_change):  # change color once falls out
            screen_utils.check_event(screen)
            if function == "Pelican":  # my attempt at coding Martin1 from scratch...slightly different output
                if x > 0:
                    sign = 1
                elif x < 0:
                    sign = -1
                else:
                    sign = 0
                xx = y - sign * (abs(b * x - c)) ** 0.5
                yy = a - x
            elif function == "Pelican2":
                # c += random.uniform(-0.00001, 0.00001)
                if x > 0:
                    sign = 1
                elif x < 0:
                    sign = -1
                else:
                    sign = 0
                xx = y - sign * math.sin((abs(b * x - c)) ** 0.5)
                yy = a - x
            elif function == "Pelican3":  # positive Barry Martin
                if x > 0:
                    sign = 1
                elif x < 0:
                    sign = -1
                else:
                    sign = 0
                xx = y + sign * (abs(b * x - c)) ** 0.5
                yy = a - x
            elif function == "Gingerbread":
                xx = y + abs(b * x)
                yy = a - x
            elif function == "Martin1":
                if x < 0:
                    xx = y - math.sqrt(abs(b * x - c))
                else:
                    xx = y + math.sqrt(abs(b * x - c))
                yy = a - x
            elif function == "Martin2":
                xx = y - math.sin(x)
                yy = a - x
            elif function == "Martin3":  # additive Martin
                xx = y + math.sqrt(abs(b * x - c))
                yy = a - x
                '''Ejk1 causes infinity errors with b > 1'''
            elif function == "Ejk1":
                if x > 0:
                    xx = y - (b * x - c)
                else:
                    xx = y + (b * x - c)
                yy = a - x
            elif function == "Ejk2":
                if x < 0:
                    xx = y - math.log(abs(b * x - c))
                else:
                    xx = y + math.log(abs(b * x - c))
                yy = a - x
            elif function == "Ejk3":
                if x > 0:
                    xx = y - math.sin(b * x) - c  # + random_factor
                else:
                    xx = y + math.sin(b * x) - c
                yy = a - x
                # random_factor = random.random()
            elif function == "Ejk4":
                if x > 0:
                    xx = y - math.sin(b * x) - c
                else:
                    xx = y + math.sqrt(abs(b * x - c))
                yy = a - x
                '''This is another one prone to infinity errors if b > 1'''
            elif function == "Ejk5":
                if x > 0:
                    xx = y - math.sin(b * x) - c
                else:
                    xx = y + (b * x - c)
                yy = a - x
                # just plain ugly
            elif function == "Ejk6":
                fmod1 = math.modf(b*x)
                xx = y - math.asin(fmod1[0])
                yy = a - x
            x = xx
            y = yy
            if testing:
                testing_counter += 1
                if testing_counter >= 200000:
                    print("x = {}, y = {}".format(x, y))
                    testing_counter = 0
            '''making incremental changes to c causes some strange behavior.  It fuzzes up the screen
                and causes these weird hoops to occasionally develop.  It's also not really the 
                hopalong program anymore once you introduce this error.
            '''
            pointx = int(x * scale + screen.halfX)
            pointy = int(y * scale + screen.halfY)
            if 0 <= pointx <= screen.sizeX and 0 <= pointy <= screen.sizeY:
                screen.point(pointx, pointy, active_color)
                screen.screen_update_counter += 1
            # speed boost, only update the screen every screen_update points
            if screen.screen_update_counter >= screen.screen_update:
                pygame.display.flip()
                screen.screen_update_counter = 0
        active_color = screen_utils.get_color_from_palette(palette_choice)
    screen.clear()
    if verbose:
        print("function = {}, palette = {}, a = {}, b = {}, c = {}, "
              "scale = {}".format(function, palette_name, a, b, c, scale))
    return running

