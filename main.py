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
    fractal_favored = ["mandelbrot", "flame", "ifs", "novaretti", "lorenz", "spiro", "lines", "hopalong", "biomorph",
                       "newton"]
    fractal_out_of_favor = ["orbit"]
    while running:
        if config.testing:
            mandelbrot(screen, 4)
        else:
            x = random.choice(fractal_favored)
            if x == "mandelbrot":
                mandelbrot(screen, 4)
            elif x == "flame":
                flame(screen, 1)
            elif x == "ifs":
                ifs(screen)
            elif x == "orbit":
                orbit(screen)
            elif x == "novaretti":
                novaretti(screen, 1)
            elif x == "lorenz":
                lorenz(screen)
            elif x == "spiro":
                for _ in range(1):
                    spiro(screen)
            elif x == "lines":
                lines(screen)
            elif x == "hopalong":
                for _ in range(1):
                    hopalong(screen)
            elif x == "newton":
                newton(screen)
            elif x == "biomorph":
                for _ in range(1):
                    biomorph(screen)
            elif x == "flame":
                flame(screen, 1)
            else:
                flame(screen, 1)

        # screen.clock.tick(1)
        screen.clear()
        # kaleidoscope(screen)


if __name__ == "__main__":
    main()
