
from direction import *


class Cell:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.borders = {direction: False for direction in Direction}

    def locate_at(self, cell):
        self.x = cell.x
        self.y = cell.y

    def add_border_at(self, direction: Direction):
        self.borders[direction] = True

    def has_border_at(self, direction: Direction):
        return self.borders[direction]


class Empty(Cell):
    def __init__(self):
        super().__init__()


class Stun(Cell):
    def __init__(self, duration: int):
        if duration < 0:
            raise
        super().__init__()
        self.duration = duration


class RubberRoom(Cell):
    def __init__(self, direction: Direction):
        super().__init__()
        self.direction = direction


class Teleport(Cell):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.destination = Cell(x, y)


class Armory(Cell):
    def __init__(self):
        super().__init__()


class Exit(Cell):
    def __init__(self, direction: Direction):
        super().__init__()
        self.direction = direction
