from util.aseprite import Animation


class Actor(Animation):
    WalkingSpeed: float = 1.7
    RunningSpeed: float = 2.4

    def __init__(self, file_name: str, **kwargs):
        super().__init__(file_name, **kwargs)

        self.speed: float = self.WalkingSpeed

