
from game.game_impl import GameImpl
from game_map.game_map import GameMap
from map.map import Map
from models.direction import *
from models.player import Player
from models.position import Position
from random import randint


def random_position_on_map(map: Map):
    return Position(randint(0, map.x_size - 1), randint(0, map.y_size - 1))


class Game:
    def __init__(self,  maps=None, players_count=0, players_positions=None):
        if maps is None or not isinstance(maps, type([Map])) or len(maps) == 0:
            raise Exception('maps are not given or they are not [Map]')
        if players_count <= 0 or type(players_count) is not int:
            raise Exception('players_count is not int or <= 0')
        if players_positions is not None and not isinstance(players_positions, type([Position])):
            raise Exception('players_positions is not [Point]')
        self.game_map = GameMap(maps[0])
        self.game_map.check_map()
        self.game_maps = [GameMap(maps[i]) for i in range(1, len(maps))]   # not implemented
        self.players = []
        for i in range(players_count):
            self.players.append(Player())
            if players_positions is not None and i < len(players_positions):
                self.players[-1].start_position = players_positions[i]
                self.game_map.add_player_at(self.players[-1], players_positions[i])
            else:
                random_position = self.random_position_on_map(maps[0])
                self.players[-1].start_position = random_position
                self.game_map.add_player_at(self.players[-1], random_position)
        self.game_is_over = False
        self.current_player_it = iter(self.players)
        self.current_player = next(self.current_player_it)
        self.game_impl = GameImpl()

    def wait_for_action(self):
        while not self.game_is_over:
            if self.game_impl.player_is_stunned(self):
                self.current_player.stun -= 1
            else:
                print('Player ' + str(self.current_player.id) + ' step', end='')
                while True:
                    print(' > ', end='')
                    in_command = input().upper()
                    key = in_command[0:1]
                    if direction_by_key(key) in Direction:
                        self.game_impl.move_to(self, direction_by_key(key))
                    elif key == 'E':
                        self.game_impl.whats_in_inventory(self)
                        continue
                    elif key == 'X':
                        if len(in_command.split(' ')) > 1:
                            key = in_command.split(' ')[1][0:1]
                        while not direction_by_key(key) in Direction and key != 'Q':
                            print('shoot direction > ', end='')
                            key = input()[0:1].upper()
                        if key == 'Q' or not self.game_impl.shoot(self, direction_by_key(key)):
                            continue
                    elif key == '?':
                        self.game_impl.help(self)
                        continue
                    else:
                        continue
                    break
            try:
                self.current_player = next(self.current_player_it)
            except StopIteration:
                self.current_player_it = iter(self.players)
                self.current_player = next(self.current_player_it)

    def start_game(self):
        if self.game_is_over:
            self.__init__(self.game_maps, len(self.players))
        self.wait_for_action()
