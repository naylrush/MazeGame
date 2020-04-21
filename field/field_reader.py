
from copy import deepcopy
from models.cell import Empty, Stun, RubberRoom, Teleport, Armory, Exit
from models.direction import UP, LEFT, DOWN, RIGHT
from models.inventory import Inventory
from models.position import Position


def read_field(path: str):
    file = open(path, 'r')
    with file as field_txt:
        lines = field_txt.readlines()

        # read size
        x_size, y_size = lines[0].split(' ')
        x_size, y_size = int(x_size), int(y_size)

        # read key
        game_with_key = False
        phrase = 'Key at '
        if lines[x_size * 2][:len(phrase)] == phrase:
            game_with_key = True
            position = lines[x_size * 2][len(phrase):]
            x, y = position[1:len(position) - 2].split(',')
            key_position = Position(int(x), int(y))
            if key_position.x >= x_size or key_position.y >= y_size:
                raise Exception('Key is unreachable')

        # read cell symbols
        symbol_by_cell = {Empty().to_symbol(): Empty()}
        for i in range(x_size * 2 + (1 if game_with_key else 0), len(lines)):
            cell_type, command = lines[i][:1], lines[i][2:]
            symbol_by_cell[cell_type] = eval(command)

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

    file.close()
    return field, game_with_key
