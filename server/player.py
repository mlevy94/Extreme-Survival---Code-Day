__author__ = 'Wes'

from server.event import *
from enum import Enum
import random

class Player:
    name = ""
    type = PlayerType.NORMAL
    events = [AntigravityEvent()]

    def __init__(self, name, type = PlayerType.NORMAL, events = []):
        self.name = name
        self.type = type
        self.events = events

    def present(self, options):
        for option in options:
            self.print("*" + option)
        # TODO send select options message to client and return result

    def turn(self, game):
        for event in self.events:
            if random.randrange(100) < event.prob:
                event.present(self)
                event.run(game)

    def print(self, to_print):
        # TODO send a message to the client to print the message
        print("Sent this to " + self.name + ": " + to_print)

class PlayerType(Enum):
    NORMAL = 1
    FRONTEND = 2
    BACKEND = 3
    DESIGNER = 4