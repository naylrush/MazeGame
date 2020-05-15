
from collections import deque
from models.cell import Teleport, Exit
from models.direction import Direction
from models.player import Player
from models.player import reset_player_total_ids
from models.position import Position


def add_player(game_field, queue: deque, position):
    new_player = Player()
    game_field.add_player_at(new_player, position)
    queue.appendleft(new_player)


class BypassCell:
    def __init__(self):
        self.visited = False
        self.came_from = None
        self.on_exit_way = False


class Bypass:
    def __init__(self, x_size, y_size):
        self.bypass = [[BypassCell() for _ in range(y_size)] for _ in range(x_size)]

    def __getitem__(self, position: Position):
        return self.bypass[position.x][position.y]

    def reset_except_exit_ways(self):
        for line in self.bypass:
            for bypass_cell in line:
                bypass_cell.visited = False
                bypass_cell.came_from = None


def mark_exit_way(bypass: Bypass, position):
    came_from = position
    while came_from is not None:
        current_cell_bypass = bypass[came_from]
        current_cell_bypass.on_exit_way = True
        came_from = current_cell_bypass.came_from


def player_teleport(game_field, queue: deque, bypass: Bypass, current_player):
    current_position = game_field.player_position(current_player)
    current_cell = game_field.player_cell(current_player)
    destination = current_cell.destination
    if not bypass[destination].visited and bypass[destination].came_from is None:
        bypass[destination].came_from = current_position
        game_field.player_go_to(current_player, destination)
        queue.appendleft(current_player)


def player_go(game_field, queue: deque, bypass: Bypass, current_player):
    current_position = game_field.player_position(current_player)
    for direction in Direction:
        if game_field.player_can_go_to(current_player, direction):
            new_position = current_position + direction
            if not bypass[new_position].visited and bypass[new_position].came_from is None:
                bypass[new_position].came_from = current_position
                add_player(game_field, queue, new_position)


def DFS(game_field, queue: deque, bypass: Bypass):
    current_player = queue.popleft()
    current_position = game_field.player_position(current_player)
    current_cell = game_field.player_cell(current_player)
    bypass[current_position].visited = True
    if isinstance(current_cell, Teleport):
        player_teleport(game_field, queue, bypass, current_player)
    else:
        player_go(game_field, queue, bypass, current_player)

    return current_position, current_cell


def find_exit(game_field):
    bypass = Bypass(game_field.x_size, game_field.y_size)

    queue = deque()
    start_position = Position(0, 0)
    add_player(game_field, queue, start_position)

    while queue:
        current_position, current_cell = DFS(game_field, queue, bypass)

        if isinstance(current_cell, Exit):
            exit_position = current_position
            mark_exit_way(bypass, exit_position)
            return exit_position, bypass

    return False, bypass


def player_bypass_from(game_field, bypass: Bypass, start_position):
    queue = deque()
    add_player(game_field, queue, start_position)

    while queue:
        current_position, _ = DFS(game_field, queue, bypass)

        if bypass[current_position].on_exit_way:
            mark_exit_way(bypass, current_position)
            return True, bypass

    return False, bypass


def bypass_field(game_field, bypass: Bypass):
    for x in range(game_field.x_size):
        for y in range(game_field.y_size):
            exit_is_reachable, bypass = player_bypass_from(game_field, bypass, Position(x, y))
            if not exit_is_reachable:
                return Position(x, y)
            bypass.reset_except_exit_ways()
    return None


def check_field(game_field):
    exit_found, bypass = find_exit(game_field)

    if not exit_found:
        return Position(0, 0)
    game_field.reset()
    reset_player_total_ids()

    bad_position = bypass_field(game_field, bypass)

    game_field.reset()
    reset_player_total_ids()

    if bad_position:
        raise LookupError(bad_position)
