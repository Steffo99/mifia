from ...base import Death
import typing
if typing.TYPE_CHECKING:
    from ...base import Player, Moment
    from ..salem import Judgement


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
