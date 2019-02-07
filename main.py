from screen_utils import *
from lines import *
from spiro import *
# from kaleidoscope import *
from biomorph import *
from hopalong import *
from mandelbrot import mandelbrot


def main():
    screen = Window()
    if config.verbose:
        print(pygame.display.get_surface().get_size())
    running = True
    while running:
        for _ in range(20):
            running = biomorph(screen)
        running = mandelbrot(screen)
        # running = kaleidoscope(screen)
        for _ in range(5):
            running = spiro(screen)
        running = lines(screen)
        for _ in range(5):
            running = hopalong(screen)
    close_window()


if __name__ == "__main__":
    main()
