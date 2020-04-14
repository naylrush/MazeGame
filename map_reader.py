
from cell import *
from copy import deepcopy
from direction import *
from position import Position


def read_map(path: str):
    file = open(path, 'r')
    with file as map_txt:
        lines = map_txt.readlines()

        # read size
        x_size, y_size = lines[0].split(' ')
        x_size, y_size = int(x_size), int(y_size)

        # read cell symbols
        cell_symbols = {Empty().to_symbol(): Empty()}
        for i in range(x_size * 2, len(lines)):
            cell_type, command = lines[i].split(' ')
            cell_symbols[cell_type] = eval(command)

        # read map
        map = [[] for _ in range(x_size)]
        # read cells
        for x in range(x_size):
            y = 0
            for sym in lines[1 + x * 2][::2]:
                cell = deepcopy(cell_symbols[sym])
                cell.locate_at(Position(x, y))
                map[x].append(cell)
                y += 1
        # read vertical walls
        for line in range(x_size):
            column = 0
            for sym in lines[1 + line * 2][1::2]:
                if sym == '|':
                    map[line][column].add_border_at(RIGHT)
                    map[line][column + 1].add_border_at(LEFT)
                column += 1
        # read horizontal walls
        for column in range(x_size - 1):
            line = 0
            for sym in lines[2 + column * 2][::2]:
                if sym == '_':
                    map[column][line].add_border_at(DOWN)
                    map[column + 1][line].add_border_at(UP)
                line += 1
    file.close()
    return map
