from typing import TYPE_CHECKING, List

from ...objectives import PendingObjective
from ...roles.singletarget import SingleTarget
from ..death import Death
from ..events import PlayerDied
from .salemrole import SalemRole

if TYPE_CHECKING:
    from ...player import Player
    from ..moment import Moment


class KilledByMafia(Death):
    def __init__(self, moment: "Moment", killer: "Player"):
        super().__init__(moment)
        self.killer: "Player" = killer


class Mafioso(SalemRole, SingleTarget):
    """A role that can target another player and kill them at dawn."""

    name: str = "Mafioso"
    default_priority: int = 1

    # TODO: just for testing!
    default_objective = PendingObjective

    def __init__(self, player: "Player"):
        super().__init__(player)

    def on_dawn(self) -> None:
        self.player: "Player"

        if self.death:
            return
        if self.target is None:
            return
        self.target.role.die(KilledByMafia(self.game.moment, self.player))
        self.game.event_manager.post(PlayerDied(channel="main", dead=self.target))
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
        return "mafia"

    def available_chat_channels(self) -> List[str]:
        available = super().available_chat_channels()
        if self.alive:
            available.append("mafia")
        return available

    def get_valid_targets(self) -> List["Player"]:
        return [player for player in self.game.players.by_name() if player.role.death is None]
