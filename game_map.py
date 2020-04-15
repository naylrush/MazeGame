
# from copy import deepcopy
from game_map_checker import *
from map import Map
from position import Position


class GameMap():
    def __init__(self, map):
        self.map = map
        self.x_size = self.map.x_size
        self.y_size = self.map.y_size
        self.player_by_position = [[set() for _ in range(self.y_size)] for _ in range(self.x_size)]
        self.position_by_player = {}

    def get(self, position: Position):
        return self.map.get(position)

    def players_at(self, position: Position):
        return self.player_by_position[position.x][position.y]

    def player_position(self, player):
        return self.position_by_player[player]

    def player_cell(self, player):
        return self.get(self.position_by_player[player])

    def add_player_at(self, player, position: Position):
        self.player_by_position[position.x][position.y].add(player)
        self.position_by_player[player] = position

    def move_player_to(self, player, new_position: Position):
        player_position = self.position_by_player[player]
        self.player_by_position[player_position.x][player_position.y].remove(player)
        self.position_by_player[player] = new_position
        self.player_by_position[new_position.x][new_position.y].add(player)

    def player_go_to(self, player, direction):
        self.move_player_to(player, self.position_by_player[player].copy_shift_to(direction))

    # def player_copy_go_to(self, player, direction: Direction):
    #     new_player = Player()
    #     self.add_player_at(new_player, self.position_by_player[player].copy_shift_to(direction))
    #     return new_player

    def player_can_go_to(self, player, direction):
        player_position = self.position_by_player[player]
        if self.map.get(player_position).has_border_at(direction):
            return False
        else:
            return not self.map.is_out_of_map(player_position.copy_shift_to(direction))

    def player_try_go_to(self, player, direction):
        if self.player_can_go_to(player, direction):
            self.player_go_to(player, direction)
            return True
        else:
            return False

    def has_route_from(self, start: Position):
        return game_map_has_route_from(start, self)
