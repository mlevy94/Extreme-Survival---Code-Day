from server.event import *
from server.game import Game
from server.playertype import PlayerType

__author__ = 'Wes'

import random

class Player:
    def __init__(self, name, client, type=PlayerType.NORMAL):
        self.name = name
        self.client = client
        self.type = type
        self.events = [AntigravityEvent(), TiredEvent(), NewCodeNeeded(), NewMember(), ForgotPassword(), Shaking()]
        self.drate = 0

    def present(self, options):
        for option in options:
            self.client_print("*" + option)
        return options[self.client_prompt("Those are your options, please select one (1 to " + str(len(options)) + ")") - 1]

    def client_prompt(self, prompt, options = None, timeout = 5 * 60):
        return Game.client_prompt(self.client, prompt, options, timeout)

    def turn(self):
        for event in self.events:
            if random.randrange(100) < event.prob:
                event.get_input(self)
            event.prob += 1
        return self

    def client_print(self, to_print):
        Game.client_print(self.client, to_print)
        print("Sent this to",  self.name, ":", to_print)