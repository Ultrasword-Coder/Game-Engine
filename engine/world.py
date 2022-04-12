import pygame



# chunks will have a set size of 12 x 12
CHUNK_WIDTH = CHUNK_HEIGHT = 12
CHUNK_TILE_WIDTH = CHUNK_TILE_HEIGHT = 32
CHUNK_WIDTH_PIX = CHUNK_WIDTH * CHUNK_TILE_WIDTH
CHUNK_HEIGHT_PIX = CHUNK_HEIGHT * CHUNK_TILE_HEIGHT


class Chunk:
    def __init__(self, pos):
        """Chunk Constructor"""
        self.chunk_id = pos[0] + (pos[1] << 16)
        self.pos = tuple(pos[0], pos[1])
        self.world_pos = (pos[0] * CHUNK_WIDTH_PIX, pos[1] * CHUNK_HEIGHT_PIX)

        # visual aspects
        self.tile_map = (Chunk.create_grid_tile(x, y, None) for x in range(CHUNK_WIDTH) for y in range(CHUNK_HEIGHT))

    @property
    def id(self):
        """get the chunk id pos"""
        return self.chunk_id
    
    @staticmethod
    def create_grid_tile(x, y, img, collide=0):
        """
        Create a tile object
        
        The position from (x, y) is converted to 
                (x * TILE_WIDTH + self.world_pos[0], y * TILE_HEIGHT + self.world_pos[1])
        
        This ensures unecassary calculations are not performed
        """
        return [x * TILE_WIDTH + self.world_pos[0], y * TILE_HEIGHT + self.world_pos[1],
                         img, 1]

    def render(self, window):
        """Renders all the grid tiles and non tile objects"""
        pass


class World:
    def __init__(self):
        """World Constructor"""
        self.chunks = {}
        
    def add_chunk(self, chunk):
        """add a chunk to the world"""
        self.chunks[chunk.chunk_id] = chunk
    
    def get_chunk(self, x, y):
        """Get chunk from the world chunk cache"""
        return self.chunks.get(x + (y << 16))
    


