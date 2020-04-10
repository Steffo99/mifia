from typing import *
from .salemrole import SalemRole, SingleTarget
from ..deaths import KilledByMafia
from ..events import MafiaKill
from ...objectives import PendingObjective
if TYPE_CHECKING:
    from ..salemplayer import SalemPlayer


class Mafioso(SalemRole, SingleTarget):
    """A role that can target another player and kill them at dawn."""

    name: str = "Mafioso"
    default_priority: int = 1

    # TODO: just for testing!
    default_objective = PendingObjective

    def on_dawn(self):
        """Kill the target at dawn."""
        self.player: SalemPlayer

        if self.player.death:
            return
        if self.target is None:
            return
        self.target.die(KilledByMafia(self.game.moment, self.player))
        self.game.send_event(MafiaKill(to=self.game.players.by_randomness(), dead=self.target, killer=self))
        self._target = None

    def get_target_change_destination(self) -> List["SalemPlayer"]:
        return self.game.players.with_role(Mafioso)

    def get_valid_targets(self) -> List["SalemPlayer"]:
        return [player for player in self.game.players.by_name() if player.death is None]
