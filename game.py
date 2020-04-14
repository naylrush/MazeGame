
from direction import *
from game_impl import GameImpl
from map import Map
from player import Player
from point import Point
from random import randint


class Game:
    def __init__(self, map: Map, players: int, positions=None):
        self.game_impl = GameImpl()
        if players < 0:
            raise
        self.map = map
        self.players = []
        if isinstance(positions, type([])):
            if len(positions) != players:
                raise
            for position in positions:
                if not map.has_route_from(position):
                    raise
                self.players.append(Player(map, position))
        else:
            for _ in range(players):
                position = self.random_position(map)
                if map.has_route_from(position):
                    self.players.append(Player(map, position))
        self.game_is_over = False
        self.current_player_id = 0
        self.current_player = self.players[self.current_player_id]

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
