import time as sys_time
from server.error import Error

__author__ = 'Wes'
class Game:
    INSTANCE = None

    def __init__(self, players, time=1440, rate=60):
        self.players = players
        self.time = time
        self.rate = rate
        self.points = 0
        Game.INSTANCE = self

    def advance(self, amount):
        self.time += amount

    def turn(self):
        if self.time == 0:
            for player in self.players:
                player.client_print("You scored " + str(self.points) + " points")
                player.client_print("Good game!")
                player.client.close()
        else:
            for player in self.players:
                player.turn(self)
            self.time += self.rate


    def add_player(self, player):
        self.players.append(player)

    @staticmethod
    def client_prompt(client, prompt, options=None, timeout=5 * 60):
        Game.client_print(client, prompt)

        if options is not None:
            Game.client_print(client, options)

        timeout_time = sys_time.time() + timeout
        output = ''
        while output == '':
            if timeout_time < sys_time.time():
                break
            output = client.read()
        if output == '':
            client.close()
            return Error.READING
        else:
            return output

    @staticmethod
    def client_print(client, to_print):
        client.write(to_print + "\n")