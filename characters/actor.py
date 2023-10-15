from enum import Flag, auto
from util.aseprite import Animation

import arcade


class Direction(Flag):
    Idle = 0
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()


class ActorState(Flag):
    Idling = 0
    Moving = auto()
    Running = auto()
    Crouching = auto()

    def to_animation(self):
        if ActorState.Crouching in self:
            return "crouch"
        if ActorState.Crouching in self:
            return "run"
        if ActorState.Moving in self:
            return "walk"
        return "idle"


class Actor(Animation):

    MovingSpeed: float = 1.0
    RunningSpeed: float = 1.5

    def __init__(self, json_filename: str, **kwargs):
        super().__init__(json_filename, **kwargs)

        self.direction: Direction = Direction.Idle
        self.speed: float = self.MovingSpeed

        self.state: ActorState = ActorState.Idling

    def flip_state(self, what: ActorState, on: bool):
        if on:
            self.state |= what
        else:
            self.state &= ~what

    @property
    def running(self) -> bool:
        return ActorState.Running in self.state

    @running.setter
    def running(self, run: bool):
        self.flip_state(ActorState.Running, run)

    @property
    def crouching(self) -> bool:
        return ActorState.Crouching in self.state

    @crouching.setter
    def crouching(self, crouch: bool):
        self.flip_state(ActorState.Crouching, crouch)

    def on_update(self, delta_time: float = 1/60):
        self.move()
        self.apply_animation()

    def move(self):
        self.change_x, self.change_y = 0.0, 0.0

        if Direction.Up in self.direction:
            self.change_y += self.speed
        if Direction.Down in self.direction:
            self.change_y -= self.speed
        if Direction.Right in self.direction:
            self.change_x += self.speed
        if Direction.Left in self.direction:
            self.change_x -= self.speed

        if any(self.velocity):
            self.state |= ActorState.Moving

    def apply_animation(self):
        self.animation = self.state.to_animation()
