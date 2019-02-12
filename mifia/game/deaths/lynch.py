from .death import Death
import typing
if typing.TYPE_CHECKING:
    from ..player import Player
    from ..games.salem import Judgement
    from ..moment import Moment


class LynchedByTheTown(Death):
    def __init__(self, moment: "Moment", judgements: typing.Dict["Player", "Judgement"]):
        super().__init__(moment)
        self.judgements = judgements

    def j(self):
        # FIXME: ensure self.judgements is jsonable
        return {
            **super().j(),
            "judgements": self.judgements
        }
