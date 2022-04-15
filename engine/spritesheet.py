"""
SpriteSheet

create spritesheet
- loads an image and make a spritesheet


"""


from engine import filehandler
from dataclasses import dataclass


@dataclass
class SpriteData:
    """
    Contains variables:

    - the index of the sprite sheet
    - spritesheet area
        - where origin data is stored on the sprite sheet
    - the actual sprite image
    """

    index: int
    x: int
    y: int
    w: int
    h: int

    tex: filehandler.pygame.Surface



class SpriteSheet:
    """
    Sprite Sheet object

    - stores the path to the image
    - an array of sprite objects
    """

    def __init__(self, image: str, sprite_width: int, sprite_height: int, x_space: int = 0, y_space: int = 0):
        """Sprite Sheet Constructor"""
        self.sheet = filehandler.get_image(image)
        self.sprites = []
        self.area = self.sheet.get_size()
        self.spacing = (x_space, y_space)
        self.sprite_area = (sprite_width, sprite_height)
        # get sprite count
        
        self.sprite_count = 0

        # load the images
        self.create()

    def create(self):
        """Create spritesheet"""
        left = self.spacing[0]
        top = self.spacing[1]

        sprite_count = 0
        while True:
            # get area
            new_img = filehandler.make_surface(self.sprite_area[0], self.sprite_area[1], filehandler.SRC_ALPHA)
            filehandler.crop_image(self.sheet, new_img, (left, top, left + self.sprite_area[0], top + self.sprite_area[1]))
            sprite_tile = SpriteData(sprite_count, left, top, self.sprite_area[0], self.sprite_area[1], new_img)
            self.sprites.append(sprite_tile)
            sprite_count += 1

            # calculate next position
            left += self.sprite_area[0] + self.spacing[0]
            if left >= self.area[0]:
                left = self.spacing[0]
                top += self.sprite_area[1] + self.spacing[1]
                if top >= self.area[1]:
                    break
        self.sprite_count = sprite_count

    def iterate_images(self):
        """Iterate thorugh images"""
        for i in range(len(self.sprites)):
            yield self.sprites[i]

