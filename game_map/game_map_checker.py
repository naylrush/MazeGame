
from collections import deque
from models.cell import Teleport, Exit
from models.direction import Direction
from models.player import *
from models.position import Position


def add_player(game_map, queue, position):
    new_player = Player()
    game_map.add_player_at(new_player, position)
    queue.appendleft(new_player)


def check_map(game_map):
    visited = [[False for _ in range(game_map.y_size)] for _ in range(game_map.x_size)]
    player = Player()
    game_map.add_player_at(player, Position(0, 0))
    queue = deque()
    queue.appendleft(player)
    exit_position = None
    while len(queue) > 0:  # DFS
        current_player = queue.popleft()
        current_player_position = game_map.player_position(current_player)
        visited[current_player_position.x][current_player_position.y] = True
        if isinstance(game_map.player_cell(current_player), Exit):
            exit_position = current_player_position
            break
        if isinstance(game_map.player_cell(current_player), Teleport):
            game_map.player_move_to(current_player, game_map.player_cell(current_player).destination)
            queue.appendleft(current_player)
        else:
            for direction in Direction:
                if game_map.player_can_go_to(current_player, direction):
                    new_position = current_player_position.copy_shift_to(direction)
                    if not visited[new_position.x][new_position.y]:
                        add_player(game_map, queue, new_position)

    if exit_position is None:
        return Position(0, 0)
    game_map.reset()
    reset_player_total_ids()
    visited = [[False for _ in range(game_map.y_size)] for _ in range(game_map.x_size)]
    visited[exit_position.x][exit_position.y] = True
    player = Player()
    game_map.add_player_at(player, exit_position)
    queue = deque()
    queue.appendleft(player)
    while len(queue) > 0:
        current_player = queue.popleft()
        for teleport_point in game_map.player_cell(current_player).teleport_dest_from:
            if not visited[teleport_point.x][teleport_point.y]:
                visited[teleport_point.x][teleport_point.y] = True
                add_player(game_map, queue, teleport_point)
        for direction in Direction:
            if not game_map.player_cell(current_player).has_border_at(direction):
                new_position = game_map.player_position(current_player).copy_shift_to(direction)
                if not game_map.map.is_out_of_map(new_position) and not visited[new_position.x][new_position.y]:
                    if game_map.player_can_go_from_to(new_position, direction.opposite()):
                        visited[new_position.x][new_position.y] = True
                        add_player(game_map, queue, new_position)
                        new_player = Player()
                        game_map.add_player_at(new_player, new_position)
                        queue.appendleft(new_player)

    game_map.reset()
    reset_player_total_ids()
    for x in range(game_map.x_size):
        for y in range(game_map.y_size):
            if not visited[x][y]:
                raise LookupError(Position(x, y))
