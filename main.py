
from field.field_reader import read_fields
from field.field_writer import write_fields
from field.generator.field_generator import generate_field
from game.game import Game
from game_field.game_field import GameField, random_position_on_field
from models.position import Position
import argparse


def check_field(args):
    assert isinstance(args.field_paths, list) or isinstance(args.field_paths, str)
    if isinstance(args.field_paths, str):
        args.field_paths = [args.field_paths]
    for field_path in args.field_paths:
        fields = read_fields(field_path)
        for field in fields:
            game_field = GameField(field)
            try:
                game_field.check_field()
            except LookupError as position:
                print('FAILED {}'.format(position))
            else:
                print('OK')


def play_game(args):
    assert isinstance(args.field_paths, list) or isinstance(args.field_paths, str)
    if isinstance(args.field_paths, str):
        args.field_paths = [args.field_paths]
    fields = []
    for field_path in args.field_paths:
        if field_path == 'random_field':
            x_size, y_size = map(int, input("Generate field with size as x_size,y_size: ").split(','))
            print('Generating...')
            field = generate_field(x_size, y_size)
            answer = input('Field path to save or Here or Enter: ').lower()
            if answer != '':
                if answer == 'here':
                    write_fields([field])
                else:
                    write_fields([field], answer)
                    print('Field saved')
            fields.append(field)
        else:
            fields += read_fields(field_path)
    if args.players is None:
        args.players = int(input('How many players will play? — '))
    positions = []
    if args.start_positions is not None:
        for position in args.start_positions:
            x, y = position[1:len(position) - 1].split(',')
            positions.append(Position(int(x), int(y)))
    if not args.random_positions:
        if args.players - len(positions) > 0:
            print('Field size: {}x{}'.format(fields[0].x_size, fields[0].y_size))
            for i in range(len(positions), args.players):
                position = input('Start position as x,y or "random" for Player {}: '.format(i))
                if position == 'random':
                    positions.append(random_position_on_field(fields[0]))
                else:
                    x, y = position.split(',')
                    positions.append(Position(int(x), int(y)))
    game = Game(fields, args.players, positions)
    game.start_game()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='modes')

    check_parser = subparsers.add_parser('check', help='check --fields <field_paths>')
    check_parser.add_argument('--fields', type=str, nargs='+', dest='field_paths')
    check_parser.set_defaults(func=check_field)

    check_parser = subparsers.add_parser('game', help='\
    game --fields <field_paths> --players <players_count> --start_positions <positions as (x,y)>')
    check_parser.add_argument('--fields', type=str, nargs='+', dest='field_paths')
    check_parser.add_argument('--players', type=int, default=None)
    check_parser.add_argument('--start_positions', type=str, nargs='+', default=None)
    check_parser.add_argument('--random_positions', action='store_true', default=False)
    check_parser.set_defaults(func=play_game)

    args = parser.parse_args()
    args.func(args)
