
from map_reader import *
from map_writer import *
from point import Point


class Map:
    def __init__(self, map=None):
        if map is None:
            map = [[]]
        if not isinstance(map, type([[]])):
            raise
        self.map = map
        self.x_size = len(map)
        self.y_size = len(map[0])

    def __getitem__(self, i):
        return self.map[i]

    def get(self, point: Point):
        return self.map[point.x][point.y]

    def is_out_of_map(self, position: Point):
        return position.x < 0 or position.x >= self.x_size or position.y < 0 or position.y >= self.y_size

    def read_from(self, path: str):
        self.__init__(read_map(path))

    def write_to(self, path=''):
        write_map(self, path)
