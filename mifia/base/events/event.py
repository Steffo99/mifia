import typing
if typing.TYPE_CHECKING:
    from ..player import Player


class Event:
    def __init__(self, to: Player):
        self.to: Player = to