
class Map:
    def __init__(self, map):
        if not isinstance(map, type([[]])):
            raise
        self.map = map
        self.x_size = len(map)
        self.y_size = len(map[0])

    def __getitem__(self, i):
        return self.map[i]
