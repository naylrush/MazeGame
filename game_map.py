
from cell import RubberRoom
from position import Position


class GameMap:
    def __init__(self, map):
        self.map = map
        self.x_size = self.map.x_size
        self.y_size = self.map.y_size
        self.player_by_position = [[set() for _ in range(self.y_size)] for _ in range(self.x_size)]
        self.position_by_player = {}

    def __getitem__(self, position: Position):
        return self.map[position]

    def players_at(self, position: Position):
        return self.player_by_position[position.x][position.y]

    def player_position(self, player):
        return self.position_by_player[player]

    def player_cell(self, player):
        return self.__getitem__(self.position_by_player[player])

    def add_player_at(self, player, position: Position):
        self.player_by_position[position.x][position.y].add(player)
        self.position_by_player[player] = position

    def remove_player(self, player):
        player_position = self.position_by_player[player]
        self.players_at_position[player_position.x][player_position.y].remove(player)
        del self.position_by_player[player]

    def player_move_to(self, player, new_position: Position):
        player_position = self.position_by_player[player]
        self.players_at_position[player_position.x][player_position.y].remove(player)
        self.position_by_player[player] = new_position
        self.player_by_position[new_position.x][new_position.y].add(player)

    def player_go_to(self, player, direction):
        self.player_move_to(player, self.position_by_player[player].copy_shift_to(direction))

    def player_can_go_to(self, player, direction):
        player_position = self.position_by_player[player]
        if self.map[player_position].has_border_at(direction) or\
            self.map.is_out_of_map(player_position.copy_shift_to(direction)) or\
                (type(self.player_cell(player)) is RubberRoom and self.player_cell(player).direction != direction):
            return False
        return True

    def player_try_go_to(self, player, direction):
        if self.player_can_go_to(player, direction):
            self.player_go_to(player, direction)
            return True
        else:
            return False

    def has_route_from(self, start: Position):
        return game_map_has_route_from(start, self)
