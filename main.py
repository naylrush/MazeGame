
from game import Game
from game_map import GameMap
from map import Map
from position import Position
import argparse


def check_map(args):
    for map_path in args.map_paths:
        map = Map()
        map.read_from(map_path)
        game_map = GameMap(map)
        try:
            game_map.check_map()
        except LookupError as position:
            print('FAILED ' + str(position))
        else:
            print('OK')


def play_game(args):
    map = Map()
    map.read_from(args.map_path)
    positions = []
    if args.positions is not None:
        for position in args.positions:
            x, y = position[1:len(position) - 1].split(',')
            positions.append(Position(int(x), int(y)))
    game = Game([map], args.players, positions)
    game.start_game()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Videos to images')
    subparsers = parser.add_subparsers(title='modes')

    check_parser = subparsers.add_parser('check', help='check --map <map_path/name>')
    check_parser.add_argument('--map', type=str, nargs='+', action='store', dest='map_paths')
    check_parser.set_defaults(func=check_map)

    check_parser = subparsers.add_parser('game', help='\
    game --map <map_path> --players <players_count> --start_positions <positions as tuple>')
    check_parser.add_argument('--map', type=str, action='store', dest='map_path')
    check_parser.add_argument('--players', type=int, action='store', dest='players', default=1)
    check_parser.add_argument('--start_positions', type=str, nargs='+', action='store', dest='positions', default=None)
    check_parser.set_defaults(func=play_game)

    args = parser.parse_args()
    args.func(args)
