
from field.field_reader import *
from field.field_writer import *
from models.position import Position


class Field:
    def __init__(self, field_key=None):
        if field_key is None:
            field_key = ([[]], False)
        elif isinstance(field_key, tuple):
            assert isinstance(field_key[0], type([[]]))
            assert isinstance(field_key[1], bool)
        self.field = field_key[0]
        self.has_key = field_key[1]
        self.x_size = len(self.field)
        self.y_size = len(self.field[0])

    def __getitem__(self, position: Position):
        return self.field[position.x][position.y]

    def is_out_of_field(self, position: Position):
        return position.x < 0 or position.x >= self.x_size or position.y < 0 or position.y >= self.y_size

    def read_from(self, path: str):
        self.__init__(read_field(path))

    def write_to(self, path=''):
        write_field(self, path)
