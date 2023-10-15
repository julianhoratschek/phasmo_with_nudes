from .ghost import Ghost


class Spirit(Ghost):
    MovingSpeed = 1.7
    RunningSpeed = 2.7

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


