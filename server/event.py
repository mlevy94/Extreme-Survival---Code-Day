__author__ = 'Wes'

class Event:
    prob = 0
    base_prob = 0
    dtime = 0
    options = []
    option_picked = None

    def __init__(self, options, baseprob = 0, dtime = 0):
        self.options = options
        self.prob = baseprob
        self.dtime = dtime

    def present(self, player):
        # Use the option_picked in run to do specific things
        self.option_picked = player.present(self.options)

    def run(self, game):
        # Subclasses should extend this for specific functionality
        self.prob = self.base_prob
        game.time += self.dtime