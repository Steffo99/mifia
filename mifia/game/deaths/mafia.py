import typing
from .death import Death
if typing.TYPE_CHECKING:
    from ..player import Player


class KilledByMafia(Death):
    def __init__(self, moment: ..., killer: "Player"):
        super().__init__(moment)
        self.killer: "Player" = killer
