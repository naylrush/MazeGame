
from game.game_impl import GameImpl
from game_field.game_field import GameField
from models.direction import Direction, direction_by_key


class Game:
    def __init__(self, fields, players_count, players_positions=None):
        assert isinstance(fields, list)
        assert isinstance(players_count, int)
        assert players_count > 0
        if players_positions is not None:
            assert isinstance(players_positions, list)

        self.game_fields = [GameField(field) for field in fields]
        self.game_fields[0].check_field()

        self.game_impl = GameImpl()
        self.players = self.game_impl.place_players(self, players_count, players_positions)
        self.current_player = self.players[0]

        self.game_is_over = False
        self.key_required = self.game_fields[0].field.has_key

    def parse_shooting(self, in_command):
        split_in_command = in_command.split(' ')
        if len(split_in_command) == 1 or split_in_command[1] == '':
            print('Correct use of shooting is: X <W/A/S/D>')
            return False
        key = split_in_command[1][0]
        return self.game_impl.shoot(self, direction_by_key(key))

    def parse_actions(self):
        while not self.game_is_over:
            if self.game_impl.can_player_go(self):
                print('Player {} step'.format(self.current_player.id), end='')
                while True:
                    in_command = input(' > ').upper()
                    key = in_command[0] if len(in_command) > 0 else ''
                    if direction_by_key(key) in Direction:
                        self.game_impl.go_to(self, direction_by_key(key))
                        break
                    elif key == 'E':
                        print(self.current_player.inventory)
                    elif key == 'X':
                        if self.parse_shooting(in_command):
                            break
                    elif key == '?':
                        self.game_impl.help(self)
                    else:
                        print('You wrote incorrect command. Write "?" for help.')
            self.current_player = self.game_impl.calc_next_player(self)

    def start_game(self):
        if self.game_is_over:
            self.__init__(self.game_fields, len(self.players))
        self.parse_actions()
