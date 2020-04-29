
from copy import deepcopy
from models.cell import Empty, Stun, RubberRoom, Teleport, Sleep, Exit
from models.direction import DOWN, RIGHT
from models.position import Position


def write_fields(fields, path=None):
    unique_cells = {}

    sym_fields = []
    teleport_sleep_count = 0
    for field in fields:
        sym_field, teleport_sleep_count = generate_sym_field(field, teleport_sleep_count, unique_cells)
        sym_fields.append(sym_field)

    unique_cells.pop(Empty().to_symbol())
    symbol_command = generate_command_by_symbol(unique_cells)

    sizes = [(field.x_size, field.y_size) for field in fields]
    if path is None:
        print_sym_fields_in_command_line(sym_fields, sizes, symbol_command)
    else:
        print_sym_fields_in_file(path, sym_fields, sizes, symbol_command)


def generate_sym_field(field, teleport_sleep_count, unique_cells):
    empty_sym = Empty().to_symbol()
    empty_border_sym = ' '

    sym_field = [[] for _ in range(field.x_size * 2 - 1)]
    for i in range(field.x_size * 2 - 1):
        for j in range(field.y_size * 2 - 1):
            cell = field[Position(i // 2, j // 2)]
            if i % 2 == 0:
                if j % 2 == 0:
                    cell_symbol = cell.to_symbol()
                    if isinstance(cell, Teleport) or isinstance(cell, Sleep):
                        teleport_sleep_count += 1
                        cell_symbol = str(teleport_sleep_count)
                    sym_field[i].append(cell_symbol)
                    unique_cells[cell_symbol] = deepcopy(cell)
                else:
                    sym_field[i].append(RIGHT.to_symbol() if cell.has_border_at(RIGHT) else empty_border_sym)
            else:
                if j & 1 == 0:
                    sym_field[i].append(DOWN.to_symbol() if cell.has_border_at(DOWN) else empty_sym)
                else:
                    sym_field[i].append(empty_border_sym)
    return sym_field, teleport_sleep_count


def generate_command_by_symbol(unique_cells):
    symbol_command = {}
    for cell_symbol, cell in unique_cells.items():
        command = cell.name + '('
        if isinstance(cell, Exit) or isinstance(cell, RubberRoom):
            command += cell.direction.name
        elif isinstance(cell, Stun):
            command += str(cell.duration)
        elif isinstance(cell, Teleport):
            command += str(cell.destination)
        elif isinstance(cell, Sleep):
            sleep_field_coords = (cell.destination_field_id, cell.destination_position.x, cell.destination_position.y)
            command += '{}, {}'.format(cell.duration, sleep_field_coords)
        command += ')'
        symbol_command[cell_symbol] = command
    return symbol_command


def print_sym_fields_in_command_line(sym_fields, sizes, symbol_command):
    print(len(sym_fields))
    for sym_field, size in zip(sym_fields, sizes):
        print(*size)
        for line in sym_field:
            print(*line, sep='')
    for symbol, command in symbol_command.items():
        print(symbol, command)


def print_sym_fields_in_file(path, sym_fields, sizes, symbol_command):
    with open(path, "w+") as field_txt:
        field_txt.write('{}\n'.format(len(sym_fields)))
        for sym_field, size in zip(sym_fields, sizes):
            field_txt.write('{} {}\n'.format(size[0], size[1]))
            for line in sym_field:
                for sym in line:
                    field_txt.write(sym)
                field_txt.write('\n')
        for symbol, command in symbol_command.items():
            field_txt.write('{} {}\n'.format(symbol, command))
