import uuid
import typing

from mifia.game.moment import GameState, GamePhase
from ..player import Player
from ..playerlist import PlayersList
from ..errors import InvalidStateError, InvalidPlayerCountError
from ..deaths import LeftTheGame
from ..moment import Moment

if typing.TYPE_CHECKING:
    from ..user import User
    from ..rolelists import RoleList
    from ..namelists import NameList


class Game:
    def __init__(self, rolelist: "RoleList", namelist: "NameList"):
        self.guid = uuid.uuid4()
        self.state: GameState = GameState.WAITING_FOR_PLAYERS
        self.moment: Moment = None
        self.players = PlayersList()
        self.rolelist: "RoleList" = rolelist
        self.namelist: "NameList" = namelist

    def user_join(self, user: "User") -> Player:
        player = Player(self, user)
        self.players.list.append(player)
        return player

    def user_leave(self, user: "User"):
        for player in self.players.by_name():
            if player.user == user:
                player.connected = False

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
        self.moment = Moment(GamePhase.NIGHT, 0)
        self.state = GameState.IN_PROGRESS

    def advance_phase(self):
        if self.moment is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        elif self.moment.phase == GamePhase.DAY:
            self._end_day()
        elif self.moment.phase == GamePhase.DUSK:
            self._end_dusk()
        elif self.moment.phase == GamePhase.NIGHT:
            self._end_night()
        elif self.moment.phase == GamePhase.DAWN:
            self._end_dawn()
        else:
            raise InvalidStateError("Game is in an invalid phase!")

    def _end_dawn(self):
        if self.moment is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.moment.phase != GamePhase.DAWN:
            raise InvalidStateError("Game is not GamePhase.DAWN!")
        self.moment = Moment(GamePhase.DAY, self.moment.cycle)
        for player in self.players.by_priority():
            player.role.on_day()
            if not player.connected:
                player.kill(LeftTheGame(self.moment))

    def _end_day(self):
        if self.moment is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.moment.phase != GamePhase.DAY:
            raise InvalidStateError("Game is not GamePhase.DAY!")
        self.moment = Moment(GamePhase.DUSK, self.moment.cycle)
        for player in self.players.by_priority():
            player.role.on_dusk()

    def _end_dusk(self):
        if self.moment is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.moment.phase != GamePhase.DUSK:
            raise InvalidStateError("Game is not GamePhase.DUSK!")
        self.moment = Moment(GamePhase.NIGHT, self.moment.cycle)
        for player in self.players.by_priority():
            player.role.on_night()

    def _end_night(self):
        if self.moment is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.moment.phase != GamePhase.NIGHT:
            raise InvalidStateError("Game is not GamePhase.NIGHT!")
        self.moment = Moment(GamePhase.DAWN, self.moment.cycle + 1)
        for player in self.players.by_priority():
            player.role.on_dawn()
