import typing
from ...base import Death
if typing.TYPE_CHECKING:
    from ...base import Moment, Player


class KilledByMafia(Death):
    def __init__(self, moment: Moment, killer: "Player"):
        super().__init__(moment)
        self.killer: "Player" = killer
