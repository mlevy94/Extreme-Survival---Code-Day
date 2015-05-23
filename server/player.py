__author__ = 'Wes'

from enum import Enum

class Player:
    type = PlayerType.NORMAL

    def __init__(self, type = PlayerType.NORMAL):
        self.type = type





class PlayerType(Enum):
    NORMAL = 1
    FRONTEND = 2
    BACKEND = 3
    DESIGNER = 4