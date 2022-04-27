import pygame

from engine import filehandler, user_input, state
from engine import maths, window, draw, handler


class Test(handler.PersistentObject):
    OBJECT_TYPE = "test"
    def __init__(self):
        super().__init__()
        self.SPEED = 100
        self.object_type = Test.OBJECT_TYPE

        self.jump_sound = None
    
    def start(self):
        self.image = filehandler.scale(filehandler.get_image("test/images/blueberry.jpeg"), (63, 63))
        self.rect.area = self.image.get_size()
        self.jump_sound = filehandler.AudioRegistry("test/audio/mario.mp3")

    def update(self, dt):
        self.m_motion[0] = maths.lerp(self.m_motion[0], 0.0, 0.2)
        self.m_motion[1] = maths.lerp(self.m_motion[1], 0.0, 0.1)

        self.m_motion[1] += state.CURRENT.gravity * dt
        if user_input.is_key_pressed(pygame.K_d):
            self.m_motion[0] += self.SPEED * dt
        if user_input.is_key_pressed(pygame.K_a):
            self.m_motion[0] -= self.SPEED * dt
        if user_input.is_key_clicked(pygame.K_SPACE):
            self.m_motion[1] = -40
            self.jump_sound.play_audio(1, 0)
        
    def handle_changes(self):
        state.CURRENT.move_object(self)
        
    def render(self):
        window.get_framebuffer().blit(self.image, self.rect.topleft)
        draw.DEBUG_DRAW_LINES(window.get_framebuffer(), (255, 0, 0), True, 
                (self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft), 2)

handler.register_object_type(Test.OBJECT_TYPE, Test)