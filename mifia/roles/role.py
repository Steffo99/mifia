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
        pass

    def on_day(self):
        pass

    def on_dusk(self):
        pass

    def on_night(self):
        pass

    def on_death(self):
        pass

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
