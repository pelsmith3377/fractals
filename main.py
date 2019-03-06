import screen_utils
import config
import pygame
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
from stalks import stalks


def main():
    screen = screen_utils.Window()
    if config.verbose:
        print(pygame.display.get_surface().get_size())
    running = True
    while running:
        # stalks(screen)
        flame(screen, 5)

        novaretti(screen, 5)

        lorenz(screen)

        for _ in range(5):
            spiro(screen)

        lines(screen)

        for _ in range(3):
            hopalong(screen)

        ifs(screen)

        newton(screen)

        for _ in range(3):
            biomorph(screen)

        mandelbrot(screen, 10)
        # screen.clock.tick(1)

        # kaleidoscope(screen)


if __name__ == "__main__":
    main()
