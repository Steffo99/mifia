import typing
if typing.TYPE_CHECKING:
    from .player import Player
    from .events import Event


class Role:
    name: str = NotImplemented
    default_priority: int = NotImplemented

    def __init__(self, player: "Player"):
        self.player: "Player" = player
        self.priority: int = self.default_priority

    def on_event(self, event) -> "Event":
        """Triggered when an event is recieved from the game."""
        return event
