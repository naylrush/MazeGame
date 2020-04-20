
from field.field import Field
from game.game import Game, random_position_on_field
from game_field.game_field import GameField
from models.position import Position
import argparse


def check_field(args):
    for field_path in args.field_paths:
        field = Field()
        field.read_from(field_path)
        game_field = GameField(field)
        try:
            game_field.check_field()
        except LookupError as position:
            print('FAILED {}'.format(position))
        else:
            print('OK')


def play_game(args):
    field = Field()
    field.read_from(args.field_path)
    if args.players == 0:
        args.players = int(input('How many players will play? — '))
    positions = []
    if args.positions is not None:
        for position in args.positions:
            x, y = position[1:len(position) - 1].split(',')
            positions.append(Position(int(x), int(y)))
    if not args.random_positions:
        if args.players - len(positions) > 0:
            print('Field size:', field.x_size, field.y_size)
            for i in range(len(positions), args.players):
                position = input('Start position as (x,y) or "random" for Player {}: '.format(i))
                if position == 'random':
                    positions.append(random_position_on_field(field))
                else:
                    x, y = position[1:len(position) - 1].split(',')
                    positions.append(Position(int(x), int(y)))
    game = Game([field], args.players, positions)
    game.start_game()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='modes')

    check_parser = subparsers.add_parser('check', help='check --field <field_path/name>')
    check_parser.add_argument('--field', type=str, nargs='+', action='store', dest='field_paths')
    check_parser.set_defaults(func=check_field)

    check_parser = subparsers.add_parser('game', help='\
    game --field <field_path> --players <players_count> --start_positions <positions as (x,y)>')
    check_parser.add_argument('--field', type=str, action='store', dest='field_path')
    check_parser.add_argument('--players', type=int, action='store', dest='players', default=0)
    check_parser.add_argument('--start_positions', type=str, nargs='+', action='store', dest='positions', default=None)
    check_parser.add_argument('--random_positions', action='store_true', dest='random_positions', default=False)
    check_parser.set_defaults(func=play_game)

    args = parser.parse_args()
    args.func(args)
