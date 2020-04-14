
from cell import *
from direction import *
from map import Map
from player import Player
from point import Point
from random import randint


class Game:
    def __init__(self, map: Map, players: int, positions=None):
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
                self.players.append(Player(self.map, position))
        else:
            for _ in range(players):
                position = Point(randint(0, map.x_size - 1), randint(0, map.y_size - 1))
                if map.has_route_from(position):
                    self.players.append(Player(self.map, position))
        self.game_is_over = False
        self.current_player_id = 0
        self.current_player = self.players[self.current_player_id]

    def successful(self):
        print('You passed')

    def unsuccessful(self):
        print('You bumped into a wall')

    def update_bullets(self):
        self.current_player.inventory.update_bullets()
        print('Your bullets were updated. Now you have: ' + str(self.current_player.inventory.bullets))

    def kill_player(self, id):
        print('Player ' + str(self.current_player_id) + ' kills Player ' + str(id) + '!')

    def stun_for(self, duration):
        self.current_player.stun = duration
        print('You are stunned for ' + str(self.current_player.stun) + ' steps')

    def teleport_to(self, destination):
        print('You\'ve been teleported')
        self.current_player.move_to(destination)

    def gave_over(self):
        self.game_is_over = True
        print('Game is over! Player ' + str(self.current_player_id) + ' wins!')

    def move_to(self, direction: Direction):
        current_cell = self.map.get(self.current_player.position)
        if isinstance(current_cell, RubberRoom) and direction != current_cell.direction:
            self.successful()
            return
        elif isinstance(current_cell, Exit) and direction == current_cell.direction:
            self.gave_over()
            return
        if not self.current_player.try_go_to(direction):
            self.unsuccessful()
        else:
            self.successful()
            current_cell = self.map.get(self.current_player.position)
            if isinstance(current_cell, Armory):
                self.update_bullets()
                return
            elif isinstance(current_cell, Stun):
                self.stun_for(current_cell.duration)
                return
            elif isinstance(current_cell, Teleport):
                self.teleport_to(current_cell.destination)
                return

    def inventory(self):
        print('Inventory:')
        print('\tBullets: ' + str(self.current_player.inventory.bullets))

    def shot_a_bullet(self):
        if self.current_player.inventory.bullets == 0:
            print('You run out of bullets')
            return False
        print('Not implemented')
        return True

    def help(self):
        print('''
Walk keys:
    W — Up
    A — Left
    S — Down
    D — Right
    
Actions:
    X - Shot a bullet

Other:
    I - Inventory
    ? - Help

After any action except 'Other' you make a step.

For more information read this —— https://github.com/NaylRush/MazeGame
@NaylRush
        ''')

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
                    self.move_to(direction_by_key(key))
                elif key == 'i':
                    self.inventory()
                    continue
                elif key == 'x':
                    if not self.shot_a_bullet():
                        continue
                elif key == '?':
                    self.help()
                    continue
                else:
                    continue
                break
            self.current_player_id += 1
            self.current_player_id %= len(self.players)
            self.current_player = self.players[self.current_player_id]

    def start_game(self):
        if self.game_is_over:
            self.__init__(self.map, len(self.players))
        self.wait_for_action()
