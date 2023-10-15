from actor import Actor

from random import random, choice
from enum import IntEnum, auto


class BackgroundStory(IntEnum):
    # This will be the id for the background story
    # TODO BackgroundStory Object?
    NoBackground = 0


class Ghost(Actor):
    """Base class for all ghosts. This should be treated as abstract class.

    :cvar LifetimeMin: Minimum time until despawn
    :cvar LifetimeMax: Maximum time until despawn
    :cvar SpawnCooldown: Minimum time until next spawn try
    :cvar HuntCooldown: Minimum time until next hunt
    :cvar HuntingCutoff: If `mood` is lower than this, hunts may happen.

    :ivar is_active: If true, ghost is currently spawned
    :ivar mood: determines if the ghost will be hostile
    :ivar is_hunting: If true, ghost is currently hunting
    :ivar life_time: time until active ghost will despawn
    :ivar background_story: ID for current background story   # TODO Use BackgroundStoryObject instead?
    """

    LifetimeMin: float = 0.8
    LifetimeMax: float = 1.2

    SpawnCooldown: float = 0.5

    HuntCooldown: float = 0.2

    # Cutoffs for self.mood
    HuntingCutoff: float = 0.6

    def __init__(self, **kwargs):
        # TODO different Ghost Models?
        super().__init__(choice(["***.json", "***.json", "***.json"]), **kwargs)

        self._spawn_timer: float = self.SpawnCooldown
        self._hunt_cooldown_timer: float = self.HuntCooldown

        self.is_active: bool = False

        self.mood: float = 1.0
        self.is_hunting: bool = False

        self.life_time: float = self.LifetimeMax

        # TODO Select background story
        self.background_story: BackgroundStory = BackgroundStory.NoBackground
        self.spawn_objects()

    def spawn_objects(self):
        # TODO Spawn special Objects for ghost background-story and mood-system
        # TODO catch signals from items for mood modification
        pass

    def on_update(self, delta_time: float = 1/60):
        # TODO interact with environment
        #   - light switches
        #   - burst lights
        #   - turn on oven, radio etc.
        #       - creating dangers for player?
        #   - throw items (balls, plates, books)
        #   - move/tip over bigger objects (tables, beds, cars, bookshelves)?
        #       - with intent to kill/hurt player?
        # TODO create ghost events
        #   - sighing
        #   - singing
        #   - apparition?
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
        #       - Oujia-board
        #   - aura-glasses
        #       - seeing-crystal
        #   - talisman, cross
        #   - uv-light
        # TODO
        #   - ghost seals
        # TODO Line of sight?

        if not self.spawn():
            if not self.initialize_hunt():
                self.randomly_change_location()
                return

        self.set_direction()
        super().on_update(delta_time)

        self.life_time -= delta_time
        if self.life_time > 0 and not self.goal_reached():
            self.despawn(delta_time)

    def randomly_change_location(self):
        # TODO change location
        #   - Some ghost may walk through walls?
        pass

    def initialize_hunt(self) -> bool:
        # TODO return if a hunt is not possible (currently hunting, spawned, mood and cooldown)

        # TODO randomly start a hunt.
        #   - become visible
        #   - is_hunting true
        #   - extend life_time?
        #   - different pathfinding?
        self.is_hunting = True
        return self.is_hunting

    def spawn(self) -> bool:
        # TODO return if spawning is not possible (currently active, spawntimer > 0 etc.)

        # TODO Spawn in its room? Or spawn randomly, but preferring its own room?
        # TODO better lifetime distribution
        self.life_time = random() * self.LifetimeMax
        self.is_active = True
        return self.is_active

    def despawn(self, delta_time: float):
        # TODO Despawn ghost
        pass

    def goal_reached(self) -> bool:
        # TODO if ghost strives for a goal after spawning, return true if it was reached
        return False

    def set_direction(self):
        if self.is_hunting:
            pass
        else:
            # TODO wander around the house
            #   - wandering aimlessly for some time?
            #   - wandering towards a goal?
            #   - Spawning randomly, wandering around and despawn after some time, preferring its room to spawn?
            #   - Confined in its room?
            pass


