from .event import Event
import typing
if typing.TYPE_CHECKING:
    from ..player import Player


class PlayerJoined(Event):
    def __init__(self, to: "Player", joiner: "Player"):
        super().__init__(to)
        self.joiner = joiner


class PlayerLeft(Event):
    def __init__(self, to: "Player", leaver: "Player"):
        super().__init__(to)
        self.leaver = leaver
