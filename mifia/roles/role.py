import typing
from ..objectives import Objective, NoObjective
if typing.TYPE_CHECKING:
    from ..player import Player


class Role:
    name: str = "[unnamed role]"
    default_priority: int = 0
    default_objective: typing.Type[Objective] = NoObjective

    def __init__(self, player: "Player"):
        self.player: "Player" = player
        self.priority: int = self.default_priority
        self.objective: Objective = self.default_objective(player)

    @property
    def game(self):
        """Shorthand for ``self.player.game``."""
        return self.player.game
