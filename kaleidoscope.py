import pygame
import math
import screen_utils


def kaleidoscope(screen):
    running = True
    white = [255, 255, 255]
    blue = [0, 0, 255]
    radius = screen.halfY - 20
    pygame.draw.line(screen.window, blue, (0, screen.halfY), (screen.sizeX, screen.halfY), 1)
    pygame.draw.line(screen.window, blue, (screen.halfX, 0), (screen.halfX, screen.sizeY), 1)
    pygame.draw.line(screen.window, blue, (0, 0), (screen.sizeX, screen.sizeY), 2)
    pygame.draw.line(screen.window, blue, (0, screen.sizeY), (screen.sizeX, 0), 2)
    pygame.draw.circle(screen.window, white, (screen.halfX, screen.halfY), radius, 1)
    center = (screen.halfX, screen.halfY)
    degree = 0
    for degree in range(0, 360, 15):
        x = center[0] + math.cos(math.radians(degree)) * radius
        y = center[1] + math.sin(math.radians(degree)) * radius
        pygame.draw.line(screen.window, white, center, (x, y), 2)
        print(degree)
    pygame.display.flip()
    for v in range(10):
        screen.window.scroll(0, 10)
        pygame.display.flip()
        screen.clock.tick(10)
    while True:
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
    return running
