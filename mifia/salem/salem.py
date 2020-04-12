from typing import Optional, TYPE_CHECKING, Dict

from ..game import Game
from ..gamestate import GameState
from ..errors import InvalidStateError
from .death import Death
from .moment import Moment
from .gamephase import GamePhase
from .judgement import Judgement
from . import events

if TYPE_CHECKING:
    from ..player import Player
    from ..rolelist import RoleList
    from ..namelists import NameList


class LynchedByTheTown(Death):
    def __init__(self, moment: "Moment", judgements: Dict["Player", "Judgement"]):
        super().__init__(moment)
        self.judgements = judgements


class Salem(Game):
    """A game mode where discussion takes place during the dawn, a player is voted during the day and a judgement
     is passed on them during the dusk.
     If they are found guilty, they are lynched, while if they are found innocent, nothing happens.
     In either case, the game moves on to the night, where nothing* happens.

     *Roles do not apply."""

    def __init__(self, rolelist: "RoleList", namelist: "NameList"):
        super().__init__(rolelist, namelist)
        self.on_trial: Optional["Player"] = None
        self.moment: Moment = Moment(phase=GamePhase.NIGHT, cycle=0)

    def require_gamephase(self, *phases):
        if self.moment.phase not in phases:
            raise InvalidStateError(f"This method can be called only if phase is in {phases}, but game "
                                    f"currently is in {self.moment.phase}")

    @property
    def votes(self) -> Dict["Player", "Player"]:
        d: Dict["Player", "Player"] = {}
        for player in self.players.by_randomness():
            player: "Player"
            d[player] = player.role.vote
        return d

    def vote_count(self) -> Dict["Player", int]:
        self.require_gamestate(GameState.IN_PROGRESS)
        self.require_gamephase(GamePhase.DAY, GamePhase.DUSK, GamePhase.NIGHT)
        counts: Dict["Player", int] = {}
        for player in self.players.by_randomness():
            counts[player] = 0
        for player in self.votes.values():
            if player is None:
                continue
            counts[player] += 1
        return counts

    def vote_order(self) -> list:
        self.require_gamestate(GameState.IN_PROGRESS)
        self.require_gamephase(GamePhase.DAY, GamePhase.DUSK, GamePhase.NIGHT)
        counts = self.vote_count()
        return sorted(counts, key=lambda p: -counts[p])

    @property
    def judgements(self) -> Dict["Player", Judgement]:
        d = {}
        for player in self.players.by_randomness():
            d[player] = player.role.judgement
        return d

    def judgements_count(self) -> int:
        self.require_gamestate(GameState.IN_PROGRESS)
        self.require_gamephase(GamePhase.DUSK, GamePhase.NIGHT)
        score = 0
        for player in self.judgements:
            score += self.judgements[player].value
        return score

    def advance_phase(self):
        self.require_gamestate(GameState.IN_PROGRESS)
        if self.moment.phase == GamePhase.DAWN:
            self.end_dawn()
        elif self.moment.phase == GamePhase.DAY:
            self.end_day()
        elif self.moment.phase == GamePhase.DUSK:
            self.end_dusk()
        elif self.moment.phase == GamePhase.NIGHT:
            self.end_night()

    def end_dawn(self):
        self.require_gamestate(GameState.IN_PROGRESS)
        self.require_gamephase(GamePhase.DAWN)
        previous_moment, self.moment = self.moment, Moment(GamePhase.DAY, self.moment.cycle)
        self.event_manager.post(
            events.MomentChange(channel="main",
                                previous_moment=previous_moment,
                                new_moment=self.moment)
        )
        for player in self.players.by_priority():
            player.role.on_day()

    def end_day(self):
        self.require_gamestate(GameState.IN_PROGRESS)
        self.require_gamephase(GamePhase.DAY)
        previous_moment, self.moment = self.moment, Moment(GamePhase.DUSK, self.moment.cycle)
        self.event_manager.post(
            events.MomentChange(channel="main",
                                previous_moment=previous_moment,
                                new_moment=self.moment)
        )
        for player in self.players.by_priority():
            player.role.on_dusk()
        self.on_trial = self.vote_order()[0]
        self.event_manager.post(
            events.TrialStart(channel="main",
                              on_trial=self.on_trial,
                              votes=self.votes)
        )
        for player in self.players.by_priority():
            player.role.vote = None

    def end_dusk(self):
        self.require_gamestate(GameState.IN_PROGRESS)
        self.require_gamephase(GamePhase.DUSK)
        previous_moment, self.moment = self.moment, Moment(GamePhase.NIGHT, self.moment.cycle)
        self.event_manager.post(
            events.MomentChange(channel="main",
                                previous_moment=previous_moment,
                                new_moment=self.moment)
        )
        for player in self.players.by_priority():
            player.role.on_night()
        vote_score = self.judgements_count()
        self.event_manager.post(
            events.PassedJudgement(channel="main",
                                   on_trial=self.on_trial,
                                   judgements=self.judgements)
        )
        if vote_score < 0:
            self.on_trial.role.die(LynchedByTheTown(self.moment, self.judgements))
            self.event_manager.post(
                events.Lynch(channel="main",
                             dead=self.on_trial))
        self.on_trial = None
        for player in self.players.by_priority():
            player.role.judgement = None

    def end_night(self):
        self.require_gamestate(GameState.IN_PROGRESS)
        self.require_gamephase(GamePhase.NIGHT)
        previous_moment, self.moment = self.moment, Moment(GamePhase.DAWN, self.moment.cycle + 1)
        self.event_manager.post(
            events.MomentChange(channel="main",
                                previous_moment=previous_moment,
                                new_moment=self.moment)
        )
        for player in self.players.by_priority():
            player.role.on_dawn()
        self.victory_check()
