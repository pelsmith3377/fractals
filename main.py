from hopalong import *
from screen_utils import *
from lines import *
from spiro import *
#from sine import *
from mandelbrot import *


def main():
    screen = Window()
    if config.verbose:
        print(pygame.display.get_surface().get_size())
    running = True
    while running:
        running = mandelbrot(screen)
        running = spiro(screen)
        running = lines(screen)
        running = hopalong(screen)
        # running = sine_wave(screen)
    close_window()


if __name__ == "__main__":
    main()
