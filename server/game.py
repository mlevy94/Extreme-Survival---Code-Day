import time as sys_time
from server.error import Error

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

    @staticmethod
    def prompt(client, prompt, options = None, timeout = 5 * 60):
        client.write("prompt('" + prompt + "')")

        if options is not None:
            client.write("print('" + options + "')")

        start_time = sys_time.time()
        output = ''
        while output == '':
            if start_time + timeout > sys_time.time():
                break
            output = client.read()

        if output == '':
            client.close()
            return Error.READING
        else:
            return output

