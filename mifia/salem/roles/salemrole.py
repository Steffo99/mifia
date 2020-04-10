from typing import *
from ...role import Role
from ...errors import GameError
from ..salemplayer import SalemPlayer
from ..events import TargetChangeEvent


class SalemRole(Role):
    def __init__(self, player: SalemPlayer):
        super().__init__(player)
        self.player: SalemPlayer

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


class InvalidTargetException(GameError):
    """The target that the player selected is invalid."""


class SingleTarget(Role):
    """A role which can target another player."""

    def __init__(self, player: SalemPlayer):
        super().__init__(player)
        self._target: Optional[SalemPlayer] = None

    def get_valid_targets(self) -> List[SalemPlayer]:
        """Return a :class:`list` of players in the game that can be targeted."""
        return [player for player in self.game.players.by_randomness()]

    def get_target_change_destination(self) -> List[SalemPlayer]:
        """Return a :class:`list` of players that should be notified of target changes."""
        self.player: SalemPlayer

        return [self.player]

    @property
    def target(self):
        return self._target
    
    @target.setter
    def target(self, value):
        self.player: SalemPlayer

        if isinstance(value, SalemPlayer):
            valid_targets = self.get_valid_targets()
            if value not in valid_targets:
                raise InvalidTargetException(f"{value} is not in the valid targets list.")
        elif value is None:
            pass
        else:
            raise TypeError("'target' must be set to a SalemPlayer instance.")

        self._target = value
        self.game.send_event(
            TargetChangeEvent(
                to=self.get_target_change_destination(),
                source=self.player,
                target=value
            )
        )
