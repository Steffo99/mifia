from .death import Death
import typing
if typing.TYPE_CHECKING:
    from ..salemplayer import SalemPlayer
    from ..moment import Moment
    from ..salem import Judgement


class LynchedByTheTown(Death):
    def __init__(self, moment: "Moment", judgements: typing.Dict["SalemPlayer", "Judgement"]):
        super().__init__(moment)
        self.judgements = judgements
