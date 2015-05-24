import random
from server.error import Error
from server.playertype import PlayerType

__author__ = 'Wes'

COMPUTERS = ['computer', 'laptop', 'desktop']
GET = ['get', 'grab']
NOTHING = ['sit', 'do nothing', 'no action', 'ignore', 'nothing']
WORK = ['work', 'code', 'design']
YES = ['yes', 'accept', 'y']
NO = ['no', 'reject', 'n']
REST = ['nap', 'rest', 'sleep']
DRINK = ['drink']
ENERGY_DRINK = ['energy', 'redbull', 'red bull', 'monster', 'coffee']
SEARCH = ['search', 'download', 'google', 'online', 'find API']
GOOD =  ['q','z','m','p','0','2']
INVESTIGATE = ['check', 'investigate', 'find']
HIDE = ['hide']

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
                    continue
        return acc >= len(self.all_required)

class Event:
    base_prob = 0

    def __init__(self, display, end_display, options, player_type=PlayerType.NORMAL, drate=1):
        self.end_display = end_display
        self.display = display
        self.option_index = -1
        self.options = options
        self.prob = self.base_prob
        self.drate = drate
        self.player_type = player_type

    def present(self, game, player):
        # Use the option_picked in run to do specific things
        if self.check(player):
            str = player.present(list(map(lambda option: option.str, self.options)))
            self.option_picked(str, game, player)

    def get_input(self, game, player):
        if self.check(player):
            player.client_print(self.display)
            response = player.client_prompt("Enter a response to event")
            if response != Error.READING:
                self.option_picked(response, game, player)
            else:
                print(Error.READING)


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
        game.rate /= self.drate

    def check(self, player):
        # Subclass for specifics
        return True

class AntigravityEvent(Event):
    base_prob = 5

    def __init__(self):
        super().__init__("""Type type type, click click click. The keys pound down on the keyboard as you slowly whittle away the hours masterfully crafting code.
        Then into your mind pops a rumor you heard once, that if you told the interpreter to input antigravity that you would be taken to a comic site.
        Bored and at wits end, you decide that you deserve a little break. You type with a renewed vigor, placing in 'input antigravity.
        A loud humming fills the room, as you suddenly feel like your falling' up?""", "", [Option([GET, COMPUTERS], "Grab your computer"), Option([NOTHING], "Do nothing")])

    def run(self, game, player):
        if self.option_picked == 0:
            self.end_display = """You grab your computer as you start to slowly float away towards the ceiling.
            You just float on, it's alright already, because you'll just float on the ceiling.
            A change of perspective is all you needed, enjoy your time up here.
            Your productivity has increased. Your productivity doubles"""
            self.drate = 2
        else:
            if random.uniform(1,1000) < 650:
                self.end_display = """You're taken by surprise as gravity suddenly reverses itself.
                In your shock you hit the ceiling as your computer hits it further than you would appreciate.
                After a bit of moaning and groaning, you figure that the only way down is with the same power that got you up here,
                 and you start to do the most awkward turtle crawly you can towards your computer. Swim my weird turtle thing, swim..
                 Your productivity halves"""
                self.drate = 1/2
            else:
                self.end_display = """No not you, your stuff. You watch as your computer finishes interpreting
                the code and begins to fly up, up, and away from you.
                Well then, your computer is on the ceiling and your still on the floor.
                What now smart guy? Your productivity has been fourthed"""
                self.drate = 1/4
        super().run(game, player)

class TiredEvent(Event):
    def __init__(self):
        super().__init__("""As you work you begin to feel your mind lagging behind your fingers. A yawn escapes your lips as you stretch your back.
        The call of sleep enters your mind as you consider stopping to rest your eyes.""", "", [Option([REST], "Take a nap"), Option([NOTHING], "Ignore"), Option([DRINK, ENERGY_DRINK], "Have Energy Drink")], 5)

    def run(self, game, player):
        if self.option_picked == 0:
            self.end_display = """Giving into your desires you wander off to find a comfortable corner or unused chair to take a nap. Your productivity doubles"""
            self.drate = 2
        elif self.option_picked == 1:
            self.end_display = """You choose to work on in the tired state.
            This has its consequences (planned feature)"""
            self.drate = 0
            # Redirect to next option soon
        else:
            self.end_display = "You are fully charged. Be careful not to overdo the drinks (planned feature)"
            self.drate = 1.5
            # raise bladder probability and increrase health problems.
        super().run(game, player)


