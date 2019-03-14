import pygame
import random
import sys
import config
import os


class Window:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
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
        pygame.display.set_caption("Fractals")  # Put a name on the window.
        self.screen_update = 50
        self.screen_update_counter = 1

    def point(self, x, y, color):
        self.window.set_at((x, y), color)

    def clear(self):
        self.window.fill((0, 0, 0))


def check_event():
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_window()
            running = False
        elif event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_SPACE:
            #     screen.clear()
            #     return running
            if event.key == pygame.K_ESCAPE:
                close_window()
                running = False
    return running


def close_window():
    pygame.quit()
    sys.exit()


def get_palette(name=""):
    c = -1
    if name == "":
        c = random.randint(0, 6)
    else:
        name = str.lower(name)
    searchable_color_names = ("red", "green", "blue", "orange", "yellow", "pink", "purple", "dark", "light",
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
    # print("Palette was empty!  Making random palette.")
    if not len(color_palette):
        name = random.choice(searchable_color_names)
        for i in pygame.color.THECOLORS:
            if name in i:
                color_palette.append(i)
    return color_palette, str.capitalize(name)


def get_random_color(value="random"):
    r = random.randint(1, 254)
    g = random.randint(1, 254)
    b = random.randint(1, 254)

    if value == "random":
        # ret_color = random.choice(list(pygame.color.THECOLORS))
        ret_color = [r, g, b]
    elif value == "dark":
        ret_color = [random.randint(0, 122), random.randint(0, 122), random.randint(0, 122)]
    elif value == "light":
        ret_color = [random.randint(166, 255), random.randint(166, 255), random.randint(166, 255)]
        # ret_color = [(r+50) % 255, (g+50) % 255, (b+50) % 255]
    else:
        ret_color = [random.randint(20, 255), random.randint(20, 255), random.randint(20, 255)]
    return ret_color


def get_color_from_palette(palette_choice):
    ret_color = (pygame.color.Color(random.choice(palette_choice)))
    return ret_color


def color_fade_from_palette(base_color, next_color, step, number_of_steps):
    try:
        if type(base_color) == str:
            base_color = pygame.color.Color(base_color)
        if type(next_color) == str:
            next_color = pygame.color.Color(next_color)
        current_color = [x + (((y - x) / number_of_steps) * step) for x, y in
                         zip(base_color, next_color)]
        # zip(pygame.color.Color(base_color), pygame.color.Color(next_color))]
    except ValueError:
        print("ValueError in color_face_from_palette.  Returning 'white'")
        current_color = [255, 255, 255]
    return current_color
