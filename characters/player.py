from actor import Actor


class Player(Actor):
    # TODO Lightsource (shader?)
    # TODO inventory

    MovingSpeed: float = 1.7
    RunningSpeed: float = 2.4

    def __init__(self, **kwargs):
        super().__init__("***.json", **kwargs)

