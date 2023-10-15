from .entity import Entity
from characters.ghost import Ghost


class BackgroundStoryItem(Entity):
    def __init__(self, ghost: Ghost, **kwargs):
        super().__init__(**kwargs)

        self.ghost = ghost

    # TODO Fill with LDtk values

