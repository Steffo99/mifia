from typing import Optional, List

from ..player import Player
from ..errors import GameError
from ..events import Event
from .role import Role


class InvalidTargetError(GameError):
    """The target that the player selected is invalid."""


class TargetChangeEvent(Event):
    """The target of a :class:`SingleTarget` role was changed."""

    def __init__(self,
                 channel: str,
                 source: Player,
                 target: Optional[Player]):
        super().__init__(channel)
        self.source: Player = source
        self.target: Optional[Player] = target


class SingleTarget(Role):
    """A role which can target another player."""

    def __init__(self, player: Player):
        super().__init__(player)
        self._target: Optional[Player] = None

    def get_valid_targets(self) -> List[Player]:
        """Return a :class:`list` of players in the game that can be targeted."""
        return [player for player in self.game.players.by_randomness()]

    def target_change_event_channel(self) -> str:
        """The channel in which the :class:`TargetChangeEvent` should be sent in."""
        return self.player.loopback_channel()

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self.player: Player

        if isinstance(value, Player):
            valid_targets = self.get_valid_targets()
            if value not in valid_targets:
                raise InvalidTargetError(f"{value} is not in the valid targets list.")
        elif value is None:
            pass
        else:
            raise TypeError("'target' must be set to a SalemPlayer instance.")

        self._target = value
        self.game.event_manager.post(
            TargetChangeEvent(
                channel=self.target_change_event_channel(),
                source=self.player,
                target=value
            )
        )
