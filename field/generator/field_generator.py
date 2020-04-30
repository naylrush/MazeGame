from field.field import Field
from game_field.game_field import GameField
from game_field.game_field_checker import check_field, find_exit, Bypass
from models.cell import Empty, Key, Stun, RubberRoom, Teleport, Armory, Sleep, Exit
from models.direction import Direction, UP, LEFT, RIGHT
from models.player import Player
from models.position import Position
from random import randint


def generate_field(x_size, y_size):
    cells = [[Empty() for _ in range(y_size)] for _ in range(x_size)]
    walls = [[[True, True] for _ in range(y_size)] for _ in range(x_size)]
    field = Field(cells, walls, has_key=False)
    game_field = GameField(field)

    generate_walls(game_field)

    exit_direction = calc_random_direction()
    for exit_count in range(max(1, (x_size * y_size) // 50)):
        random_put_cell_on(field, Exit(exit_direction), wall_required_at=exit_direction)
        random_put_cell_on(field, Key())

    teleport_counter = 0
    for random_cell_count in range(randint((x_size * y_size) // 12, (x_size * y_size) // 7)):
        random_cell_type = calc_random_cell_type()
        if teleport_counter == 9:
            while random_cell_type is Teleport:
                random_cell_type = calc_random_cell_type()
        if random_cell_type is Stun:
            random_put_cell_on(field, Stun(2))
        elif random_cell_type is RubberRoom:
            random_direction = calc_random_direction()
            random_put_cell_on(field, RubberRoom(random_direction), without_wall_at_direction=random_direction)
        elif random_cell_type is Teleport:
            teleport_counter += 1
            random_put_cell_on(field, Teleport(calc_random_position_on(field).as_tuple()))

    while check_bad_rubber_room(game_field):
        pass

    return game_field.field


def generate_walls(game_field):
    player = Player()
    current_position = Position(0, 0)
    game_field.add_player_at(player, current_position)

    visited = [[False for _ in range(game_field.y_size)] for _ in range(game_field.x_size)]

    while True:
        visited[current_position.x][current_position.y] = True
        random_direction = calc_random_direction()
        new_position = current_position + random_direction
        if not game_field.field.is_out_of_field(new_position) and\
                visited[new_position.x][new_position.y] is not None and\
                not visited[new_position.x][new_position.y]:
            remove_wall_at(game_field.field, current_position, random_direction)
            game_field.player_go_to(player, new_position)
            current_position = new_position
            continue
        if game_field.field.has_wall_at(current_position, random_direction):
            remove_wall_at(game_field.field, current_position, random_direction)
        unvisited_positions = []
        for direction in Direction:
            new_position = current_position + direction
            if not game_field.field.is_out_of_field(new_position) and\
                    visited[new_position.x][new_position.y] is not None and\
                    not visited[new_position.x][new_position.y]:
                unvisited_positions.append((new_position, direction))
        if not unvisited_positions:
            current_position = try_place_player_somewhere(game_field, player, visited)
            if current_position is None:
                break


def try_place_player_somewhere(game_field, player, visited):
    for x in range(game_field.x_size):
        for y in range(game_field.y_size):
            if visited[x][y]:
                current_position = Position(x, y)
                for direction in Direction:
                    new_position = current_position + direction
                    if not game_field.field.is_out_of_field(new_position) and \
                            visited[new_position.x][new_position.y] is not None and\
                            not visited[new_position.x][new_position.y]:
                        remove_wall_at(game_field.field, current_position, direction)
                        game_field.player_go_to(player, new_position)
                        return new_position
    return None


def remove_wall_at(field, position, direction):
    pos = position
    if direction == LEFT:
        pos = position + LEFT
    if direction == UP:
        pos = position + UP
    if not field.is_out_of_field(pos):
        field.walls[pos.x][pos.y][0 if direction == LEFT or direction == RIGHT else 1] = False


def calc_random_position_on(field: Field):
    return Position(randint(0, field.x_size - 1), randint(0, field.y_size - 1))


def calc_random_direction():
    random_number = randint(0, 3)
    return Direction(random_number)


def calc_random_cell_type():
    cell_types = [Stun, Stun, RubberRoom, RubberRoom, Armory, Armory, Teleport]
    return cell_types[randint(0, len(cell_types) - 1)]


def random_put_cell_on(field, cell, *, without_wall_at_direction=None, wall_required_at=None):
    while True:
        random_position = calc_random_position_on(field)
        cell_at_random_position = field[random_position]
        if isinstance(cell_at_random_position, Empty):
            if without_wall_at_direction is not None:
                if field.has_wall_at(random_position, without_wall_at_direction):
                    continue
            if wall_required_at is not None:
                if not field.has_wall_at(random_position, wall_required_at):
                    continue
            field.put_cell_at(random_position, cell)
            break


def check_bad_rubber_room(game_field):
    try:
        check_field(game_field)
    except LookupError as error:
        position = error.args[0]
        _, bypass = find_exit(game_field, start_position=position)
        for x in range(game_field.x_size):
            for y in range(game_field.y_size):
                current_position = Position(x, y)
                if bypass[current_position].visited and isinstance(game_field.field[current_position], RubberRoom):
                    game_field.field.put_cell_at(current_position, Empty())
                    return True
        raise OverflowError
    else:
        return False
