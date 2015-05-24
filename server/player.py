from server.event import AntigravityEvent
from server.game import Game
from server.playertype import PlayerType

__author__ = 'Wes'

import random

NORMAL = [AntigravityEvent()]
FRONTEND = []
BACKEND = []
DESIGNER = []
MASTER = NORMAL + FRONTEND + BACKEND + DESIGNER

class Player:
    def __init__(self, name, client, type = PlayerType.NORMAL):
        self.name = name
        self.client = client
        self.type = type
        if type == PlayerType.NORMAL:
            self.events = NORMAL
        elif type == PlayerType.FRONTEND:
            self.events = FRONTEND
        elif type == PlayerType.BACKEND:
            self.events = BACKEND
        elif type == PlayerType.DESIGNER:
            self.events = DESIGNER

    def present(self, options):
        for option in options:
            self.print("*" + option)
        return options[self.prompt("Those are your options, please select one (1 to " + str(len(options)) + ")") - 1]

    def prompt(self, prompt, options = None, timeout = 5 * 60):
        return Game.prompt(self.client, prompt, options, timeout)

    def turn(self, game):
        for event in self.events:
            if random.randrange(100) < event.prob:
                event.get_input(self)

    def print(self, to_print):
        self.client.write("print('" + to_print + "')")
        print("Sent this to",  self.name, "(" + self.client + ")" + ":", to_print)