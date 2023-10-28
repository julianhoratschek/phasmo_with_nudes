import arcade
import json

from pathlib import Path


class Animation(arcade.Sprite):
    def __init__(self, file_name: str, **kwargs):
        super().__init__(**kwargs)

        self.animations: dict[str, tuple[int, int]] = dict()
        self.load_from_json(file_name)

        self.frame_duration: float = 0.2
        self._frame_timer: float = 0.0

        self.current_animation: str = list(self.animations.keys())[0]
        self.frame_index: int = self.animations[self.current_animation][0]

        # This is needed for Hitbox-Assignment to work
        self.texture = self.textures[self.frame_index]

    def set_animation(self, new_animation: str):
        if self.current_animation == new_animation:
            return

        self.current_animation = new_animation
        self.frame_index = self.animations[new_animation][0]

    def load_from_json(self, file_path: str | Path):
        if isinstance(file_path, str):
            file_path = Path(file_path)

        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)

        image_path = file_path.with_name(json_data["meta"]["image"])

        for frame_tag in json_data["meta"]["frameTags"]:
            self.animations[frame_tag["name"]] = (frame_tag["from"], frame_tag["to"])

            for frame in json_data["frames"][frame_tag["from"]:frame_tag["to"]+1]:
                x, y, w, h = frame["frame"].values()
                self.textures.append(arcade.load_texture(image_path, x=x, y=y, width=w, height=h))

    def update_animation(self, delta_time: float = 1/60):
        self._frame_timer += delta_time
        if self._frame_timer < self.frame_duration:
            return

        self._frame_timer -= self.frame_duration

        self.frame_index += 1
        if self.frame_index > self.animations[self.current_animation][1]:
            self.frame_index = self.animations[self.current_animation][0]

        self.texture = self.textures[self.frame_index]

