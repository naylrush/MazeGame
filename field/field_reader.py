
from copy import deepcopy
from field.field import Field
from models.cell import Empty, Stun, RubberRoom, Teleport, Armory, Exit
from models.direction import UP, LEFT, DOWN, RIGHT
from models.inventory import Inventory
from models.position import Position


def read_fields(path):
    fields = []
    file = open(path, 'r')
    with file as field_txt:
        lines = field_txt.readlines()
        field_txt.close()
        file.close()

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
    phrase = 'Key at '

    # jump to cell symbols
    for _ in range(field_amount):
        x_size = int(lines[current_line].split()[0])
        current_line += x_size * 2
        if lines[current_line][:len(phrase)] == phrase:
            current_line += 1

    # read cell symbols
    symbol_by_cell = {Empty().to_symbol(): Empty()}
    for i in range(current_line, len(lines)):
        cell_type, command = lines[i][:1], lines[i][2:]
        symbol_by_cell[cell_type] = eval(command)

    return symbol_by_cell


def read_field(lines, symbol_by_cell):
    # read size
    x_size, y_size = lines[0].split()
    x_size, y_size = int(x_size), int(y_size)

    # read key
    game_with_key = False
    key_position = None
    phrase = 'Key at '
    if lines[x_size * 2][:len(phrase)] == phrase:
        game_with_key = True
        position = lines[x_size * 2][len(phrase):]
        x, y = position[1:len(position) - 2].split(',')
        key_position = Position(int(x), int(y))
        if key_position.x >= x_size or key_position.y >= y_size:
            raise Exception('Key is unreachable')

    # read field
    field = [[] for _ in range(x_size)]
    # read cells
    for x in range(x_size):
        y = 0
        for sym in lines[1 + x * 2][:y_size * 2:2]:
            cell = deepcopy(symbol_by_cell[sym])
            cell.locate_at(Position(x, y))
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

    # add key
    if game_with_key:
        field[key_position.x][key_position.y].inventory = Inventory(True)

    return Field(field, game_with_key)
