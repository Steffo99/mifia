from enum import Enum


class GameState(Enum):
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
    IN_PROGRESS = "IN_PROGRESS"
    ENDED = "ENDED"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.value}"
