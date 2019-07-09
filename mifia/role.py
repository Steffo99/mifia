import typing
if typing.TYPE_CHECKING:
    from .player import Player
    from .objectives import Objective


class Role:
    name: str = NotImplemented
    default_priority: int = NotImplemented
    default_objective: "Objective" = NotImplemented

    def __init__(self, player: "Player"):
        self.player: "Player" = player
        self.priority: int = self.default_priority
        self.objective: "Objective" = self.default_objective

    @property
    def game(self):
        """Shorthand for ``self.player.game``."""
        return self.player.game
