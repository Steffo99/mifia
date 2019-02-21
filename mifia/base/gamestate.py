from enum import Enum


class GameState(Enum):
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
    IN_PROGRESS = "IN_PROGRESS"
    POST_GAME = "POST_GAME"
    ENDED = "ENDED"
