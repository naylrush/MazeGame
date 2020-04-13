
from copy import deepcopy
from direction import *


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, point):
        self.x += point.x
        self.y += point.y

    def __isub__(self):
        self.x = -self.x
        self.y = -self.y

    # because of way of storage a map
    def shift_to(self, direction: Direction):
        shift_by_direction = {UP: Point(-1, 0), LEFT: Point(0, -1), DOWN: Point(1, 0), RIGHT: Point(0, 1)}
        self.__add__(shift_by_direction[direction])

    def copy_shift_to(self, direction: Direction):
        copy = deepcopy(self)
        copy.shift_to(direction)
        return copy
