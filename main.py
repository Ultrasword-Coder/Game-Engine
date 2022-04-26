import pygame

import engine
from engine import window, clock, user_input, handler, draw
from engine import filehandler, maths, animation, state, serialize
from engine import spritesheet, core_utils
from engine.globals import *

# create essential instances
window.create_instance("Template", 640, 360, f=pygame.RESIZABLE)
window.set_scaling(True)
# should use framebuffer!
window.change_framebuffer(1280, 720, pygame.SRCALPHA)

# ------------------------------ your code ------------------------------ #
FPS = 60 # change fps if needed
BACKGROUND = (255, 255, 255) # change background color if needed

# default state
HANDLER = state.State()
state.push_state(HANDLER)
# ----------------------------------------------------------------------- #


clock.start(fps=FPS)
window.create_clock(clock.FPS)
running = True
while running:
    # update clock -- calculate delta time
    clock.update()
    window.GLOBAL_CLOCK.tick(FPS)

    # fill instance
    window.fill_buffer(BACKGROUND)

    # updates
    if state.CURRENT:
        state.CURRENT.update(clock.delta_time)

    # render
    window.push_buffer((0,0))

    # update display
    pygame.display.flip()

    # update keyboard and mouse
    user_input.update()
    # for loop through events
    for e in pygame.event.get():
        # handle different events
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            # keyboard press
            user_input.key_press(e)
        elif e.type == pygame.KEYUP:
            # keyboard release
            user_input.key_release(e)
        elif e.type == pygame.MOUSEMOTION:
            # mouse movement
            user_input.mouse_move_update(e)
        elif e.type == pygame.MOUSEBUTTONDOWN:
            # mouse press
            user_input.mouse_button_press(e)
        elif e.type == pygame.MOUSEBUTTONUP:
            # mouse release
            user_input.mouse_button_release(e)
        elif e.type == pygame.WINDOWRESIZED:
            # window resized
            window.handle_resize(e)
            user_input.update_ratio(window.WIDTH, window.HEIGHT, window.ORIGINAL_WIDTH, window.ORIGINAL_HEIGHT)
        elif e.type == pygame.WINDOWMAXIMIZED:
            # window maximized
            window.get_instance().fill(background)
            # re render all entities
            HANDLER.render_all()
            # push frame
            pygame.display.update()
            # prevent re push
            window.INSTANCE_CHANGED = False

pygame.quit()
