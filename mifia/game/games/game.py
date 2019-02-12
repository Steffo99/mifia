import uuid
import enum
import typing
from ..player import Player
from ..playerlist import PlayersList
from ..errors import InvalidStateError, InvalidPlayerCountError

if typing.TYPE_CHECKING:
    from mifia.game.user import User
    from mifia.game.rolelists import RoleList
    from mifia.game.namelists import NameList


class GameState(enum.Enum):
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
    IN_PROGRESS = "IN_PROGRESS"
    POST_GAME = "POST_GAME"
    ENDED = "ENDED"


class GamePhase(enum.Enum):
    DAY = "DAY"
    DUSK = "DUSK"
    NIGHT = "NIGHT"
    DAWN = "DAWN"


class Game:
    def __init__(self, rolelist: "RoleList", namelist: "NameList"):
        self.guid = uuid.uuid4()
        self.state: GameState = GameState.WAITING_FOR_PLAYERS
        self.phase: typing.Optional[GamePhase] = None
        self.players = PlayersList()
        self.rolelist: "RoleList" = rolelist
        self.namelist: "NameList" = namelist

    def user_join(self, user: "User") -> Player:
        player = Player(self, user)
        self.players.list.append(player)
        return player

    def user_leave(self, user: "User") -> Player:
        pass  # TODO

    def j_lobby(self) -> dict:
        return {
            "guid": self.guid,
            "state": self.state.value,
            "players_qty": len(self.players)
        }

    def j_ingame(self) -> dict:
        return {
            "guid": self.guid,
            "state": self.state.value,
            "players": self.players.j_public(),
        }

    def start_game(self):
        if self.state != GameState.WAITING_FOR_PLAYERS:
            raise InvalidStateError("Game is not GameState.WAITING_FOR_PLAYERS!")
        if not self.rolelist.validate_player_number(len(self.players)):
            raise InvalidPlayerCountError("Game has an invalid player count according to the preset")
        for player in self.players.by_randomness():
            player.assign_role(next(self.rolelist.generator))
            player.assign_name(next(self.namelist.generator))
        self.phase = GamePhase.DAWN
        self.state = GameState.IN_PROGRESS

    def advance_phase(self):
        if self.phase is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        elif self.phase == GamePhase.DAY:
            self._end_day()
        elif self.phase == GamePhase.DUSK:
            self._end_dusk()
        elif self.phase == GamePhase.NIGHT:
            self._end_night()
        elif self.phase == GamePhase.DAWN:
            self._end_dawn()
        else:
            raise InvalidStateError("Game is in an invalid phase!")

    def _end_dawn(self):
        if self.phase is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.phase != GamePhase.DAWN:
            raise InvalidStateError("Game is not GamePhase.DAWN!")
        self.phase = GamePhase.DAY
        for player in self.players.by_priority():
            player.role.on_day()

    def _end_day(self):
        if self.phase is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.phase != GamePhase.DAY:
            raise InvalidStateError("Game is not GamePhase.DAY!")
        self.phase = GamePhase.DUSK
        for player in self.players.by_priority():
            player.role.on_dusk()

    def _end_dusk(self):
        if self.phase is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.phase != GamePhase.DUSK:
            raise InvalidStateError("Game is not GamePhase.DUSK!")
        self.phase = GamePhase.NIGHT
        for player in self.players.by_priority():
            player.role.on_night()

    def _end_night(self):
        if self.phase is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.phase != GamePhase.NIGHT:
            raise InvalidStateError("Game is not GamePhase.NIGHT!")
        self.phase = GamePhase.DAWN
        for player in self.players.by_priority():
            player.role.on_dawn()
