
class Inventory:
    def __init__(self, bullets=0):
        self.bullets = bullets
        self.max_bullets = 3

    def update_bullets(self):
        self.bullets = self.max_bullets


total_ids = 0


def reset_player_total_ids():
    global total_ids
    total_ids = 0


class Player:
    def __init__(self, id=None):
        if id is None:
            global total_ids
            self.id = total_ids
            total_ids += 1
        else:
            if not isinstance(id, int):
                raise Exception('id is not int')
            self.id = id
        self.inventory = Inventory()
        self.stun = 0
