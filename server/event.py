from server.playertype import PlayerType

__author__ = 'Wes'

COMPUTERS = ['computer', 'laptop', 'desktop']
GET = ['get', 'grab']
NOTHING = ['sit', 'do nothing', 'no action']

class Option:

    def __init__(self, all_required, str):
        self.all_required = all_required
        self.str = str

    def check(self, str):
        acc = 0
        for required in self.all_required:
            for required_str in required:
                if required_str in str:
                    acc += 1
        return acc >= len(self.all_required)

class Event:
    base_prob = 0

    def __init__(self, display, end_display, options, player_type = PlayerType.NORMAL, dtime = 0):
        self.end_display = end_display
        self.display = display
        self.option_index = -1
        self.options = options
        self.prob = self.base_prob
        self.dtime = dtime
        self.player_type = player_type

    def present(self, game, player):
        # Use the option_picked in run to do specific things
        if self.check(player):
            str = player.present(map(lambda option: option.str, self.options))
            self.option_picked(str, game, player)

    def get_input(self, game, player):
        if self.check(player):
            player.print(self.display)
            self.option_picked(player.prompt("Enter a response to event"), game, player)


    def option_picked(self, str, game, player):
        for option in self.options:
            if option.check(str):
                self.option_index = self.options.index(option)
            if self.option_index == -1:
                self.present(game, player)
            else:
                self.run(game, player)

    def run(self, game, player):
        # Subclasses should extend this for specific functionality
        self.prob = self.base_prob
        game.time += self.dtime
        player.present()

    def check(self, player):
        # Subclass for specifics
        return True

class AntigravityEvent(Event):
    base_prob = 5

    def __init__(self):
        super().__init__("You have imported antigravity!", "", [Option([GET, COMPUTERS], "Grab your computer"), Option([NOTHING], "Do nothing")])

    def run(self, game, player):
        if self.option_picked == 0:
            self.end_display = """You grabbed your computer and are now working on the ceiling.
            Your productivity has increased. You gain 1 hour"""
            self.dtime = 60
        else:
            self.end_display = "You lost your computer. You spend 2 hours trying to get it back"
            self.dtime = -120
        super().run(game, player)

class TiredEvent(Event):
   def __init__(self):
        super().__init__("Feeling Tired", "", [Option([REST], "Rest"), Option([NOTHING], "Ignore"), Option([ENERGY, DRINK, REDBULL, COFFEE], "Have Energy Drink")], 5)

    def run(self, game, player):
        if self.option_picked == 0:
            self.end_display = """You are no longer tired. The sleep cost you 1 hour of coding time"""
            self.dtime = -60
        else if:
            self.end_display = """You choose to work on in the tired state.
            This has its consequences"""
            self.dtime = 0
            # Redirect to next option soon
        else:
            self.end_display = "You are fully charged. Be careful not to overdo the drinks"
            self.dtime = 30
            # raise bladder probability and increrase health problems.
        super().run(game, player)

class TiredEvent(Event):
   def __init__(self):
        super().__init__("Feeling Tired", "", [Option([REST, NAP], "Rest"), Option([NOTHING, IGNORE], "Ignore"), Option([ENERGY, DRINK, REDBULL, COFFEE], "Have Energy Drink")], 5)

    def run(self, game, player):
        if self.option_picked == 0:
            self.end_display = """You are no longer tired. The sleep cost you 1 hour of coding time"""
            self.dtime = -60
        else if self.option_picked == 1:
            self.end_display = """You choose to work on in the tired state.
            This has its consequences"""
            self.dtime = 0
            # Redirect to next option soon
        else:
            self.end_display = "You are fully charged. Be careful not to overdo the drinks"
            self.dtime = 30
            # raise bladder probability and increrase health problems.
        super().run(game, player)

class NewCodeNeeded(Event):
   def __init__(self):
        super().__init__("New Code Snippet Needed", "", [Option([Work, Code], "Work on it"), Option([NOTHING,IGNORE], "Ignore"), Option([DOWNLOAD, SEARCH, ONLINE, FIND], "Find Code Online")], 5)

    def run(self, game, player):
        if self.option_picked == 0:
            #random option
            self.end_display = """The Code Works. You save half an hour"""
            self.dtime = 30
            #not working
            self.end_display = """There are bugs. They took time to fix
            You lost an Hour"""
            self.dtime = -60
        else ifself.option_picked == 1:
            self.end_display = """Work grings to a halt for two hours due to lack of API's"""
            self.dtime = -120
            # Redirect to next option soon
        else:
            #Random Option
            self.end_display = "You found useful code online. It saves you 2 hours"
            self.dtime = 120
            # small probability
            self.end_display = "File filled with viruses. All data Corrupted. Must start over."
        super().run(game, player)

 class NewMember(Event):
   def __init__(self):
        super().__init__("Another Member wishes to join your team", "", [Option([ACCEPT, YES, Y, OK], "Accept"), Option([REJECT, NO, N], "Reject"), 5)

    def run(self, game, player):
        if self.option_picked == 0:
            #random option
            self.end_display = """The new member is a genius. He saves two hours"""
            self.dtime = 120
            #2
            self.end_display = """The new guy is good. One hour is saved"""
            self.dtime = 60
            #3
            self.end_display = """The new guy is distracting. One hour lost"""
            self.dtime = -60
        else:
            self.end_display = "He joins another team. You continued with your work." \
                               ""
            self.dtime = 0
        super().run(game, player)