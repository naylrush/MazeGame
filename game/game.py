
from game.game_impl import GameImpl
from game_field.game_field import GameField
from field.field import Field
from models.direction import *
from models.player import Player
from models.position import Position
from random import randint


def random_position_on_field(field: Field):
    return Position(randint(0, field.x_size - 1), randint(0, field.y_size - 1))


class Game:
    def __init__(self, fields, players_count, players_positions=None):
        assert isinstance(fields, type([Field]))
        assert isinstance(players_count, int)
        assert players_count > 0
        if players_positions is not None:
            assert isinstance(players_positions, type([Position]))
        self.game_field = GameField(fields[0])
        self.key_required = self.game_field.field.has_key
        self.game_field.check_field()
        self.game_fields = [GameField(fields[i]) for i in range(1, len(fields))]   # not implemented

        self.players = []
        for i in range(players_count):
            self.players.append(Player())
            if players_positions is not None and i < len(players_positions):
                self.players[-1].start_position = players_positions[i]
                self.game_field.add_player_at(self.players[-1], players_positions[i])
            else:
                random_position = random_position_on_field(fields[0])
                self.players[-1].start_position = random_position
                self.game_field.add_player_at(self.players[-1], random_position)

        self.game_is_over = False
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]
        self.game_impl = GameImpl()

    def parse_shooting(self, in_command):
        split_in_command = in_command.split(' ')
        if len(split_in_command) == 1 or split_in_command[1] == '':
            print('Correct use of shooting is: X <W/A/S/D>')
            return False
        key = split_in_command[1][0]
        return self.game_impl.shoot(self, direction_by_key(key))

    def parse_actions(self):
        while not self.game_is_over:
            if self.game_impl.player_is_stunned(self):
                self.current_player.stun -= 1
            else:
                print('Player ' + str(self.current_player.id) + ' step', end='')
                while True:
                    in_command = input(' > ').upper()
                    key = in_command[0]
                    if direction_by_key(key) in Direction:
                        self.game_impl.move_to(self, direction_by_key(key))
                        break
                    elif key == 'E':
                        self.game_impl.whats_in_inventory(self)
                    elif key == 'X':
                        if self.parse_shooting(in_command):
                            break
                    elif key == '?':
                        self.game_impl.help(self)
                    else:
                        print('You wrote incorrect command. Write "?" for help.')
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            self.current_player = self.players[self.current_player_index]

    def start_game(self):
        if self.game_is_over:
            self.__init__(self.game_fields, len(self.players))
        self.parse_actions()
