from .requiregamephase import require_gamephase
from ..game import Game
from ..requiregamestate import require_gamestate
from ..gamestate import GameState
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

    @require_gamephase(GamePhase.DAY, GamePhase.DUSK, GamePhase.NIGHT)
    def vote_count(self) -> typing.Dict[SalemPlayer, int]:
        counts: typing.Dict[SalemPlayer, int] = {}
        for player in self.players.by_randomness():
            counts[player] = 0
        for player in self.votes:
            counts[player] += 1
        return counts

    @require_gamephase(GamePhase.DAY, GamePhase.DUSK, GamePhase.NIGHT)
    def vote_order(self) -> list:
        counts = self.vote_count()
        return sorted(counts, key=lambda p: -counts[p])

    @require_gamephase(GamePhase.DUSK, GamePhase.NIGHT)
    def judgements_count(self) -> int:
        score = 0
        for player in self.judgements:
            score += self.judgements[player].value
        return score

    @require_gamestate(GameState.IN_PROGRESS)
    @require_gamephase(GamePhase.DAWN)
    def end_dawn(self):
        previous_moment, self.moment = self.moment, Moment(GamePhase.DAY, self.moment.cycle)
        self._send_event(events.MomentChange(to=self.players.by_randomness(),
                                             previous_moment=previous_moment,
                                             new_moment=self.moment))
        for player in self.players.by_priority():
            player.role.on_day()
            if not player.connected:
                player.die(LeftTheGame(self.moment))

    @require_gamestate(GameState.IN_PROGRESS)
    @require_gamephase(GamePhase.DAY)
    def end_day(self):
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

    @require_gamestate(GameState.IN_PROGRESS)
    @require_gamephase(GamePhase.DUSK)
    def end_dusk(self):
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
            self.on_trial.die(LynchedByTheTown(self.moment, self.judgements))
            self._send_event(events.Lynch(to=self.players.by_randomness(),
                                          dead=self.on_trial))
        self.on_trial = None

    @require_gamestate(GameState.IN_PROGRESS)
    @require_gamephase(GamePhase.NIGHT)
    def end_night(self):
        previous_moment, self.moment = self.moment, Moment(GamePhase.DAWN, self.moment.cycle + 1)
        self._send_event(events.MomentChange(to=self.players.by_randomness(),
                                             previous_moment=previous_moment,
                                             new_moment=self.moment))
        for player in self.players.by_priority():
            player.role.on_dawn()
        self._victory_check()
