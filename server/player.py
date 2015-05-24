from server.event import AntigravityEvent
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
        self.prompt("Those are your options, please select one")

    def prompt(self, prompt):
        self.print(prompt)
        # TODO setup prompting message on client

    def turn(self, game):
        for event in self.events:
            if random.randrange(100) < event.prob:
                event.get_input(self)

    def print(self, to_print):
        # TODO send a message to the client to print the message
        print("Sent this to",  self.name, "(" + self.client + ")" + ":", to_print)