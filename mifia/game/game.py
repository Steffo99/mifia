import uuid
import enum
import typing
from .player import Player

if typing.TYPE_CHECKING:
    from .user import User


class GameStates(enum.Enum):
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
    PRE_GAME = "PRE_GAME"
    IN_PROGRESS = "IN_PROGRESS"
    POST_GAME = "POST_GAME"
    ENDED = "ENDED"


class GamePhase(enum.Enum):
    DAY_DISCUSSION = "DAY_DISCUSSION"
    DAY_TRIAL = "DAY_TRIAL"
    DUSK = "DUSK"
    NIGHT = "NIGHT"
    DAWN = "DAWN"


class PlayersList(list):
    def j_public(self) -> list:
        return [player.j_public() for player in self]

    def user_join(self, user: "User") -> Player:
        pass

    def user_leave(self, user: "User") -> Player:
        pass


class MifiaGame:
    def __init__(self):
        self.guid = uuid.uuid4()
        self.state = GameStates.WAITING_FOR_PLAYERS
        self.players = PlayersList()

    def j_lobby(self) -> dict:
        return {
            "guid": self.guid,
            "state": self.state.value,
            "players": self.players.j_public()
        }

    def j_ingame(self) -> dict:
        return {
            "guid": self.guid,
            "state": self.state.value,
            "players": self.players.j_public(),

        }

