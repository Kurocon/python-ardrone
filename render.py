import pygame

# Dimensions
W, H = 640, 360
CW, CH = W // 2, H // 2
O, OA = 60, 120

# Component sizes
reticle_radius_factor = 0.5
crosshair_size = 30
crosshair_small_size = 5
bar_height = H // 2
bar_width = 10
strafe_factor = 1
thrust_factor = 1
lift_factor = 1
yaw_factor = 1
text_padding = 10

# Colours
colour_stop = (255, 0, 0)
colour_mode = (142, 199, 255)
colour_control = (142, 199, 255)
colour_reticle = (255, 0, 0)
colour_crosshair = (0, 0, 0)
colour_bar = (0, 255, 0)
colour_bar_background = (0, 0, 0)
colour_text_outline = (0, 0, 0)


def render(screen, original_image, new_image, is_new_image, offset, keypoint, strafe, thrust, lift, yaw, is_landing,
           is_takeoff, is_auto, is_emergency, regular_font, alert_font):
    """
    Renders an image on the screen with additional information
    :param screen: The screen to blit to
    :param original_image: The image from the camera
    :param new_image: The process-result
    :param is_new_image: Flag for selecting which image to use (default = false)
    :param offset: Offset of target from center (format: (x, y), range: (-1...1, 1...-1)
    :param keypoint: Keypoint object (ask Kevin)
    :param strafe: Sideways movement
    :param thrust: Forward movement
    :param lift: Vertical movement
    :param yaw: Left-right rotation
    :param is_landing: Flag, is currently landing
    :param is_takeoff: Flag, is currently taking off
    :param is_auto: Flag, is currently flying on auto pilot
    :param is_emergency: Flag, is currently making emergency landing
    :param regular_font: Font for regular text
    :param alert_font: Font for large (alert) text
    :return:
    """
    # Draw image
    surface = pygame.image.frombuffer(new_image if is_new_image else original_image, (W, H), 'RGB')
    screen.blit(surface, (O, O))

    # Draw reticle
    if offset is not None:
        surface = pygame.Surface((W, H))
        reticle = (CW + offset[0] * W, CH + offset[1] * H)
        radius = reticle_radius_factor * keypoint.size
        pygame.draw.polygon(surface, colour_reticle, [
            (reticle[0] + radius, reticle[1]),
            (reticle[0], reticle[1] + radius),
            (reticle[0] - radius, reticle[1]),
            (reticle[0], reticle[1] - radius),
        ], 3)
        surface.set_colorkey((0, 0, 0))
        screen.blit(surface, (O, O))

    # Draw crosshair
    surface = pygame.Surface((W, H))
    surface.fill((255, 255, 255))
    pygame.draw.line(surface, colour_crosshair, (CW - crosshair_size, CH), (CW + crosshair_size, CH), 1)
    pygame.draw.line(surface, colour_crosshair, (CW - crosshair_size, CH - crosshair_small_size),
                     (CW - crosshair_size, CH + crosshair_small_size), 1)
    pygame.draw.line(surface, colour_crosshair, (CW + crosshair_size, CH - crosshair_small_size),
                     (CW + crosshair_size, CH + crosshair_small_size), 1)

    pygame.draw.line(surface, colour_crosshair, (CW, CH - crosshair_size), (CW, CH + crosshair_size), 1)
    pygame.draw.line(surface, colour_crosshair, (CW - crosshair_small_size, CH - crosshair_size),
                     (CW + crosshair_small_size, CH - crosshair_size), 1)
    pygame.draw.line(surface, colour_crosshair, (CW - crosshair_small_size, CH + crosshair_size),
                     (CW + crosshair_small_size, CH + crosshair_size), 1)

    surface.set_colorkey((255, 255, 255))
    screen.blit(surface, (O, O))

    # Draw strafe
    strafe = strafe if strafe is not None else 0
    surface = pygame.Surface((W, H))
    surface.fill((255, 255, 255))
    rectangle = pygame.Rect(CW, H - 2 * bar_width, bar_height * abs(strafe) * strafe_factor, bar_width)

    pygame.draw.rect(surface, colour_bar, rectangle, 0)
    pygame.draw.rect(surface, colour_bar_background, rectangle, 1)

    if strafe <= 0:
        surface = pygame.transform.flip(surface, True, False)

    surface.set_colorkey((255, 255, 255))
    screen.blit(surface, (O, O))

    # Draw thrust
    thrust = thrust if thrust is not None else 0
    surface = pygame.Surface((W, H))
    surface.fill((255, 255, 255))
    rectangle = pygame.Rect(W - bar_width, CH, bar_width, bar_height * abs(thrust) * thrust_factor)

    pygame.draw.rect(surface, colour_bar, rectangle, 0)
    pygame.draw.rect(surface, colour_bar_background, rectangle, 1)

    if thrust <= 0:
        surface = pygame.transform.flip(surface, False, True)

    surface.set_colorkey((255, 255, 255))
    screen.blit(surface, (O, O))

    # Draw lift
    lift = lift if lift is not None else 0
    surface = pygame.Surface((W, H))
    surface.fill((255, 255, 255))
    rectangle = pygame.Rect(0, CH, bar_width, bar_height * abs(lift) * lift_factor)

    pygame.draw.rect(surface, colour_bar, rectangle, 0)
    pygame.draw.rect(surface, colour_bar_background, rectangle, 1)

    if lift > 0:
        surface = pygame.transform.flip(surface, False, True)

    surface.set_colorkey((255, 255, 255))
    screen.blit(surface, (O, O))

    # Draw yaw
    yaw = yaw if yaw is not None else 0
    surface = pygame.Surface((W, H))
    surface.fill((255, 255, 255))
    rectangle = pygame.Rect(CW, H - bar_width, bar_height * abs(yaw) * yaw_factor, bar_width)

    pygame.draw.rect(surface, colour_bar, rectangle, 0)
    pygame.draw.rect(surface, colour_bar_background, rectangle, 1)

    if yaw <= 0:
        surface = pygame.transform.flip(surface, True, False)

    surface.set_colorkey((255, 255, 255))
    screen.blit(surface, (O, O))

    # Draw mode
    if is_takeoff:
        text = regular_font.render("Takeoff", True, colour_text_outline)
        rectangle = text.get_rect()

        rectangle.topright = (W - bar_width - text_padding + 1 + O, text_padding + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding + 1 + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding - 1 + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding - 1 + O, text_padding + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding - 1 + O, text_padding - 1 + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding + O, text_padding - 1 + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding + 1 + O, text_padding - 1 + O)
        screen.blit(text, rectangle)

        text = regular_font.render("Takeoff", True, colour_mode)
        rectangle = text.get_rect()
        rectangle.topright = (W - bar_width - text_padding + O, text_padding + O)
        screen.blit(text, rectangle)

    elif is_landing:
        text = regular_font.render("Landing", True, colour_text_outline)
        rectangle = text.get_rect()

        rectangle.topright = (W - bar_width - text_padding + 1 + O, text_padding + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding + 1 + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding - 1 + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding - 1 + O, text_padding + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding - 1 + O, text_padding - 1 + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding + O, text_padding - 1 + O)
        screen.blit(text, rectangle)
        rectangle.topright = (W - bar_width - text_padding + 1 + O, text_padding - 1 + O)
        screen.blit(text, rectangle)

        text = regular_font.render("Landing", True, colour_mode)
        rectangle = text.get_rect()
        rectangle.topright = (W - bar_width - text_padding + O, text_padding + O)
        screen.blit(text, rectangle)

    # Draw control
    if is_auto:
        text = regular_font.render("Auto", True, colour_text_outline)
        rectangle = text.get_rect()

        rectangle.topleft = (bar_width + text_padding + 1 + O, text_padding + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding + 1 + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding - 1 + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding - 1 + O, text_padding + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding - 1 + O, text_padding - 1 + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding + O, text_padding - 1 + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding + 1 + O, text_padding - 1 + O)
        screen.blit(text, rectangle)

        text = regular_font.render("Auto", True, colour_control)
        rectangle = text.get_rect()
        rectangle.topleft = (bar_width + text_padding + O, text_padding + O)
        screen.blit(text, rectangle)

    else:
        text = regular_font.render("Manual", True, colour_text_outline)
        rectangle = text.get_rect()

        rectangle.topleft = (bar_width + text_padding + 1 + O, text_padding + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding + 1 + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding - 1 + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding - 1 + O, text_padding + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding - 1 + O, text_padding - 1 + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding + O, text_padding - 1 + O)
        screen.blit(text, rectangle)
        rectangle.topleft = (bar_width + text_padding + 1 + O, text_padding - 1 + O)
        screen.blit(text, rectangle)

        text = regular_font.render("Manual", True, colour_control)
        rectangle = text.get_rect()
        rectangle.topleft = (bar_width + text_padding + O, text_padding + O)
        screen.blit(text, rectangle)

    # Draw emergency
    if is_emergency:
        text = alert_font.render("STOP", True, colour_text_outline)
        rectangle = text.get_rect()

        rectangle.midtop = (CW + 1 + O, text_padding + O)
        screen.blit(text, rectangle)
        rectangle.midtop = (CW + 1 + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.midtop = (CW + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.midtop = (CW - 1 + O, text_padding + 1 + O)
        screen.blit(text, rectangle)
        rectangle.midtop = (CW - 1 + O, text_padding + O)
        screen.blit(text, rectangle)
        rectangle.midtop = (CW - 1 + O, text_padding - 1 + O)
        screen.blit(text, rectangle)
        rectangle.midtop = (CW + O, text_padding - 1 + O)
        screen.blit(text, rectangle)
        rectangle.midtop = (CW + 1 + O, text_padding - 1 + O)
        screen.blit(text, rectangle)

        text = alert_font.render("STOP", True, colour_stop)
        rectangle = text.get_rect()
        rectangle.midtop = (CW + O, text_padding + O)
        screen.blit(text, rectangle)

    # Draw title
    text = alert_font.render("ARDrone 2.0", True, (255, 255, 255))
    rectangle = text.get_rect()
    rectangle.topleft = (text_padding, text_padding)
    screen.blit(text, rectangle)

    # Draw subtitle
    text = alert_font.render("Target Practice", True, (255, 255, 255))
    rectangle = text.get_rect()
    rectangle.topright = (W + 2 * O - text_padding, text_padding)
    screen.blit(text, rectangle)

    # Draw descriptions
    text = regular_font.render("Strafe", True, (255, 255, 255))
    rectangle = text.get_rect()
    rectangle.midtop = (CW + O, H + O + text_padding // 2)
    screen.blit(text, rectangle)

    text = regular_font.render("Yaw", True, (255, 255, 255))
    rectangle = text.get_rect()
    rectangle.midtop = (CW + O, H + O + text_padding // 2 + rectangle.height)
    screen.blit(text, rectangle)

    text = regular_font.render("Lift", True, (255, 255, 255))
    text = pygame.transform.rotate(text, 90)
    rectangle = text.get_rect()
    rectangle.midright = (O - text_padding // 2, CH + O)
    screen.blit(text, rectangle)

    text = regular_font.render("Thrust", True, (255, 255, 255))
    text = pygame.transform.rotate(text, -90)
    rectangle = text.get_rect()
    rectangle.midleft = (W + O + text_padding // 2, CH + O)
    screen.blit(text, rectangle)

    # Draw instructions
    text = regular_font.render("Press 'I' to switch feed", True, (255, 255, 255))
    rectangle = text.get_rect()
    rectangle.bottomleft = (text_padding, H + O + OA - text_padding)
    screen.blit(text, rectangle)

    text = regular_font.render("Press 'Return' to start", True, (255, 255, 255))
    rectangle = text.get_rect()
    rectangle.bottomleft = (text_padding, H + O + OA - text_padding - rectangle.height)
    screen.blit(text, rectangle)

    text = regular_font.render("Press 'Escape' to kill drone", True, (255, 255, 255))
    rectangle = text.get_rect()
    rectangle.bottomright = (W + 2 * O - text_padding, H + O + OA - text_padding - rectangle.height)
    screen.blit(text, rectangle)

    text = regular_font.render("Press 'Space' for emergency stop", True, (255, 255, 255))
    rectangle = text.get_rect()
    rectangle.bottomright = (W + 2 * O - text_padding, H + O + OA - text_padding)
    screen.blit(text, rectangle)
