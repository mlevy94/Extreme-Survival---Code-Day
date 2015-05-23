from server.player import PlayerType

__author__ = 'Wes'

class Event:
    prob = 0
    base_prob = 0
    dtime = 0
    display = ""
    end_display = ""
    options = []
    option_picked = None
    player_type = PlayerType.NORMAL

    def __init__(self, display, end_display, options, baseprob = 0, dtime = 0):
        self.end_display = end_display
        self.display = display
        self.options = options
        self.prob = baseprob
        self.dtime = dtime

    def present(self, game, player):
        # Use the option_picked in run to do specific things
        if self.check(player):
            self.option_picked = player.present(self.options)
            self.run(game, player)


    def run(self, game, player):
        # Subclasses should extend this for specific functionality
        self.prob = self.base_prob
        game.time += self.dtime
        player.present()

    def check(self, player):
        # Subclass for specifics
        self.player_type == PlayerType.NORMAL or player.type == self.player_type

class AntigravityEvent(Event):
    def __init__(self):
        super().__init__("You have imported antigravity!", "", ["Try To Grab Computer", "Sit there"], 5)

    def run(self, game, player):
        if self.option_picked == "Try To Grab Computer":
            self.end_display = """You grabbed your computer and are now working on the cieling.
            Your productivity has increased. You gain 1 hour"""
            self.dtime = 60
        else:
            self.end_display = "You lost your computer. You spend 2 hours trying to get it back"
            self.dtime = -120
        super().run(game, player)
