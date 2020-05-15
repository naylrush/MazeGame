
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
    fields = read_fields(args.field_paths)
    for i, field in enumerate(fields):
        game_field = GameField(field)
        try:
            game_field.check_field()
        except LookupError as position:
            print('{}: FAILED {}'.format(i, position))
        else:
            print('{}: OK'.format(i))


def generate_and_save_field(args):
    if args.size is None:
        x_size, y_size = map(int, input("Generate field with size as x_size,y_size: ").split(','))
    else:
        x_size, y_size = map(int, args.size[1:-1].split(','))
    print('Generating...')
    field = generate_field(x_size, y_size)
    write_fields([field], args.file_path)
    print('Field saved')


def play_game(args):
    assert isinstance(args.field_paths, list) or isinstance(args.field_paths, str)
    if isinstance(args.field_paths, str):
        args.field_paths = [args.field_paths]
    fields = read_fields(args.field_paths)
    if args.players is None:
        args.players = int(input('How many players will play? — '))
    positions = []
    if args.start_positions is not None:
        for position in args.start_positions:
            x, y = map(int, position[1:-1].split(','))
            positions.append(Position(x, y))
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
    arg_parser = argparse.ArgumentParser()
    subparsers = arg_parser.add_subparsers(title='modes')

    parser = subparsers.add_parser('check', help='check --fields <paths>')
    parser.add_argument('--fields', nargs='+', dest='field_paths')
    parser.set_defaults(func=check_field)

    parser = subparsers.add_parser('generate', help='\
        generate --size <(x,y)> <path>')
    parser.add_argument('--size', default=None)
    parser.add_argument(dest='file_path')
    parser.set_defaults(func=generate_and_save_field)

    parser = subparsers.add_parser('game', help='\
        game --fields <paths> --players <count> --start_positions <(x,y)>')
    parser.add_argument('--fields', nargs='+', dest='field_paths')
    parser.add_argument('--players', type=int, default=None)
    parser.add_argument('--start_positions', nargs='+', default=None)
    parser.add_argument('--random_positions', action='store_true', default=False)
    parser.set_defaults(func=play_game)

    args = arg_parser.parse_args()
    args.func(args)
