
from enum import Enum

direction_symbols = {'UP': '_', 'LEFT': '|', 'DOWN': '_', 'RIGHT': '|'}


class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    def to_char(self):
        return self.name[0]

    def to_symbol(self):
        return direction_symbols[self.name]


UP = Direction.UP
LEFT = Direction.LEFT
DOWN = Direction.DOWN
RIGHT = Direction.RIGHT


def direction_by_key(key: str):
    direction_by_key_dict = {'w': UP, 'a': LEFT, 's': DOWN, 'd': RIGHT}
    if key in direction_by_key_dict:
        return direction_by_key_dict[key]
    return None
