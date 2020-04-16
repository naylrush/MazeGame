
from enum import Enum


class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    def to_char(self):
        return self.name[0]

    def to_symbol(self):
        return '_' if self.value % 2 == 0 else '|'


UP = Direction.UP
LEFT = Direction.LEFT
DOWN = Direction.DOWN
RIGHT = Direction.RIGHT


def direction_by_key(key: str):
    key.upper()
    direction_by_key_dict = {'W': UP, 'A': LEFT, 'S': DOWN, 'D': RIGHT}
    return direction_by_key_dict.get(key)
