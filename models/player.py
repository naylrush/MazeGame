
from copy import deepcopy
from models.inventory import Inventory
from models.position import Position


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
        self.ghost_inventory = []
        self.stun = 0
        self.sleep_times = []
        self.field_id = [0]
        self.start_position = start_position

    def sleep_for(self, duration):
        assert isinstance(duration, int)
        self.sleep_times.append(duration)
        self.ghost_inventory.append(deepcopy(self.inventory))

    def is_sleeping(self):
        return len(self.sleep_times) == 0 and self.sleep_times[-1] > 0

    def wake_up(self):
        self.stun = 0
        self.sleep_times.pop(-1)
        self.ghost_inventory.pop(-1)
