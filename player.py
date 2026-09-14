class Player:
    def __init__(self, name, is_human=True):
        self.name = name
        self.is_human = is_human
        self.score = 0

    def add_pair(self):
        self.score += 1