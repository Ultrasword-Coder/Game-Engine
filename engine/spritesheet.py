"""
SpriteSheet

create spritesheet
- loads an image and make a spritesheet


"""


from engine import filehandler, window
from engine.world import Tile
from engine.globals import *
from dataclasses import dataclass


# ------------ SpriteData ----------------- #

@dataclass(init=False)
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
    parent_str: str = None

    def __init__(self, index: int, x: int, y: int, w: int, h: int, tex):
        """Sprite data constructor"""
        self.index = index
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.tex = tex


# ------------- SpriteTile ----------------- #

@dataclass(init=False)
class SpriteTile(Tile):
    """
    Sprite Tile object

    contains data and a render function!
    - child of Tile

    - GOES INTO CHUNKS

    Tile:
        x: int
        y: int
        img: str
        collide: int
    """

    # a SpriteData pointer reference object thingy idk what python does with complex objects anymore
    sprite_data: SpriteData
    sprite_hashed_name: str

    def __init__(self, x: int, y: int, collide: int, sprite_data):
        """Sprite Tile constructor"""
        super().__init__(x, y, None, collide)

        self.sprite_data = sprite_data
        self.sprite_hashed_name = self.genereate_hash_str()
        self.img = self.sprite_data.parent_str

    def render(self, images: dict, offset: tuple = (0, 0)) -> None:
        """Render function for this sprite tile"""
        if self.img:
            window.FRAMEBUFFER.blit(images[self.sprite_hashed_name], (self.x + offset[0], self.y + offset[1]))
    
    def cache_image(self, cache: dict) -> None:
        """Cache the image"""
        # we somehow need to hash the image
        cache[self.sprite_hashed_name] = filehandler.scale(self.sprite_data.tex, CHUNK_TILE_AREA)

    def genereate_hash_str(self) -> str:
        """Generate a hash string"""
        return f"{self.sprite_data.parent_str}-{self.sprite_data.index}"


# ------------- SpriteSheet ----------------- #

class SpriteSheet:
    """
    Sprite Sheet object

    - stores the path to the image
    - an array of sprite objects
    """

    def __init__(self, image: str, sprite_width: int, sprite_height: int, x_space: int = 0, y_space: int = 0):
        """Sprite Sheet Constructor"""
        self.sheet_path = image
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
            sprite_tile.parent_str = self.sheet_path
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

    def get_sprite(self, index: int) -> SpriteData:
        """Get a sprite data object"""
        return self.sprites[index]

