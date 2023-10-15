from enum import IntEnum, auto
from pathlib import Path

import arcade
import json


class AnimationType(IntEnum):
    Stopped = 0
    Once = auto()
    Looping = auto()
    PingPong = auto()


class Animation(arcade.Sprite):

    def __init__(self, json_filename: str, **kwargs):
        super().__init__(None, **kwargs)

        json_filename = Path(json_filename)

        self.animation_type: AnimationType = AnimationType.Looping
        self.animations: dict[str, tuple[int, int]] = dict()

        self._current_animation: str = ""

        self.frame_duration: float = 0.2
        self._frame_timer: float = 0.0
        self.frame: int = 0

        self.load_from_json(json_filename)

    def load_from_json(self, json_filename: str | Path):
        # TODO Load Textures into self.textures and assign self.animations
        pass

    @property
    def animation(self) -> str:
        return self._current_animation

    @animation.setter
    def animation(self, animation_name: str):
        if animation_name == self._current_animation or animation_name not in self.animations:
            return

        self._current_animation = animation_name

    def on_finished(self):
        """Override or reassign this to be called when an animation finished and animation_type is Once.
        """
        pass

    def update_animation(self, delta_time: float = 1/60):
        # TODO
        pass

