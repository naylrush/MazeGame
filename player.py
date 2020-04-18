
class Inventory:
    def __init__(self, bullets=0):
        self.bullets = bullets
        self.max_bullets = 3

    def update_bullets(self):
        self.bullets = self.max_bullets

    def reset(self):
        self.__init__()


total_ids = 0


def reset_player_total_ids():
    global total_ids
    total_ids = 0


class Player:
    def __init__(self):
        global total_ids
        self.id = total_ids
        total_ids += 1
        self.inventory = Inventory()
        self.stun = 0
