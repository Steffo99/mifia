from ..base import Game
from ..base.errors import InvalidStateError
from .deaths import LynchedByTheTown, LeftTheGame
from .moment import Moment, GamePhase
from .judgement import Judgement
import typing
if typing.TYPE_CHECKING:
    from multiprocessing import Queue
    from ..base import RoleList, NameList
    from .player import SalemPlayer


class Salem(Game):
    """A game mode where discussion takes place during the dawn, a player is voted during the day and a judgement
     is passed on them during the dusk.
     If they are found guilty, they are lynched, while if they are found innocent, nothing happens.
     In either case, the game moves on to the night, where nothing* happens.

     *Roles do not apply."""

    def __init__(self, rolelist: "RoleList", namelist: "NameList", outgoing_queue: "Queue"):
        super().__init__(rolelist, namelist, outgoing_queue)
        self.votes: typing.Dict[SalemPlayer, SalemPlayer] = {}
        self.on_trial: typing.Optional[SalemPlayer] = None
        self.judgements: typing.Dict[SalemPlayer, Judgement] = {}
        self.moment: Moment = None

    def vote_count(self) -> typing.Dict[SalemPlayer, int]:
        counts: typing.Dict[SalemPlayer, int] = {}
        for player in self.players.by_randomness():
            counts[player] = 0
        for player in self.votes:
            counts[player] += 1
        return counts

    def vote_order(self) -> list:
        counts = self.vote_count()
        return sorted(counts, key=lambda p: -counts[p])

    def judgements_count(self) -> int:
        score = 0
        for player in self.judgements:
            score += self.judgements[player].value
        return score

    def end_dawn(self):
        if self.moment is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.moment.phase != GamePhase.DAWN:
            raise InvalidStateError("Game is not GamePhase.DAWN!")
        self.moment = Moment(GamePhase.DAY, self.moment.cycle)
        for player in self.players.by_priority():
            player.role.on_day()
            if not player.connected:
                player.kill(LeftTheGame(self.moment))

    def end_day(self):
        if self.moment is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.moment.phase != GamePhase.DAY:
            raise InvalidStateError("Game is not GamePhase.DAY!")
        self.moment = Moment(GamePhase.DUSK, self.moment.cycle)
        for player in self.players.by_priority():
            player.role.on_dusk()
        self.on_trial = self.vote_order()[0]

    def end_dusk(self):
        if self.moment is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.moment.phase != GamePhase.DUSK:
            raise InvalidStateError("Game is not GamePhase.DUSK!")
        self.moment = Moment(GamePhase.NIGHT, self.moment.cycle)
        for player in self.players.by_priority():
            player.role.on_night()
        if self.judgements_count() < 0:
            self.on_trial.kill(LynchedByTheTown(self.moment, self.judgements))
        self.on_trial = None

    def end_night(self):
        if self.moment is None:
            raise InvalidStateError("Game is not GameState.IN_PROGRESS!")
        if self.moment.phase != GamePhase.NIGHT:
            raise InvalidStateError("Game is not GamePhase.NIGHT!")
        self.moment = Moment(GamePhase.DAWN, self.moment.cycle + 1)
        for player in self.players.by_priority():
            player.role.on_dawn()
