
# !/usr/bin/env python

import cv2
import pygame
import libardrone
import time
from flightCommandFromCoordinates import get_flight_command
from recognition import preprocess_image, process_image, draw_keypoint

capture = False
running = True
flying = False
path = 'tcp://192.168.1.1:5555'

drone = libardrone.ARDrone()
drone.speed = 0.5
pygame.init()
W, H = 640, 360
hud_color = (255, 0, 0)
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
stream = cv2.VideoCapture(path)

need_to_land = False
land_counter = 0

if capture:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("output.avi", fourcc, 20.0, (W, H))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                drone.reset()
                running = False
            # takeoff / land
            elif event.key == pygame.K_RETURN:
                drone.takeoff()
                flying = True
            elif event.key == pygame.K_SPACE:
                drone.land()
                flying = False
            # emergency
            elif event.key == pygame.K_BACKSPACE:
                drone.reset()
            # forward / backward

    if running == False:
        print "Shut Down"
        pygame.quit()
        drone.halt()
        break
    try:
        buff = stream.grab()
        imageyuv = stream.retrieve(buff)
        if capture:
            out.write(imageyuv)
        imagergb = cv2.cvtColor(imageyuv[1], cv2.COLOR_BGR2RGB)
        im = preprocess_image(imagergb)
        keypoint, offset = process_image(im)

        if need_to_land and land_counter >= 30:
            drone.land()
            flying = False
        elif need_to_land:
            print("Landing in {}".format(land_counter - 30))
            land_counter += 1

        # Process image
        if flying and not need_to_land:
            a, b, c, d = get_flight_command(keypoint, offset)
            if a is None:
                need_to_land = True

            else:
                print(a,b,c,d)
                drone.at(libardrone.at_pcmd, True, a, b, c, d)

        if keypoint is None:
            rgb_im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
        else:
            rgb_im = draw_keypoint(keypoint, im)

        surface = pygame.image.frombuffer(rgb_im, (W, H), 'RGB')
        bat = drone.navdata.get('battery', 0)
        screen.blit(surface, (0, 0))

        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())
        f = pygame.font.Font(None, 20)
        hud = f.render('Battery: %i%%' % bat, True, hud_color)
        print bat
        screen.blit(hud, (10, 10))
    except Exception as e:
        import traceback
        traceback.print_exc()
        print e
        pass
pygame.quit()