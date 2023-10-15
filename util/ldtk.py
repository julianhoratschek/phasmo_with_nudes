from pathlib import Path

import arcade
import json


class LDtkMap:
    def __int__(self, json_filename: str):
        json_filename = Path(json_filename)

        # TODO Walls and Collisions
        # TODO Entities
        # TODO Decorations with collision
        # TODO Rooms
        # TODO Shader?

    def add_to_scene(self, scene: arcade.Scene):
        # TODO add Walls
        # TODO add Floors
        # TODO add Decorations (with Collisions)
        # TODO add overlays? Opacity?
        # TODO add Entities
        # TODO add Doors
        # TODO shaders?
        pass


