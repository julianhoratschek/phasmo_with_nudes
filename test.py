from enum import Flag, auto


class ee(Flag):
    a = 0
    b = auto()
    c = auto()


print((ee.b | ee.c))

