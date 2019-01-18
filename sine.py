import math
import pygame
import screen_utils
import config


def sine_wave(screen):
    sin_line = int(screen.halfY / 2)
    sin_points = []
    old_sin_points = [[0, sin_line], [screen.sizeX, sin_line]]
    cos_points = []
    old_cos_points = [[0, screen.halfY], [screen.sizeX, screen.halfY]]
    tan_line = int(screen.halfY / 2 + screen.halfY)
    tan_points = []
    old_tan_points = [[0, tan_line], [screen.sizeX, tan_line]]
    freq = 0
    max_freq = 8
    amplitude = 90
    tan_amplitude = 50
    direction = 1
    running = config.running
    for i in range(1000):
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

        for x in range(0, screen.sizeX):
            y = int(math.sin((x / screen.sizeX) * freq * math.pi) * amplitude + sin_line)
            sin_points.append([x, y])
        pygame.draw.lines(screen.window, [0, 0, 255], False, old_sin_points, 2)
        pygame.draw.lines(screen.window, [255, 255, 255], False, sin_points, 2)
        pygame.draw.line(screen.window, [0, 255, 0], (0, sin_line), (screen.sizeX, sin_line), 2)

        for x in range(0, screen.sizeX):
            y = int(math.cos((x / screen.sizeX) * freq * math.pi) * amplitude + screen.halfY)
            cos_points.append([x, y])
        pygame.draw.lines(screen.window, [0, 0, 255], False, old_cos_points, 2)
        pygame.draw.lines(screen.window, [255, 255, 255], False, cos_points, 2)
        pygame.draw.line(screen.window, [0, 255, 0], (0, screen.halfY), (screen.sizeX, screen.halfY), 2)

        # for x in range(0, screen.sizeX):
        #     y = int(math.tan((x / screen.sizeX) * freq * math.pi) * tan_amplitude + tan_line)
        #     tan_points.append([x, y])
        # pygame.draw.lines(screen.window, [0, 0, 255], False, old_tan_points, 2)
        # pygame.draw.lines(screen.window, [255, 255, 255], False, tan_points, 2)
        # pygame.draw.line(screen.window, [0, 255, 0], (0, tan_line), (screen.sizeX, tan_line), 2)

        freq += (0.1 * direction)
        if freq <= -max_freq or freq >= max_freq:
            direction = direction * -1
        pygame.display.flip()
        old_sin_points = sin_points
        sin_points = []
        old_cos_points = cos_points
        cos_points = []
        old_tan_points = tan_points
        tan_points = []
        screen.clock.tick(3)
        print("freq={}".format(freq))
    return running
