from ..game import Game, _require_gamestate
from ..gamestate import GameState
from ..errors import InvalidStateError
from .deaths import LynchedByTheTown, LeftTheGame
from .moment import Moment
from .gamephase import GamePhase
from .judgement import Judgement
from . import events
import typing
if typing.TYPE_CHECKING:
    from .salemplayer import SalemPlayer
    from ..rolelist import RoleList
    from ..namelists import NameList


class Salem(Game):
    """A game mode where discussion takes place during the dawn, a player is voted during the day and a judgement
     is passed on them during the dusk.
     If they are found guilty, they are lynched, while if they are found innocent, nothing happens.
     In either case, the game moves on to the night, where nothing* happens.

     *Roles do not apply."""

    def __init__(self, rolelist: "RoleList", namelist: "NameList"):
        super().__init__(rolelist, namelist)
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

    @_require_gamestate(GameState.IN_PROGRESS)
    def end_dawn(self):
        if self.moment.phase != GamePhase.DAWN:
            raise InvalidStateError("Game is not GamePhase.DAWN!")
        previous_moment, self.moment = self.moment, Moment(GamePhase.DAY, self.moment.cycle)
        self._send_event(events.MomentChange(to=self.players.by_randomness(),
                                             previous_moment=previous_moment,
                                             new_moment=self.moment))
        for player in self.players.by_priority():
            player.role.on_day()
            if not player.connected:
                player.kill(LeftTheGame(self.moment))

    @_require_gamestate(GameState.IN_PROGRESS)
    def end_day(self):
        if self.moment.phase != GamePhase.DAY:
            raise InvalidStateError("Game is not GamePhase.DAY!")
        previous_moment, self.moment = self.moment, Moment(GamePhase.DUSK, self.moment.cycle)
        self._send_event(events.MomentChange(to=self.players.by_randomness(),
                                             previous_moment=previous_moment,
                                             new_moment=self.moment))
        for player in self.players.by_priority():
            player.role.on_dusk()
        self.on_trial = self.vote_order()[0]
        self._send_event(events.TrialStart(to=self.players.by_randomness(),
                                           on_trial=self.on_trial,
                                           vote_counts=self.vote_count()))

    @_require_gamestate(GameState.IN_PROGRESS)
    def end_dusk(self):
        if self.moment.phase != GamePhase.DUSK:
            raise InvalidStateError("Game is not GamePhase.DUSK!")
        previous_moment, self.moment = self.moment, Moment(GamePhase.NIGHT, self.moment.cycle)
        self._send_event(events.MomentChange(to=self.players.by_randomness(),
                                             previous_moment=previous_moment,
                                             new_moment=self.moment))
        for player in self.players.by_priority():
            player.role.on_night()
        vote_score = self.judgements_count()
        self._send_event(events.PassedJudgement(to=self.players.by_randomness(),
                                                on_trial=self.on_trial,
                                                judgements=self.judgements))
        if vote_score < 0:
            self.on_trial.kill(LynchedByTheTown(self.moment, self.judgements))
            self._send_event(events.Lynch(to=self.players.by_randomness(),
                                          dead=self.on_trial))
        self.on_trial = None

    @_require_gamestate(GameState.IN_PROGRESS)
    def end_night(self):
        if self.moment.phase != GamePhase.NIGHT:
            raise InvalidStateError("Game is not GamePhase.NIGHT!")
        previous_moment, self.moment = self.moment, Moment(GamePhase.DAWN, self.moment.cycle + 1)
        self._send_event(events.MomentChange(to=self.players.by_randomness(),
                                             previous_moment=previous_moment,
                                             new_moment=self.moment))
        for player in self.players.by_priority():
            player.role.on_dawn()
        self._victory_check()
