
import sys
from map_reader import *
from map_writer import *

if __name__ == "__main__":
    in_path = sys.argv[1]
    # write_map(read_map(in_path))
    out_path = './map_2.txt'
    write_map(read_map(in_path), out_path)
