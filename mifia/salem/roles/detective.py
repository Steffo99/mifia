from typing import TYPE_CHECKING, List

from ...objectives import PendingObjective
from ...roles.singletarget import SingleTarget
from ..events import Event
from .salemrole import SalemRole

if TYPE_CHECKING:
    from ...player import Player
    from ...roles.role import Role


class DetectiveRoleDiscovery(Event):
    """A :class:`Detective` has discovered another player's role."""
    def __init__(self, channel: str, role: "Role"):
        super().__init__(channel)
        self.role: "Role" = role


class Detective(SalemRole, SingleTarget):
    """A role that can target another player and kill them at dawn."""

    name: str = "Detective"
    default_priority: int = 0

    # TODO: just for testing!
    default_objective = PendingObjective

    def __init__(self, player: "Player"):
        super().__init__(player)

    def on_dawn(self) -> None:
        self.player: "Player"

        if self._death:
            return
        if self.target is None:
            return
        self.game.event_manager.post(DetectiveRoleDiscovery(channel=self.player.loopback_channel(),
                                                            role=self.target.role))
        self._target = None

    def on_day(self) -> None:
        pass

    def on_dusk(self) -> None:
        pass

    def on_night(self) -> None:
        pass

    def on_death(self) -> None:
        pass

    def target_change_event_channel(self) -> str:
        return self.player.loopback_channel()

    def available_chat_channels(self) -> List[str]:
        return super().available_chat_channels()

    def get_valid_targets(self) -> List["Player"]:
        return [player for player in self.game.players.by_name() if player.role.death is None]
