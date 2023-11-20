import arcade
from .actor import Actor
from random import random, choice
from enum import Enum

# TODO
#    Raumwechsel
#  Movement
#    "Random" movement
#      - Zufälliges Ziel (Mehr im eigenen Raum) -> Erreicht despawned
#        - Gewichtete Zielsetzung für eigenen Raum
#    Gerichtete bewegung (Zum Spieler/Objekt zur Interaktion/fliehen)
#       Hunting Verhalten
#  Events
#    "Herumstehen"?
#    Weitere Events?
#  Beweise
#  Mood-System/Hunt-System
#  Mehrere Geister?
#  Background-System


class GhostState(Enum):
    Inactive = 0
    Roaming = 1
    Hunting = 2
    HuntingSearch = 3
    Standing = 4
    # TODO Events?


class Ghost(Actor):

    ActivityTimerMin: float = 2.3
    ActivityTimerMax: float = 9.2
    RespawnTimerMin: float = 0.7
    RespawnTimerMax: float = 1.2

    # output = output_start + (output_end - output_start) * (input)

    def __init__(self, favourite_room: str, **kwargs):
        super().__init__(file_name="res/sprites/actors/ghost.json", **kwargs)

        self.favourite_room: str = favourite_room
        self.respawn_timer: float = 0.0
        self.activity_timer: float = 0.0
        self.state: GhostState = GhostState.Inactive
        self.path: list[tuple[int, int]] = []
        self.path_index: int = 0

        self.visible = False

    def on_update(self, delta_time: float = 1/60):
        # TODO Event (Event-Class? For different Events?)
        # TODO Flickering
        match self.state:
            case GhostState.Inactive:
                self.respawn_timer -= delta_time
                return

            case GhostState.Standing:
                pass

            case GhostState.Roaming:
                distance = arcade.math.get_distance(*self.position, *self.path[self.path_index])

                self.change_x = (self.path[self.path_index][0] - self.position[0]) / distance * self.speed
                self.change_y = (self.path[self.path_index][1] - self.position[1]) / distance * self.speed

                if distance < 5.0:
                    if self.path_index >= len(self.path) - 1:
                        self.despawn()
                    else:
                        self.path_index += 1

        self.activity_timer -= delta_time
        if self.activity_timer < 0.0:
            self.despawn()

    def is_active(self) -> bool:
        return self.state != GhostState.Inactive and self.activity_timer > 0.0

    def can_spawn(self) -> bool:
        return self.state == GhostState.Inactive and self.respawn_timer < 0.0

    def spawn(self, spawn_point: tuple[int, int]) -> GhostState:
        self.visible = True
        self.position = spawn_point
        self.path_index = 0
        self.activity_timer = self.ActivityTimerMin + (self.ActivityTimerMax - self.ActivityTimerMin) * random()
        self.state = choice((GhostState.Roaming, GhostState.Standing))
        return self.state

    def despawn(self):
        self.visible = False
        self.respawn_timer = self.RespawnTimerMin + (self.RespawnTimerMax - self.RespawnTimerMin) * random()
        self.state = GhostState.Inactive
        self.stop()

