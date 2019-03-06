"""
'JuliaStalksImaginary ©2000 Ivan Freyman - FreymanArt.com
'This program draws imaginary stalks for a Julia set with coordinates -.72, +.125
'Original idea for drawing stalks invented by Cliff Pickover.
'Imaginary stalks are created when the point being iterated passes within a short distance
'(in this case .002) of the imaginary axis (Y-axis).  If that happens, iteration is halted
'and the point's starting location is colored in proportion to the distance to the imaginary axis.
"""
import config
import screen_utils
import math
import pygame


def stalks(screen):
    sx = screen.sizeX
    sy = screen.sizeY
    scrn = 1
    maxi = 200
    # Maximum # of iterations to perform

    pi = 3.141592

    rr = 0
    gg = 0
    bb = 0


    xoff = 0
    yoff = 0
    z = 1.50

    xh = z + xoff
    # Coordinates of view window of Mandelbrot set.
    x1 = -z + xoff
    yh = z * .75 + yoff
    y1 = -z * .75 + yoff

    yp = 0
    y = yh
    ystep = (y1 - yh) / sy * scrn
    # for y in range(int(yh), int(y1), int(ystep)):
    for y in range(sy):
        print(y)
        # for y in range(int(yh), int(y1)):
        # for y = yh to yl step ystep
        xp = 0
        yp = yp + 1
        # x = xb
        x = xp
        xstep = (xh - x1) / sx * scrn
        # for x= xl to xh step xstep
        # for x in range(x1, xh, xstep):
        for x in range(sx):
            screen_utils.check_event()
            xp = xp + 1

            for anti in range(2):
                for anti2 in range(2):
                    icount = 0
                    rcount = 0
                    r = x + anti * xstep / 3
                    i = y + ystep * anti2 / 3

                for iterate in range(maxi):  #Set up loop to iterate point.
                    r2 = r * r - i * i - .72
                    # Complex multiplication.
                    i = 2 * r * i + .125
                    # You can change the numbers -.72 and +.125 for a different Julia set.
                    r = r2

                    su = i * i + r * r
                    # if su > 4:
                    #     if iterate < 7:
                    #         # skipplot() = next x
                    #         break
                    #     else:
                    #         # skipadd() = next anti2, next anti
                    #         break
                        # IF
                        # sum > 4
                        # then
                        # if iter < 7 THEN goto skipplot else goto skipadd 'Escape to infinity check
                        # end if

                    if abs(i) < .002 and iterate > 1:
                        # plotit()
                        rat = math.log(abs(i * r * 3000) + .15)

                        rr = rr + (math.sin(rat - pi) + 1) * 32768
                        gg = gg + (math.sin(rat - pi) + 1) * 32768
                        bb = bb + (math.sin(rat - pi * 1.2 + .4) + 1) * 32768

                # next
                # iterate
                # 'it close

            # skipadd()

            # plotit:
            #
            # rat = math.log(abs(i * r * 3000) + .15)
            #
            # rr = rr + (math.sin(rat - pi) + 1) * 32768
            # gg = gg + (math.sin(rat - pi) + 1) * 32768
            # bb = bb + (math.sin(rat - pi * 1.2 + .4) + 1) * 32768

            # skipadd:
            #
            # next
            # anti2
            # next
            # anti

        if anti < 2:
            color = [rr, gg, bb]
        else:
            color = [rr / 9, gg / 9, bb / 9]
        # dplot
        # xp, yp
        # print(xp, yp, color)
        screen.point(xp, yp, color)
        rr = 0
        gg = 0
        bb = 0

        pygame.display.flip()
        #     skipplot:
        #     next
        #     x
        # 'End loops
        # if not button then next y
        #
