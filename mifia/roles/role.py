import typing
from ..utils.limitedlist import LimitedList
if typing.TYPE_CHECKING:
    from mifia.player import Player


class Role:
    name: str = NotImplemented
    default_priority: int = NotImplemented

    def __init__(self, player: "Player"):
        self.player: "Player" = player
        self.priority: int = self.default_priority

    def on_dawn(self):
        """Triggered when dawn starts."""

    def on_day(self):
        """Triggered when day starts."""

    def on_dusk(self):
        """Triggered when dusk starts."""

    def on_night(self):
        """Triggered when night starts."""

    def on_death(self):
        """Triggered after the player dies."""

    def on_event(self):
        """Triggered when an event is recieved from the game."""

    def on_message(self):
        pass


class SingleTargetRole(Role):
    def __init__(self, player: "Player"):
        super().__init__(player)
        self.target: "Player" = None


class MultipleTargetRole(Role):
    max_targets = NotImplemented

    def __init__(self, player: "Player"):
        super().__init__(player)
        self.targets: LimitedList = LimitedList(max_length=self.max_targets)
