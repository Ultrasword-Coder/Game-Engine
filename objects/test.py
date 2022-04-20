import pygame
from engine import handler, user_input, state, window, draw, maths


class test(handler.PersistentObject):
    object_type_name = "test"

    def __init__(self):
        super().__init__(self.object_type_name)
    
    def start(self):
        """Start method"""
        # should have already set ani_registry
        self.image = self.ani_registry.get_frame()
        self.rect.area = self.ani_registry.frame_dim

    def update(self, dt):
        self.ani_registry.update(dt)
        if self.ani_registry.changed:
            self.image = self.ani_registry.get_frame()

        # print(dt)
        if user_input.is_key_pressed(pygame.K_a):
            self.m_motion[0] -= 100 * dt
        if user_input.is_key_pressed(pygame.K_d):
            self.m_motion[0] += 100 * dt
        if user_input.is_key_pressed(pygame.K_w):
            self.m_motion[1] -= 100 * dt
        if user_input.is_key_pressed(pygame.K_s):
            self.m_motion[1] += 100 * dt
        
        # lerp
        self.m_motion[0] = maths.lerp(self.m_motion[0], 0.0, 0.3)
        self.m_motion[1] = maths.lerp(self.m_motion[1], 0.0, 0.3)
        state.CURRENT.move_object(self)

    def render(self):
        window.draw_buffer(self.image, self.rect.pos)
        # draw some lines facing the direction of the motion
        c = self.rect.center
        draw.DEBUG_DRAW_LINES(window.get_framebuffer(), (255, 0, 0), True, (self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft))
        draw.DEBUG_DRAW_LINE(window.get_framebuffer(), (255,0,0), c, (c[0] + self.m_motion[0] * 10, c[1] + self.m_motion[1] * 10), 1)

handler.register_object_type(test.object_type_name, test)