import pygame
import random
import sys
import config


class Window:
    def __init__(self):
        pygame.init()
        # Set up some variables containing the screen size
        self.sizeX = 1200
        self.sizeY = 800

        if config.full_screen:
            self.window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)  # Create the pygame window
            self.sizeX = pygame.display.get_surface().get_size()[0]
            self.sizeY = pygame.display.get_surface().get_size()[1]
        else:
            self.window = pygame.display.set_mode([self.sizeX, self.sizeY])  # Create the pygame window

        self.halfX = int(self.sizeX / 2)
        self.halfY = int(self.sizeY / 2)
        self.clock = pygame.time.Clock()  # Create the clock object
        pygame.display.set_caption("Pretty Math")  # Put a name on the window.
        self.screen_update = 50
        self.screen_update_counter = 1

    def point(self, x, y, color):
        self.window.set_at((x, y), color)

    def clear(self):
        self.window.fill((0, 0, 0))


def close_window():
    pygame.quit()
    sys.exit()


def get_palette(name=""):
    c = -1
    if name == "":
        c = random.randint(0, 8)
    else:
        name = str.lower(name)
    searchable_color_names = ("red", "green", "blue", "orange", "yellow", "pink", "purple", "dark", "light", "gray",
                              "sea", "gold", "brown", "medium", "orchid", "brick", "turquoise", "white", "olive")
    color_palette = []
    if c == 0 or name == "fire":
        name = "Fire"
        color_palette = ["red", "orange", "yellow", "darkred"]
    elif c == 1 or name == "rgb":
        name = "RGB"
        color_palette = ["blue", "red", "green"]
    elif c == 2 or name == "rb":
        name = "Red/Blue"
        color_palette = ["red", "blue"]
    elif c == 3 or name == "rainbow":
        name = "Rainbow"
        color_palette = ["red", "orange", "yellow", "green", "blue", "blueviolet", "violet"]
    elif c == 4 or name == "primary":
        name = "Primary"
        color_palette = ["red", "yellow", "blue"]
    elif c == 5 or name == "bg":
        name = "Blue and Gray"
        color_palette = ["blue", "darkgray"]
    elif c == 6 or name == "random":
        name = "Random"
        for i in range(10):
            color_palette.append(random.choice(list(pygame.color.THECOLORS)))
    elif c == 7 or name == "complementary":
        name = "Complementary"
        c2 = random.randint(0, 3)
        if c2 == 0:
            color_palette = ['yellow', 'violet']
        elif c2 == 1:
            color_palette = ['green', 'red']
        else:
            color_palette = ['blue', 'orange']
    else:
        if not name or name == "search":
            name = random.choice(searchable_color_names)
        for i in pygame.color.THECOLORS:
            if name in i:
                color_palette.append(i)
    '''If for some reason our palette is still empty, ie, searched for a string not in THECOLORS,
        then choose something and build a palette'''
    if not len(color_palette):
        name = random.choice(searchable_color_names)
        for i in pygame.color.THECOLORS:
            if name in i:
                color_palette.append(i)
    return color_palette, str.capitalize(name)


def get_color_from_palette(palette_choice):
    ret_color = (pygame.color.Color(random.choice(palette_choice)))
    return ret_color


def color_fade_from_palette(base_color, next_color, step, number_of_steps):
    current_color = [x + (((y - x) / number_of_steps) * step) for x, y in
                     zip(pygame.color.Color(base_color), pygame.color.Color(next_color))]
    return current_color
