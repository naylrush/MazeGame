
from direction import *
from game_impl import GameImpl
from map import Map
from player import Player
from position import Position
from random import randint


class Game:
    def random_position_on_map(self, map: Map):
        return Position(randint(0, map.x_size - 1), randint(0, map.y_size - 1))

    def __init__(self,  maps=None, players_count=0, players_positions=None):
        if maps is None or not isinstance(maps, type([Map])) or len(maps) == 0:
            raise Exception('maps are not given or they are not [Map]')
        if players_count <= 0 or not isinstance(players_count, int):
            raise Exception('players_count is not int or <= 0')
        if players_positions is not None and not isinstance(players_positions, type([Position])):
            raise Exception('players_positions is not [Point]')
        self.map = maps[0]
        self.maps = maps  # not implemented
        self.players = []
        for i in range(players_count):
            if players_positions is not None and i < len(players_positions):
                if not maps[0].has_route_from(players_positions[i]):
                    raise Exception('Player ' + str(i) + 'has not route to the exit')
                self.players.append(Player(maps[0], players_positions[i], i))
            else:
                random_position = self.random_position_on_map(maps[0])
                while not maps[0].has_route_from(random_position):
                    random_position = self.random_position_on_map(maps[0])
                self.players.append(Player(maps[0], random_position, i))
        self.game_is_over = False
        self.current_player_id = 0
        self.current_player = self.players[self.current_player_id]
        self.game_impl = GameImpl()

    def wait_for_action(self):
        while not self.game_is_over:
            if self.current_player.stun > 0:
                stun = self.current_player.stun
                print('Player ' + str(self.current_player_id) + ' are stunned for ', end='')
                print('1 step' if stun == 1 else (str(stun) + ' steps'))
                self.current_player.stun -= 1
                continue
            print('Player ' + str(self.current_player_id) + ' step', end='')
            while True:
                print(' > ', end='')
                key = input()[0:1].lower()
                if direction_by_key(key) in Direction:
                    self.game_impl.move_to(self, direction_by_key(key))
                elif key == 'i':
                    self.game_impl.inventory(self)
                    continue
                elif key == 'x':
                    if not self.game_impl.shot_a_bullet(self):
                        continue
                elif key == '?':
                    self.game_impl.help(self)
                    continue
                else:
                    continue
                break
            self.current_player_id += 1
            self.current_player_id %= len(self.players)
            self.current_player = self.players[self.current_player_id]

    def start_game(self):
        if self.game_is_over:
            self.__init__(self.players[0].map, len(self.players))
        self.wait_for_action()
