
import sys
from map import *

if __name__ == "__main__":
    in_path = sys.argv[1]
    out_path = './map_2.txt'
    map = Map()
    map.read_from(in_path)
    map.write_to()
    # map.write_to(out_path)
