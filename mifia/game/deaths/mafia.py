import typing
from .death import Death
if typing.TYPE_CHECKING:
    from ..moment import Moment
    from ..player import Player


class KilledByMafia(Death):
    def __init__(self, moment: Moment, killer: "Player"):
        super().__init__(moment)
        self.killer: "Player" = killer
