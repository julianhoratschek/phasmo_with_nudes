from enum import Flag, auto

import arcade.hitbox

from util.aseprite import Animation


class Direction(Flag):
    Idle = 0
    Up = auto()     # 0b0001
    Down = auto()   # 0b0010
    Left = auto()   # 0b0100
    Right = auto()  # 0b1000


class Player(Animation):
    def __init__(self, **kwargs):
        super().__init__("res/sprites/dude.json", **kwargs)

        self.direction: Direction = Direction.Idle
        self.speed: float = 2.0

        self.hit_box = arcade.hitbox.RotatableHitBox(points=[(-8, -16), (8, -16), (8, -11), (-8, -11)])

    # TODO Interact
    # TODO Collision
    # TODO Inventory
    # TODO Running
    # TODO Hiding

    def get_next_positions(self) -> list[tuple[int, int]]:
        for point in self.hit_box.get_adjusted_points():
            yield point[0] + self.change_x, point[1] + self.change_y

    def on_collision(self):
        self.change_x, self.change_y = 0.0, 0.0

    def on_update(self, delta_time: float = 1/60):
        self.change_x, self.change_y = 0.0, 0.0

        if Direction.Up in self.direction:
            self.change_y += self.speed

        if Direction.Down in self.direction:
            self.change_y -= self.speed

        if Direction.Right in self.direction:
            self.change_x += self.speed

        if Direction.Left in self.direction:
            self.change_x -= self.speed

        # TODO State based animation function
        self.set_animation("walk" if any(self.velocity) else "idle")


