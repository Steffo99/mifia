import typing
from .death import Death
if typing.TYPE_CHECKING:
    from ...base import Player
    from ..moment import Moment


class KilledByMafia(Death):
    def __init__(self, moment: "Moment", killer: "Player"):
        super().__init__(moment)
        self.killer: "Player" = killer
