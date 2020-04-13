
from cell import Exit
from direction import Direction
from player import Player
from point import Point
from queue import Queue


def map_has_route_from(start: Point, map):
    visited = [[False for _ in range(map.y_size)] for _ in range(map.x_size)]
    queue = Queue()
    queue.put(Player(map, start))
    while not queue.empty():
        current_player = queue.get()
        visited[current_player.position.x][current_player.position.y] = True
        if type(map.get(current_player.position)) is Exit:
            return True
        for direction in Direction:
            if current_player.can_go_to(direction):
                new_player = current_player.copy_go_to(direction)
                if not visited[new_player.position.x][new_player.position.y]:
                    queue.put(current_player.copy_go_to(direction))
    return False
