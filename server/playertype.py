from enum import Enum

__author__ = 'Wes'

class PlayerType(Enum):
    INVALID = -1
    NORMAL = 0
    FRONTEND = 1
    BACKEND = 2
    DESIGNER = 3

    @staticmethod
    def from_string(str):
        type = str.lower
        if type == 'normal':
            return PlayerType.NORMAL
        if type == 'frontend':
            return PlayerType.FRONTEND
        elif type == 'backend':
            return PlayerType.BACKEND
        elif type == 'designer':
            return PlayerType.DESIGNER

    @staticmethod
    def get_types_str():
        return ['normal', 'frontend', 'backend', 'designer']
