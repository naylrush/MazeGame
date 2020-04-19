
class Inventory:
    def __init__(self, bullets=0):
        self.bullets = bullets
        self.max_bullets = 3

    def update_bullets(self):
        self.bullets = self.max_bullets

    def reset(self):
        self.__init__()
