import arcade

from util.aseprite import Animation

# TODO furniture overlapping

class Furniture(Animation):
    Path: str = "res/sprites/furniture"

    def __init__(self, name: str, **kwargs):
        super().__init__(f"{Furniture.Path}/{name}.json", **kwargs)


