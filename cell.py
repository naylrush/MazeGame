
from direction import Direction
from enum import Enum
from point import Point


class CellSymbol(Enum):
    Empty = '.'
    Stun = 'S'
    RubberRoom = '_'  # computing
    Teleport = 'T'
    Armory = 'A'
    Exit = 'E'


cell_symbols = {cell.name: cell.value for cell in CellSymbol}


class Cell:
    def __init__(self, position=Point()):
        self.name = type(self).__name__
        self.position = position
        self.borders = {direction: False for direction in Direction}

    def locate_at(self, position):
        self.position = position

    def add_border_at(self, direction: Direction):
        self.borders[direction] = True

    def has_border_at(self, direction: Direction):
        return self.borders[direction]

    def to_symbol(self):
        return cell_symbols[self.name]


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

    def to_symbol(self):
        return self.direction.to_char()


class Teleport(Cell):
    def __init__(self, destination: Point):
        super().__init__()
        self.destination = Cell(destination)


class Armory(Cell):
    def __init__(self):
        super().__init__()


class Exit(Cell):
    def __init__(self, direction: Direction):
        super().__init__()
        self.direction = direction
