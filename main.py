
import sys
from map import Map
from game import Game

from position import Position

if __name__ == "__main__":
    in_path = sys.argv[1]
    map = Map()
    map.read_from(in_path)
    # game = Game([map], 1, [Point(0, 2)])
    game = Game([map], 1)
    game.start_game()
