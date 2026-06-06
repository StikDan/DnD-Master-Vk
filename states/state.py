from enum import Enum, auto


class State(Enum):
    NONE = auto()
    EXPLORATION = auto()
    COMBAT = auto()
    SOCIAL = auto()
    REST = auto()