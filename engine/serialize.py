"""
Contains functions and methods for serializing level data

Serializable objects:
- Rect
- Animation
- Entity
- Chunk
- World
- Handler
- State

Output will be a .json file
Data can be loaded using the classes made in this file

"""

import json
import pickle

from engine.globals import *


# TODO - make a global image section for the json
# all the images will be stored there



# ------- Serialize base object -------- #

class Serializable:
    def __init__(self):
        """Serializable Constructor"""
        pass
    
    def serialize(self) -> dict:
        """Serialize the object"""
        return {}
    
    @staticmethod
    def save_to_file(file_path: str, data: dict) -> None:
        """Saves data to a .json file"""
        if not file_path.endswith(".json"):
            file_path += ".json"
        with open(file_path, "w") as file:
            json.dump(data, file) # indent=4)
            file.close()


# --------- Serialize Animation --------- #

class SerializeAnimation(Serializable):
    def __init__(self):
        """Serialize Animation constructor"""
        super().__init__()

    def serialize(self, animation_registry) -> dict:
        """
        Serialize Animation

        - gets the filepath and thats about it
        """
        result = {}
        result[ANIMATION_PATH_KEY] = animation_registry.handler.json_path
        result[ANIMATION_NAME_KEY] = animation_registry.handler.name
        return result


# --------- Serialize Entity ------------ #

class SerializeEntity(Serializable):
    def __init__(self):
        """Serialize Entity constructor"""
        super().__init__()

    def serialize(self, entity) -> dict:
        """
        Serialize Entity

        - rect data
        - animatino data | if it exists
        """
        result = {}
        # serialize the rect
        result[ENTITY_RECT_KEY] = entity.rect.serialize()
        
        # serialize animation
        # if there is no animation, None - otherwise return animation name
        result[ENTITY_ANIMATION_KEY] = None if not entity.ani_registry else entity.ani_registry.handler.json_path
        
        # serialize the entity type
        result[ENTITY_TYPE_KEY] = str(pickle.dumps(type(entity), protocol=4))
        return result


# --------- Serialize Handler ----------- #

class SerializeHandler(Serializable):
    def __init__(self):
        """Serialize handler construcstor"""
        super().__init__()

        self.entity_serializer = SerializeEntity()
        self.animation_serializer = SerializeAnimation()

    def serialize(self, handler, graphics) -> dict:
        """
        Serialize Handler
        - stores all entity data and serializes it
        - serializes the different animations as well :D

        - animations are stored not based on image path but json file
        """
        result = {}
        
        # find animations and entities
        # animations = {}
        entities = {}
        for eid, entity in handler.p_objects.items():
            entities[eid] = self.entity_serializer.serialize(entity)

            # check if has an ani_registry
            if entity.ani_registry:
                # seriaelize the animation and add to graphics
                graphics[GRAPHICS_ANIMATION_KEY][entity.ani_registry.handler.json_path] = self.animation_serializer.serialize(entity.ani_registry)


        result[HANDLER_DATA_KEY] = entities
        # result[HANDLER_ANIMATION_KEY] = animations # TODO - find a place to put animations
        return result


# --------- Serialize State -------------- #

class SerializeState(Serializable):
    def __init__(self):
        """Serialize State Constructor"""
        super().__init__()

        self.handler_serializer = SerializeHandler()
        self.world_serializer = SerializeWorld()
        self.sprite_sheet_serializer = SerializableSpriteSheet()


    def serialize(self, state) -> dict:
        """
        Serialize State

        - serialize the world and the handler
        - world will consists of
            - world.chunks = {}
        """
        
        result = {}
        
        # create the dict for graphics stuff
        result[STATE_GRAPHICS_KEY] = {GRAPHICS_IMAGE_KEY: set(), GRAPHICS_ANIMATION_KEY: {}} # dict for now

        # get handler data
        handler_data = self.handler_serializer.serialize(state, result[STATE_GRAPHICS_KEY])
        world_data = self.world_serializer.serialize(state, result[STATE_GRAPHICS_KEY])
        
        result[STATE_HANDLER_KEY] = handler_data
        result[STATE_WORLD_KEY] = world_data

        # reset the sets to lists
        result[STATE_GRAPHICS_KEY][GRAPHICS_IMAGE_KEY] = list(result[STATE_GRAPHICS_KEY][GRAPHICS_IMAGE_KEY])
        # idk abt this y et
        # result[STATE_GRAPHICS_KEY][GRAPHICS_ANIMATION_KEY] = 
        return result


