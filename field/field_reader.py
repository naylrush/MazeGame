
from copy import deepcopy
from field.field import Field
from models.cell import Empty, Key, Stun, RubberRoom, Teleport, Armory, Sleep, Exit
from models.direction import UP, LEFT, DOWN, RIGHT
from models.position import Position


def read_fields(path):
    fields = []
    with open(path, 'r') as fields_txt:
        lines = fields_txt.readlines()

    if len(lines[0].split()) == 2:
        symbol_by_cell = find_and_read_field_symbols(lines, 1)
        return [read_field(lines, symbol_by_cell)]

    field_amount = int(lines[0])
    lines.pop(0)
    symbol_by_cell = find_and_read_field_symbols(lines, field_amount)
    current_line = 0
    for _ in range(field_amount):
        x_size = int(lines[current_line].split()[0])
        field_lines = [lines[current_line + i] for i in range(x_size * 2 + 1)]
        fields.append(read_field(field_lines, symbol_by_cell))
        current_line += x_size * 2 + (1 if fields[-1].has_key else 0)

    return fields


def find_and_read_field_symbols(lines, field_amount):
    current_line = 0

    # jump to cell symbols
    for _ in range(field_amount):
        x_size = int(lines[current_line].split()[0])
        current_line += x_size * 2

    # read cell symbols
    symbol_by_cell = {Empty().to_symbol(): Empty()}
    for line in lines[current_line:]:
        cell_type, command = line.split(maxsplit=1)
        symbol_by_cell[cell_type] = eval(command)

    return symbol_by_cell


def read_field(lines, symbol_by_cell):
    # read size
    x_size, y_size = map(int, lines[0].split())

    # read field
    field = [[] for _ in range(x_size)]
    # read cells
    for x in range(x_size):
        y = 0
        for sym in lines[1 + x * 2][:y_size * 2:2]:
            cell = deepcopy(symbol_by_cell[sym])
            field[x].append(cell)
            y += 1
    # read vertical walls
    for line in range(x_size):
        column = 0
        for sym in lines[1 + line * 2][1:y_size * 2:2]:
            if sym == '|':
                field[line][column].add_border_at(RIGHT)
                field[line][column + 1].add_border_at(LEFT)
            column += 1
    # read horizontal walls
    for column in range(x_size - 1):
        line = 0
        for sym in lines[2 + column * 2][:y_size * 2:2]:
            if sym == '_' or sym == '-':
                field[column][line].add_border_at(DOWN)
                field[column + 1][line].add_border_at(UP)
            line += 1

    # add teleport points
    for x in range(x_size):
        for y in range(y_size):
            if isinstance(field[x][y], Teleport):
                destination = field[x][y].destination
                field[destination.x][destination.y].teleport_dest_from.append(Position(x, y))

    return Field(field, has_key=symbol_by_cell.get(Key().to_symbol(), None) is not None)
