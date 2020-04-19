
from models.direction import Direction
from models.inventory import Inventory
from models.position import Position


class Cell:
    def __init__(self, position=Position()):
        self.name = type(self).__name__
        self.position = position
        self.borders = {direction: False for direction in Direction}
        self.teleport_dest_from = []
        self.inventory = None

    def locate_at(self, position):
        self.position = position

    def add_border_at(self, direction: Direction):
        self.borders[direction] = True

    def has_border_at(self, direction: Direction):
        return self.borders[direction]

    def to_symbol(self):
        return self.name[0]


class Empty(Cell):
    def __init__(self):
        super().__init__()

    def to_symbol(self):
        return '.'


class Stun(Cell):
    def __init__(self, duration: int):
        if duration < 0:
            raise Exception('duration must be >= 0')
        super().__init__()
        self.duration = duration


class RubberRoom(Cell):
    def __init__(self, direction: Direction):
        super().__init__()
        self.direction = direction

    def to_symbol(self):
        return self.direction.to_char()


class Teleport(Cell):
    def __init__(self, dest: tuple):
        super().__init__()
        self.destination = Position(dest[0], dest[1])


class Armory(Cell):
    def __init__(self):
        super().__init__()


class Exit(Cell):
    def __init__(self, direction: Direction):
        super().__init__()
        self.direction = direction
