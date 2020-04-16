
from copy import deepcopy
from direction import *


class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        self.x += other.x
        self.y += other.y

    def __isub__(self):
        self.x = -self.x
        self.y = -self.y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __str__(self):
        return str((self.x, self.y))

    # because of the way of storage a map
    def shift_to(self, direction: Direction):
        shift_by_direction = {UP: Position(-1, 0), LEFT: Position(0, -1), DOWN: Position(1, 0), RIGHT: Position(0, 1)}
        self.__add__(shift_by_direction[direction])

    def copy_shift_to(self, direction: Direction):
        copy = deepcopy(self)
        copy.shift_to(direction)
        return copy
