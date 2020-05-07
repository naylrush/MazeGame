
from copy import deepcopy
from models.direction import Direction, UP, LEFT, DOWN, RIGHT


class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def __iadd__(self, other):
        assert isinstance(other, Position) or isinstance(other, Direction)
        if isinstance(other, Position):
            self.x += other.x
            self.y += other.y
        else:
            # because of the way of storage a field
            shift_by_direction = {UP: Position(-1, 0), LEFT: Position(0, -1), DOWN: Position(1, 0), RIGHT: Position(0, 1)}
            direction = other
            self += shift_by_direction[direction]
        return self

    def __add__(self, other):
        copy = deepcopy(self)
        copy += other
        return copy

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __str__(self):
        return str(self.as_tuple())
