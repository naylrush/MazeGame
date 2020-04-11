
from map_reader import *
from map_writer import *


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

    def read_from(self, path: str):
        self.__init__(read_map(path))

    def write_to(self, path=''):
        write_map(self, path)
