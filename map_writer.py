
from cell import *
from copy import deepcopy
from direction import *
from position import Position


def write_map(map, path=''):
    sym_map = [[] for _ in range(map.x_size * 2 - 1)]

    empty_sym = Empty().to_symbol()
    empty_border_sym = ' '

    unique_cells = {}

    # generate symbol map
    teleport_count = 0
    for i in range(map.x_size * 2 - 1):
        for j in range(map.y_size * 2 - 1):
            cell = map[Position(i // 2, j // 2)]
            if i & 1 == 0:
                if j & 1 == 0:
                    cell_symbol = cell.to_symbol()
                    if type(cell) is Teleport:
                        teleport_count += 1
                        cell_symbol = str(teleport_count)
                    sym_map[i].append(cell_symbol)
                    unique_cells[cell_symbol] = deepcopy(cell)
                else:
                    sym_map[i].append(RIGHT.to_symbol() if cell.has_border_at(RIGHT) else empty_border_sym)
            else:
                if j & 1 == 0:
                    sym_map[i].append(DOWN.to_symbol() if cell.has_border_at(DOWN) else empty_sym)
                else:
                    sym_map[i].append(empty_border_sym)

    unique_cells.pop(Empty().to_symbol())
    # generate command by symbol
    symbol_command = {}
    for cell_symbol, cell in unique_cells.items():
        command = cell.name + '('
        if type(cell) is Exit or type(cell) is RubberRoom:
            command += cell.direction.name
        elif type(cell) is Stun:
            command += str(cell.duration)
        elif type(cell) is Teleport:
            command += str(cell.destination)
        command += ')'
        symbol_command[cell_symbol] = command

    # print
    if path == '':
        print(map.x_size, map.y_size)
        for line in sym_map:
            print(*line, sep='')
        for symbol, command in symbol_command.items():
            print(symbol, command)
    else:
        file = open(path, "w+")
        with file as map_txt:
            map_txt.write(str(map.x_size) + ' ' + str(map.y_size) + '\n')
            for line in sym_map:
                for sym in line:
                    map_txt.write(sym)
                map_txt.write('\n')
            for symbol, command in symbol_command.items():
                map_txt.write(symbol + ' ' + command + '\n')
        file.close()
