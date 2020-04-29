
from models.direction import UP, LEFT, RIGHT
from models.position import Position


class Field:
    def __init__(self, field, walls, *, has_key=False):
        assert isinstance(field, list)
        self.field = field
        self.walls = walls
        self.has_key = has_key
        self.x_size = len(self.field)
        self.y_size = len(self.field[0])

    def __getitem__(self, position: Position):
        return self.field[position.x][position.y]

    def is_out_of_field(self, position: Position):
        return position.x < 0 or position.x >= self.x_size or position.y < 0 or position.y >= self.y_size

    def has_wall_at(self, position, direction):
        if self.is_out_of_field(position) or self.is_out_of_field(position + direction):
            return True
        pos = position
        if direction == LEFT:
            pos = position + LEFT
        if direction == UP:
            pos = position + UP
        return self.walls[pos.x][pos.y][0 if direction == LEFT or direction == RIGHT else 1]
