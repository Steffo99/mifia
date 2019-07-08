from .salemrole import SalemRole, SingleTarget
from ..deaths import KilledByMafia


class Mafioso(SalemRole, SingleTarget):
    name: str = "Mafioso"
    default_priority: int = 1

    def on_dawn(self):
        """Kill the target at dawn."""
        if self.player.death:
            return
        if self.target is None:
            return
        self.target.die(KilledByMafia(self.player.game.moment, self.player))
