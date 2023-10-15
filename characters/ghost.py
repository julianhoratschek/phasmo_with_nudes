from actor import Actor


class Ghost(Actor):
    # TODO catch signals from items for mood modification
    # TODO change location
    #   - Some ghost may walk through walls?
    # TODO wander around the house
    #   - Spawning in its room, wandering aimlessly for some time?
    #   - Spawning in its room, wandering towards a goal and despawn?
    #   - Spawning randomly, wandering around and despawn after some time, preferring its room to spawn?
    #   - Confined in its room?
    # TODO interact with environment
    #   - lightswitches
    #   - burst lights
    #   - turn on oven, radio etc.
    #       - creating dangers for player?
    #   - throw items (balls, plates, books)
    #   - move/tip over bigger objects (tables, beds, cars, bookshelves)?
    #       - with intent to kill/hurt player?
    # TODO create ghost events
    #   - sighing
    #   - singing
    #   - apparation?
    #   - hallucinations?
    # TODO react to evidence
    #   - compass
    #       - emf
    #           - oscilloscope
    #   - geiger-counter
    #   - temperature
    #       - infrared/thermo-sensor
    #   - low frequency analyzer
    #   - hygrometer
    #   - laser grid (dots)
    #   - old radio
    #       - spiritbox
    #   - pendulum
    #       - ujia-board
    #   - aura-glasses
    #       - seeing-crystal
    #   - talisman, cross
    #   - uv-light
    # TODO
    #   - ghost seals

    def __init__(self, json_filename: str, **kwargs):
        super().__init__(json_filename, **kwargs)

        self.mood: float = 1.0
        self.hunting_cutoff: float = 0.6
        self.hunting_cooldown: float = 0.25
        self._cooldown_counter: float = 0.0


