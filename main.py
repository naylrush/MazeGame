
import sys
from map import *

if __name__ == "__main__":
    in_path = sys.argv[1]
    out_path = './map_2.txt'
    map = Map()
    map.read_from(in_path)
    map.write_to()
    print(map.has_route_from(Point(0, 0)))
    # map.write_to(out_path)
