
from game_map.game_map_checker import check_map
from models.cell import RubberRoom
from models.position import Position


class GameMap:
    def __init__(self, map):
        self.map = map
        self.x_size = self.map.x_size
        self.y_size = self.map.y_size
        self.players_at_position = [[set() for _ in range(self.y_size)] for _ in range(self.x_size)]
        self.position_by_player = {}

    def __getitem__(self, position: Position):
        return self.map[position]

    def reset(self):
        self.__init__(self.map)

    def players_at(self, position: Position):
        return self.players_at_position[position.x][position.y]

    def player_position(self, player):
        return self.position_by_player[player]

    def player_cell(self, player):
        return self.__getitem__(self.position_by_player[player])

    def add_player_at(self, player, position: Position):
        self.players_at_position[position.x][position.y].add(player)
        self.position_by_player[player] = position

    def remove_player(self, player):
        player_position = self.position_by_player[player]
        self.players_at_position[player_position.x][player_position.y].remove(player)
        del self.position_by_player[player]

    def player_move_to(self, player, new_position: Position):
        player_position = self.position_by_player[player]
        self.players_at_position[player_position.x][player_position.y].remove(player)
        self.position_by_player[player] = new_position
        self.players_at_position[new_position.x][new_position.y].add(player)

    def player_go_to(self, player, direction):
        self.player_move_to(player, self.position_by_player[player].copy_shift_to(direction))

    def player_can_go_from_to(self, position, direction):
        if self.map[position].has_border_at(direction) or\
                self.map.is_out_of_map(position.copy_shift_to(direction)) or\
                (type(self.map[position]) is RubberRoom and self.map[position].direction != direction):
            return False
        return True

    def player_can_go_to(self, player, direction):
        player_position = self.position_by_player[player]
        return self.player_can_go_from_to(player_position, direction)

    def player_try_go_to(self, player, direction):
        if self.player_can_go_to(player, direction):
            self.player_go_to(player, direction)
            return True
        else:
            return False

    def check_map(self):
        position = check_map(self)
        if position is not None:
            raise LookupError(position)