class NewCodeNeeded(Event):
    def __init__(self):
        super().__init__("""As you work you run into an issue, but you don't have any code to fix
        the issue. You think it might be a
        minor issue, but you're not certain.  You:""", [Option([WORK], "Work on it"), Option([NOTHING], "Ignore"), Option([SEARCH], "Find Code Online")], 5)

    def run(self, game, player):
        if self.option_picked == 0:
            if random.uniform(0, 1000) < 700:
                self.end_display = """The Code Works. Your productivity increases"""
                self.drate = 1.5
            else:
                self.end_display = """There are bugs. They took time to fix
                Your productivity is halfed"""
                self.drate = 1/2
        else:
            player.client_print("""ignore it. After coding for a while longer however, you discover
            that it was in fact an important piece of code. You have to write it anyways,
            killing time fixing all the bugs that the new code caused. Your productivity is a third of what it was""")
            self.drate = 1/1.5
        super().run(game, player)

class NewMember(Event):
    def __init__(self):
        super().__init__("Another Member wishes to join your team", "", [Option([YES], "Accept"), Option([NO], "Reject")], 5)

    def run(self, game, player):
        if self.option_picked == 0:
            if random.uniform(0, 10) < 3:
                self.end_display = """The new member is a genius. He/She saves quadruples your productivity"""
                self.drate = 4
            elif random.uniform(0, 10) < 7:
                self.end_display = """The new guy is good. He/She doubles your productivity"""
                self.drate = 2
            else:
                self.end_display = """The new guy is distracting. He/She halves your productivity"""
                self.drate = 1/2
        else:
            self.end_display = "He joins another team. You continued with your work."
            self.drate = 1
        super().run(game, player)

class ForgotPassword(Event):
    def __init__(self):
        super().__init__("""As you rouse your computer from its deep slumber, it presents you with a familiar screen:
            a red background, with some text informing you that your device is locked. You move your cursor over the familiar dialogue box, and'""", "", [Option([GOOD], "Success")], 5)

    def run(self, game, player):
        if self.option_picked == 0:
            self.end_display = """You log in...Moving on to more important things"""
            #break
        else:
            self.end_display = """Your computer thinks for a moment then responds with a large 'Password Incorrect' message.
            Huh? That's odd, you know your own password, and you've used the same one since high school'
            You should probably have changed it since then but you know, I'm sorry, knew your password.
            Well not much left to do but start guessing."""
            self.drate = 1/1.25
            # TODO repeat request for password
        super().run(game, player)

class Shaking(Event):
    def __init__(self):
        super().__init__("""You feel a slight tremor""", "", [Option([NOTHING], "Ignore"), Option([INVESTIGATE], "Investigate"), Option([HIDE], "Hide")], 5)

    def run(self, game, player):
        if self.option_picked == 0:
            if random.uniform(1,1000)< 400:
                def __init__(self):
                    super().__init__("""A Pterodactyl breaks in through the roof""", "", [Option([NOTHING], "Ignore"), Option([HIDE], "Hide")], 5)
            elif random.uniform(1,1000) < 400:
                self.end_display = """An earthquake causes the roof to fall. Productivity is halved trying to find new place to code"""
                self.drate = 2
            else:
                self.end_display = """It was the constuction work, continue to code."""
        elif self.option_picked == 1:
            if random.uniform(1,1000)< 400:
                self.end_display = None # TODO insert Scenario
                self.drate = 1/1.5
            else:
                self.end_display = None # TODO insert scenario
        else:
            if random.uniform(1,1000)< 400:
                self.end_display = """Wasted half hour hiding from the sound of the construction work.
                Assured of safety, you continue work"""
                self.drate = 1/1.5
            else:
                self.end_display = """Your preparedness for the earthquake saved you valuable time. Continue to code"""
        super().run(game, player)
