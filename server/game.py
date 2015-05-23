__author__ = 'Wes'
class Game:
    time = 1,440
    players = []
    def __init__(self, players):
        self.players = players

    def advance(self, amount):
        self.time += amount

    def turn(self):
        # TODO
        return
