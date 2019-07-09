from .salemrole import SalemRole, SingleTarget
from ..deaths import KilledByMafia
from ...events import Event
import typing
if typing.TYPE_CHECKING:
    from ..salemplayer import SalemPlayer


class MafiosoTargetSelect(Event):
    """A Mafioso changed its target."""
    def __init__(self, to: typing.Union[None, "SalemPlayer", typing.List["SalemPlayer"]],
                 mafioso: "Mafioso", target: typing.Optional["SalemPlayer"],):
        super().__init__(to=to)
        self.mafioso: "Mafioso" = mafioso
        self.target: typing.Optional["SalemPlayer"] = target


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

    def set_target(self, target: typing.Optional["SalemPlayer"]):
        super().set_target(target)
        self.player.game.send_event(MafiosoTargetSelect(to=self.game.players.with_role(Mafioso),
                                                        mafioso=self,
                                                        target=target))
