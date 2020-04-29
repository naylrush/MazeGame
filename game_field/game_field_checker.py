
from collections import deque
from models.cell import Teleport, Exit
from models.direction import Direction
from models.player import Player
from models.player import reset_player_total_ids
from models.position import Position


def add_player(game_field, queue, position):
    new_player = Player()
    game_field.add_player_at(new_player, position)
    queue.appendleft(new_player)


def find_exit(game_field, queue):
    exit_position = None
    visited = [[False for _ in range(game_field.y_size)] for _ in range(game_field.x_size)]
    while queue:  # DFS
        current_player = queue.popleft()
        current_player_position = game_field.player_position(current_player)
        visited[current_player_position.x][current_player_position.y] = True
        if isinstance(game_field.player_cell(current_player), Exit):
            exit_position = current_player_position
            break
        if isinstance(game_field.player_cell(current_player), Teleport):
            game_field.player_go_to(current_player, game_field.player_cell(current_player).destination)
            queue.appendleft(current_player)
        else:
            for direction in Direction:
                if game_field.player_can_go_to(current_player, direction):
                    new_position = current_player_position.copy_shift_to(direction)
                    if not visited[new_position.x][new_position.y]:
                        add_player(game_field, queue, new_position)
    return exit_position


def bypass_field(exit_position, game_field, queue):
    visited = [[False for _ in range(game_field.y_size)] for _ in range(game_field.x_size)]
    visited[exit_position.x][exit_position.y] = True
    while queue:
        current_player = queue.popleft()
        for teleport_point in game_field.player_cell(current_player).teleport_dest_from:
            if not visited[teleport_point.x][teleport_point.y]:
                visited[teleport_point.x][teleport_point.y] = True
                add_player(game_field, queue, teleport_point)
        for direction in Direction:
            if not game_field.player_cell(current_player).has_border_at(direction):
                new_position = game_field.player_position(current_player).copy_shift_to(direction)
                if not game_field.field.is_out_of_field(new_position) and not visited[new_position.x][new_position.y]:
                    if game_field.player_can_go_from_to(new_position, direction.opposite()):
                        visited[new_position.x][new_position.y] = True
                        add_player(game_field, queue, new_position)
                        new_player = Player()
                        game_field.add_player_at(new_player, new_position)
    return visited


def check_field(game_field):
    player = Player()
    game_field.add_player_at(player, Position(0, 0))
    queue = deque()
    queue.appendleft(player)
    exit_position = find_exit(game_field, queue)

    if exit_position is None:
        return Position(0, 0)
    game_field.reset()
    reset_player_total_ids()

    player = Player()
    game_field.add_player_at(player, exit_position)
    queue = deque()
    queue.appendleft(player)
    visited = bypass_field(exit_position, game_field, queue)

    game_field.reset()
    reset_player_total_ids()
    for x in range(game_field.x_size):
        for y in range(game_field.y_size):
            if not visited[x][y]:
                raise LookupError(Position(x, y))
