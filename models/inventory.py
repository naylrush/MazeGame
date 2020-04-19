
class Inventory:
    def __init__(self, has_key=False):
        self.bullets = 0
        self.max_bullets = 3
        self.has_key = has_key

    def empty(self):
        return self.bullets == 0 and not self.has_key

    def append(self, other):
        if other.has_key:
            self.has_key = True
        self.bullets += other.bullets
        if self.bullets > self.max_bullets:
            self.bullets = self.max_bullets

    def update_bullets(self):
        self.bullets = self.max_bullets

    def reset(self):
        self.__init__()
