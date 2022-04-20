import pygame

import engine
from engine import window, clock, user_input, handler, draw
from engine import filehandler, maths, animation, state, serialize
from engine import spritesheet
from engine.globals import *

from objects import test

background = (255, 255, 255)

# create essential instances
window.create_instance("Template", 1280, 720, f=pygame.RESIZABLE)
window.set_scaling(True)
window.change_framebuffer(1280, 720, pygame.SRCALPHA)



# handler object -> # TODO - abstract later 
# HANDLER = state.State()
# state.push_state(HANDLER)
HANDLER = state.State.deserialize(serialize.load_json_data("test.json"))
state.push_state(HANDLER)


# -------------------------------- testing ------------------------------ #
# loading sprite sheet
sheet = spritesheet.SpriteSheet("test/images/tilemap.png", 16, 16, 0, 0)
def render_sprite_sheet(sheet):
    """temporary function to render the sprite sheet"""
    for data in sheet.iterate_images():
        window.get_framebuffer().blit(data.tex, (data.x, data.y))



# tile = "test/images/kirb.jpeg"
# c = HANDLER.make_template_chunk(0, 0)
# # for x in range(world.CHUNK_WIDTH):
# #     for y in range(world.CHUNK_HEIGHT):
# #         c.set_tile_at(c.create_grid_tile(x, y, tile))
# for x in range(CHUNK_WIDTH):
#     c.set_tile_at(c.create_grid_tile(x, 7, tile, collide=True))
# for x in range(CHUNK_WIDTH):
#     c.set_tile_at(c.create_grid_tile(x, 6, tile, collide=False))


# c.set_tile_at(spritesheet.SpriteTile(5, 5, 1, sheet.get_sprite(12)))


# img = filehandler.get_image("test/images/test1.png")

# data = animation.create_animation_handler_from_json("test/ani/ani.json")
# object_data = handler.ObjectData(100, 100, 100, 100)


# Test = test.test()
# Test.animation = data.get_registry()
# object_data.set_object_params(Test)

# HANDLER.add_entity_auto(Test)

# serialize.save_to_file("test.json", HANDLER.serialize())


# ----------------------------------------------------------------------- #


clock.start(fps=30)
window.create_clock(clock.FPS)
running = True
while running:
    # fill instance
    window.fill_buffer(background)

    # updates
    HANDLER.update(clock.delta_time)
    render_sprite_sheet(sheet)

    # render
    window.push_buffer((0,0))
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

    # update clock -- calculate delta time
    clock.update()
    # update global clock - time sleep for vsync
    window.GLOBAL_CLOCK.tick(clock.FPS)

pygame.quit()
