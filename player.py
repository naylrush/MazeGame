
from direction import *
from position import Position


class Inventory:
    def __init__(self, bullets=0):
        self.bullets = bullets
        self.max_bullets = 3

    def update_bullets(self):
        self.bullets = self.max_bullets


class Player:
    def __init__(self, map, start_position=Position(), id=0):
        self.map = map
        self.position = start_position
        self.id = id
        self.inventory = Inventory()
        self.stun = 0

    def move_to(self, position: Position):
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
