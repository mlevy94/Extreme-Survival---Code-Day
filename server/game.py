__author__ = 'Wes'
class Game:
    def __init__(self, players, time = 1440):
        self.players = players
        self.time = time

    def advance(self, amount):
        self.time += amount

    def turn(self):
        for player in self.players:
            player.turn(self)

    def add_player(self, player):
        self.players.append(player)


