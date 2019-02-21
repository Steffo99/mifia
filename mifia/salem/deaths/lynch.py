from .death import Death
import typing
if typing.TYPE_CHECKING:
    from ...base import Player
    from ..moment import Moment
    from ..salem import Judgement


class LynchedByTheTown(Death):
    def __init__(self, moment: "Moment", judgements: typing.Dict["Player", "Judgement"]):
        super().__init__(moment)
        self.judgements = judgements
