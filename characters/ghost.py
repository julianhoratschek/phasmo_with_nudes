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


class Ghost(Actor):

    ActivityTimerMin: float = 2.3
    ActivityTimerMax: float = 5.2
    RespawnTimerMin: float = 0.7
    RespawnTimerMax: float = 1.2

    # output = output_start + (output_end - output_start) * (input)

    def __init__(self, favourite_room: str, **kwargs):
        super().__init__(file_name="res/sprites/actors/ghost.json", **kwargs)

        self.favourite_room: str = favourite_room
        self.goal: tuple[int, int] = (0, 0)
        self.respawn_timer: float = 0.0
        self.activity_timer: float = 0.0

        self.visible = False

        self.is_active: bool = False

    def on_update(self, delta_time: float = 1/60):
        if not self.is_active:
            self.respawn_timer -= delta_time
            if self.respawn_timer < 0.0:
                self.spawn()
        else:
            self.activity_timer -= delta_time
            if self.activity_timer < 0.0:
                self.despawn()

    def spawn(self):
        self.visible = True
        self.activity_timer = self.ActivityTimerMin + (self.ActivityTimerMax - self.ActivityTimerMin) * random()
        self.is_active = True

    def despawn(self):
        self.visible = False
        self.respawn_timer = self.RespawnTimerMin + (self.RespawnTimerMax - self.RespawnTimerMin) * random()
        self.is_active = False

    def set_goal(self):
        pass

    def move_to(self):
        pass


