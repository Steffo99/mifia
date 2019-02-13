from .game import Game
import enum
import typing
from ..deaths import LynchedByTheTown
if typing.TYPE_CHECKING:
    from multiprocessing import Queue
    from ..player import Player
    from ..rolelists import RoleList
    from ..namelists import NameList


class Judgement(enum.IntEnum):
    GUILTY = -1
    ABSTAINED = 0
    INNOCENT = 1


class Salem(Game):
    """A game mode where discussion takes place during the dawn, a player is voted during the day and a judgement is passed on them during the dusk.
     If they are found guilty, they are lynched, while if they are found innocent, nothing happens.
     In either case, the game moves on to the night, where nothing* happens.

     *Roles do not apply."""

    def __init__(self, rolelist: "RoleList", namelist: "NameList", outgoing_queue: "Queue"):
        super().__init__(rolelist, namelist, outgoing_queue)
        self.votes: typing.Dict[Player, Player] = {}
        self.on_trial: typing.Optional[Player] = None
        self.judgements: typing.Dict[Player, Judgement] = {}

    def vote_count(self) -> typing.Dict[Player, int]:
        counts: typing.Dict[Player, int] = {}
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

    def _end_day(self):
        super()._end_day()
        self.on_trial = self.vote_order()[0]

    def _end_dusk(self):
        super()._end_dusk()
        if self.judgements_count() < 0:
            self.on_trial.kill(LynchedByTheTown(self.moment, self.judgements))
        self.on_trial = None
