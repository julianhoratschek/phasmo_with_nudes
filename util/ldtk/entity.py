import arcade


class Entity(arcade.Sprite):
    def __init__(self, iid: str, **kwargs):
        super().__init__(**kwargs)

        self.entity_id: str = iid


class Stairs(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.destination = None


class Furniture(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.can_interact: bool = False

