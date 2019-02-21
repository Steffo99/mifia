from ...base import Role
import typing
if typing.TYPE_CHECKING:
    from ...base import Player


class SalemRole(Role):
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


class SingleTarget(Role):
    def __init__(self, player: "Player"):
        super().__init__(player)
        self._target: typing.Optional["Player"] = None

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value
