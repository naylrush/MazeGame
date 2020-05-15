from field.field import Field
from game_field.game_field import GameField
from game_field.game_field_checker import check_field, find_exit
from models.cell import Empty, Key, Stun, RubberRoom, Teleport, Armory, Sleep, Exit
from models.direction import Direction
from models.player import Player
from models.position import Position
from random import choice, randint


class GenerationConfig:
    def __init__(self, x_size, y_size):
        self.max_exits_on_map = max(1, (x_size * y_size) // 50)
        self.random_cell_count = randint((x_size * y_size) // 12, (x_size * y_size) // 7)
        self.default_stun_duration = 2
        self.max_teleport_count = 9


def generate_field(x_size, y_size):
    cells = [[Empty() for _ in range(y_size)] for _ in range(x_size)]
    vertical_walls = [[True for _ in range(y_size)] for _ in range(x_size)]
    horizontal_walls = [[True for _ in range(y_size)] for _ in range(x_size)]
    field = Field(cells, (vertical_walls, horizontal_walls), has_key=False)
    game_field = GameField(field)

    generate_walls(game_field)

    config = GenerationConfig(x_size, y_size)

    exit_direction = calc_random_direction()
    for exit_count in range(config.max_exits_on_map):
        random_put_cell_on(field, Exit(exit_direction), wall_required_at=exit_direction)
        random_put_cell_on(field, Key())

    teleport_counter = 0
    for _ in range(config.random_cell_count):
        random_cell_type = calc_random_cell_type()
        if teleport_counter == config.max_teleport_count:
            while random_cell_type is Teleport:
                random_cell_type = calc_random_cell_type()
        if random_cell_type is Stun:
            random_put_cell_on(field, Stun(config.default_stun_duration))
        elif random_cell_type is RubberRoom:
            random_direction = calc_random_direction()
            random_put_cell_on(field, RubberRoom(random_direction), without_wall_at_direction=random_direction)
        elif random_cell_type is Teleport:
            teleport_counter += 1
            random_put_cell_on(field, Teleport(calc_random_position_on(field).as_tuple()))

    while fix_bad_rubber_room(game_field):
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
        if not game_field.field.is_out_of_field(new_position) and \
                not visited[new_position.x][new_position.y]:
            game_field.field.remove_wall_at(current_position, random_direction)
            game_field.player_go_to(player, new_position)
            current_position = new_position
            continue
        if game_field.field.has_wall_at(current_position, random_direction):
            game_field.field.remove_wall_at(current_position, random_direction)
        there_are_unvisited_positions = False
        for direction in Direction:
            new_position = current_position + direction
            if not game_field.field.is_out_of_field(new_position) and \
                    not visited[new_position.x][new_position.y]:
                there_are_unvisited_positions = True
                break
        if not there_are_unvisited_positions:
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
                            not visited[new_position.x][new_position.y]:
                        game_field.field.remove_wall_at(current_position, direction)
                        game_field.player_go_to(player, new_position)
                        return new_position
    return None


def calc_random_position_on(field: Field):
    return Position(randint(0, field.x_size - 1), randint(0, field.y_size - 1))


def calc_random_direction():
    random_number = randint(0, 3)
    return Direction(random_number)


def calc_random_cell_type():
    cell_types = [Stun, Stun, RubberRoom, RubberRoom, Armory, Armory, Teleport]
    return choice(cell_types)


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


def fix_bad_rubber_room(game_field):
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
        raise Exception('Field has no exit way by some position')
    else:
        return False
