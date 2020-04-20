
from copy import deepcopy
from models.cell import *
from models.direction import *
from models.position import Position


def write_field(field, path=''):
    sym_field = [[] for _ in range(field.x_size * 2 - 1)]

    empty_sym = Empty().to_symbol()
    empty_border_sym = ' '

    unique_cells = {}

    # generate symbol field
    teleport_count = 0
    for i in range(field.x_size * 2 - 1):
        for j in range(field.y_size * 2 - 1):
            cell = field[Position(i // 2, j // 2)]
            if i & 1 == 0:
                if j & 1 == 0:
                    cell_symbol = cell.to_symbol()
                    if isinstance(cell, Teleport):
                        teleport_count += 1
                        cell_symbol = str(teleport_count)
                    sym_field[i].append(cell_symbol)
                    unique_cells[cell_symbol] = deepcopy(cell)
                else:
                    sym_field[i].append(RIGHT.to_symbol() if cell.has_border_at(RIGHT) else empty_border_sym)
            else:
                if j & 1 == 0:
                    sym_field[i].append(DOWN.to_symbol() if cell.has_border_at(DOWN) else empty_sym)
                else:
                    sym_field[i].append(empty_border_sym)

    unique_cells.pop(Empty().to_symbol())
    # generate command by symbol
    symbol_command = {}
    for cell_symbol, cell in unique_cells.items():
        command = cell.name + '('
        if isinstance(cell, Exit) or isinstance(cell, RubberRoom):
            command += cell.direction.name
        elif isinstance(cell, Stun):
            command += str(cell.duration)
        elif isinstance(cell, Teleport):
            command += str(cell.destination)
        command += ')'
        symbol_command[cell_symbol] = command

    # print
    if path == '':
        print(field.x_size, field.y_size)
        for line in sym_field:
            print(*line, sep='')
        for symbol, command in symbol_command.items():
            print(symbol, command)
    else:
        file = open(path, "w+")
        with file as field_txt:
            field_txt.write('{} {}\n'.format(field.x_size, field.y_size))
            for line in sym_field:
                for sym in line:
                    field_txt.write(sym)
                field_txt.write('\n')
            for symbol, command in symbol_command.items():
                field_txt.write('{} {}\n'.format(symbol, command))
        file.close()
