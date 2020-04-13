
from direction import *
from point import Point


class Player:
    def __init__(self, map, start_position=Point()):
        self.position = start_position
        self.map = map

    def move_to(self, position: Point):
        self.position = position

    def go_to(self, direction: Direction):
        self.position.shift_to(direction)

    def copy_go_to(self, direction: Direction):
        return Player(self.map, self.position.copy_shift_to(direction))

    def can_go_to(self, direction: Direction):
        if self.map.get(self.position).has_border_at(direction):
            return False
        else:
            return not self.map.is_out_of_map(self.position.copy_shift_to(direction))

    def try_go_to(self, direction: Direction):
        if self.can_go_to(direction):
            self.position.shift_to(direction)
            return True
        else:
            return False
