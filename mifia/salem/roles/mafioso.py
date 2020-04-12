from typing import TYPE_CHECKING, List

from ...objectives import PendingObjective
from ...roles.singletarget import SingleTarget
from ..death import Death
from ..events import PlayerDied
from .salemrole import SalemRole

if TYPE_CHECKING:
    from ..salemplayer import Player
    from ..moment import Moment
    from ..salemplayer import SalemPlayer


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

    def __init__(self, player: "SalemPlayer"):
        super().__init__(player)

    def on_dawn(self):
        self.player: SalemPlayer

        if self.player.death:
            return
        if self.target is None:
            return
        self.target.die(KilledByMafia(self.game.moment, self.player))
        self.game.event_manager.post(PlayerDied(channel="main", dead=self.target))
        self._target = None

    # noinspection PyMethodMayBeStatic
    def target_change_event_channel(self) -> str:
        return "mafia"

    # noinspection PyMethodMayBeStatic
    def available_chat_channels(self) -> List[str]:
        return ["main", "mafia"]

    def get_valid_targets(self) -> List["SalemPlayer"]:
        return [player for player in self.game.players.by_name() if player.death is None]
