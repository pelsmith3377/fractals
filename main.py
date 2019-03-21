import screen_utils
import config
import pygame
import random
import sys
from lines import lines
from spiro import spiro
# from kaleidoscope import *
from biomorph import biomorph
from hopalong import hopalong
from ifs import ifs
from newton import newton
from mandelbrot import mandelbrot
from lorenz import lorenz
from novaretti import novaretti
from flame import flame
from orbit import orbit


def main():
    screen = screen_utils.Window()
    if config.verbose:
        print(pygame.display.get_surface().get_size())
    running = True
    while running:
        if config.testing:
            orbit(screen)
        else:
            x = random.randint(0, 10)
            if x == 0:
                mandelbrot(screen, 40)
            elif x == 1:
                flame(screen, 15)
            elif x == 2:
                ifs(screen)
            elif x == 3:
                # stalks(screen)
                novaretti(screen, 5)
            elif x == 4:
                lorenz(screen)
            elif x == 5:
                for _ in range(5):
                    spiro(screen)
            elif x == 6:
                lines(screen)
            elif x == 7:
                for _ in range(3):
                    hopalong(screen)
            elif x == 8:
                newton(screen)
            elif x == 9:
                for _ in range(10):
                    biomorph(screen)
            else:
                flame(screen, 5)

        # screen.clock.tick(1)

        # kaleidoscope(screen)


if __name__ == "__main__":
    main()
