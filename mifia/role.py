import typing
if typing.TYPE_CHECKING:
    from .player import Player
    from mifia.events import Event


class Role:
    name: str = NotImplemented
    default_priority: int = NotImplemented

    def __init__(self, player: "Player"):
        self.player: "Player" = player
        self.priority: int = self.default_priority
