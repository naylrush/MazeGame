
from models.position import Position
from models.inventory import Inventory


total_ids = 0


def reset_player_total_ids():
    global total_ids
    total_ids = 0


class Player:
    def __init__(self, start_position=Position()):
        global total_ids
        self.id = total_ids
        total_ids += 1
        self.inventory = Inventory()
        self.stun = 0
        self.start_position = start_position
