from actor import Actor


class NPC(Actor):
    # TODO Gather evidence/information
    # TODO possession

    def __init__(self, json_filename: str, **kwargs):
        super().__init__(json_filename, **kwargs)

