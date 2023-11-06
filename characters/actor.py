from util.aseprite import Animation


class Actor(Animation):
    def __init__(self, file_name: str, **kwargs):
        super().__init__(file_name, **kwargs)

