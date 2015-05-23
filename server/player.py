__author__ = 'Wes'

from server.event import *
from enum import Enum
import random

class Player:
    name = ""
    type = PlayerType.NORMAL
    events = [AntigravityEvent()]
    client = None

    def __init__(self, name, client, type = PlayerType.NORMAL, events = []):
        self.name = name
        self.client = client
        self.type = type
        self.events = events

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

class PlayerType(Enum):
    NORMAL = 1
    FRONTEND = 2
    BACKEND = 3
    DESIGNER = 4