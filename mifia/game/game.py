import uuid
import enum
import typing
import secrets
from .player import Player

if typing.TYPE_CHECKING:
    from .user import User
    from .presets import Preset
    from .namelists import NameList


class GameState(enum.Enum):
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


class GameError(Exception):
    pass


class InvalidStateError(GameError):
    pass


class InvalidPlayerCountError(GameError):
    pass


class PlayersList:
    def __init__(self):
        self.list: typing.List[Player] = []

    def by_priority(self) -> typing.List[Player]:
        return sorted(self.list, key=lambda p: p.role.priority)

    def by_name(self) -> typing.List[Player]:
        return sorted(self.list, key=lambda p: p.name)

    def by_randomness(self) -> typing.List[Player]:
        origin = self.list.copy()
        result = []
        for _ in origin:
            player = secrets.choice(origin)
            result.append(player)
            origin.remove(player)
        assert len(result) == len(self.list)
        return result

    def j_public(self) -> list:
        return [player.j_public() for player in self.by_name()]

    def __len__(self):
        return len(self.list)


class MifiaGame:
    def __init__(self, preset: "Preset", namelist: "NameList"):
        self.guid = uuid.uuid4()
        self.state: GameState = GameState.WAITING_FOR_PLAYERS
        self.phase: typing.Optional[GamePhase] = None
        self.players = PlayersList()
        self.preset: "Preset" = preset
        self.namelist: "NameList" = namelist

    def user_join(self, user: "User") -> Player:
        player = Player(self, user)
        self.players.list.append(player)
        return player

    def user_leave(self, user: "User") -> Player:
        raise NotImplementedError()  # TODO

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

    def pre_game(self):
        if self.state != GameState.WAITING_FOR_PLAYERS:
            raise InvalidStateError("Game is not GameState.WAITING_FOR_PLAYERS!")
        if not self.preset.validate_player_number(len(self.players)):
            raise InvalidPlayerCountError("Game has an invalid player count according to the preset")
        for player in self.players.by_randomness():
            player.assign_role(next(self.preset.generator))
            player.assign_name(next(self.namelist.generator))
