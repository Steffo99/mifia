import typing
if typing.TYPE_CHECKING:
    from .player import Player


class Command:
    def __init__(self, player: "Player"):
        self.player: "Player" = player
