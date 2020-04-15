
from cell import Exit
from direction import Direction
from player import *
from queue import Queue


def game_map_has_route_from(start, game_map):
    visited = [[False for _ in range(game_map.y_size)] for _ in range(game_map.x_size)]
    queue = Queue()
    player = Player()
    game_map.add_player_at(player, start)
    queue.put(player)
    while not queue.empty():
        current_player = queue.get()
        current_player_position = game_map.player_position(current_player)
        visited[current_player_position.x][current_player_position.y] = True
        if type(game_map.player_cell(current_player)) is Exit:
            reset_player_total_ids()
            return True
        for direction in Direction:
            if game_map.player_can_go_to(current_player, direction):
                new_position = game_map.player_position(current_player).copy_shift_to(direction)
                if not visited[new_position.x][new_position.y]:
                    new_player = Player()
                    game_map.add_player_at(new_player, new_position)
                    queue.put(new_player)
    return False
