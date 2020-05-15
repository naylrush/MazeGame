
from models.cell import Cell
from models.direction import UP, LEFT, RIGHT
from models.position import Position


class Field:
    def __init__(self, field, walls, *, has_key=False):
        assert isinstance(field, list)
        self.field = field
        self.vertical_walls, self.horizontal_walls = walls
        self.has_key = has_key
        self.x_size = len(self.field)
        self.y_size = len(self.field[0])

    def __getitem__(self, position: Position):
        return self.field[position.x][position.y]

    def put_cell_at(self, position: Position, cell: Cell):
        assert isinstance(cell, Cell)
        self.field[position.x][position.y] = cell

    def is_out_of_field(self, position: Position):
        return position.x < 0 or position.x >= self.x_size or position.y < 0 or position.y >= self.y_size

    def wall_access(self, position, direction, set_value=None):
        if self.is_out_of_field(position) or self.is_out_of_field(position + direction):
            return True
        pos = position
        if direction == LEFT or direction == RIGHT:
            if direction == LEFT:
                pos = position + LEFT
            if set_value is None:
                return self.vertical_walls[pos.x][pos.y]
            else:
                self.vertical_walls[pos.x][pos.y] = set_value
        else:
            if direction == UP:
                pos = position + UP
            if set_value is None:
                return self.horizontal_walls[pos.x][pos.y]
            else:
                self.horizontal_walls[pos.x][pos.y] = set_value

    def has_wall_at(self, position, direction):
        return self.wall_access(position, direction)

    def remove_wall_at(self, position, direction):
        return self.wall_access(position, direction, False)
