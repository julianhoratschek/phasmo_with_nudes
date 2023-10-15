from enum import Flag, auto
from characters import Direction


class KeyType(Flag):
    Unknown = 0
    Movement = auto()
    Run = auto()
    Crouch = auto()
    Interact = auto()
    Use = auto()
    Drop = auto()
    Place = auto()
    Menu = auto()


class KeyMap:

    def __init__(self):
        self.key_type: KeyType = KeyType.Unknown

    def __contains__(self, item: KeyType) -> bool:
        return item in self.key_type

    def press(self, symbol: int, modifier: int):
        # TODO add symbol to the currently pressed key combination
        pass

    def release(self, symbol: int, modifier: int):
        # TODO remove symbol
        pass

    def direction_of(self, symbol: int) -> Direction:
        # TODO return direction of symbol or Direction.Idle
        pass

