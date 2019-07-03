from ..events import Event
import typing
if typing.TYPE_CHECKING:
    from .player import SalemPlayer
    from .roles.salemrole import SalemRole


class PlayerDied(Event):
    """A player has died... Somehow."""
    def __init__(self, to: typing.Union[None, "SalemPlayer", typing.List["SalemPlayer"]], dead: "SalemPlayer"):
        super().__init__(to=to)
        self.dead: SalemPlayer = dead


class KilledByMafia(PlayerDied):
    """A player was killed by the Mafia."""
    def __init__(self, to: typing.Union[None, "SalemPlayer", typing.List["SalemPlayer"]], dead: "SalemPlayer", killer: "SalemRole"):
        super().__init__(to=to, dead=dead)
        self.killer: "SalemRole" = killer
