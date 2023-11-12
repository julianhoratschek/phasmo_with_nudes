import arcade
from .actor import Actor
from random import random

# TODO
#  Spawning (in festem Raum)
#    In welchem Raum? Aussuchen? Festen Raum halten? Wo im Raum? (Kollision mit Entities)
#    Raumwechsel
#  Movement
#    "Random" movement
#      - Algorithmus A*
#        - Graphenalgorithmus
#        - Wegpunkte -> Optimalen Pfad finden (Tiles)
#      - Spawned -> Timer -> Despawned (+ Huntzeit)
#      - Zufälliges Ziel (Mehr im eigenen Raum) -> Erreicht despawned
#        - Gewichtete Zielsetzung für eigenen Raum
#      - Nach Despawn "Respawn-Timer"
#    Gerichtete bewegung (Zum Spieler/Objekt zur Interaktion/fliehen)
#       Hunting Verhalten
#  Events
#    "Herumstehen"?
#    Weitere Events?
#  Beweise
#  Mood-System/Hunt-System
#  Mehrere Geister?
#  Background-System

# TODO Ghost state


class Ghost(Actor):

    ActivityTimerMin: float = 2.3
    ActivityTimerMax: float = 5.2
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

        self.speed = 1.7

        self.visible = False

    def on_update(self, delta_time: float = 1/60):
        # TODO Movement (dependant on state?)
        # TODO Event (Event-Class? For different Events?)
        match self.state:
            case GhostState.Inactive:
                self.respawn_timer -= delta_time
                return

            case GhostState.Standing:
                self.activity_timer -= delta_time

            case GhostState.Roaming:
                self.activity_timer -= delta_time

                distance = arcade.math.get_distance(*self.position, *self.path[self.path_index])

                self.change_x = (self.path[self.path_index][0] - self.position[0]) / distance * self.speed
                self.change_y = (self.path[self.path_index][1] - self.position[1]) / distance * self.speed

                if distance < 5.0:
                    if self.path_index == len(self.path) - 1:
                        self.despawn()
                    else:
                        self.path_index += 1

        if self.activity_timer < 0.0:
            self.despawn()

    # TODO: hunt-function
    #   update player-position/last known position

    def is_active(self) -> bool:
        return self.state != GhostState.Inactive and self.activity_timer >= 0.0

    def can_spawn(self) -> bool:
        return self.state == GhostState.Inactive and self.respawn_timer < 0.0

    def spawn(self) -> GhostState:
        self.visible = True
        self.activity_timer = self.ActivityTimerMin + (self.ActivityTimerMax - self.ActivityTimerMin) * random()
        self.is_active = True

    def despawn(self):
        self.visible = False
        self.respawn_timer = self.RespawnTimerMin + (self.RespawnTimerMax - self.RespawnTimerMin) * random()
        self.state = GhostState.Inactive
        self.stop()

