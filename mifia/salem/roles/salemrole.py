from typing import *
import abc

from ...roles.rolewithchat import RoleWithChat
from ...player import Player
from ...gamestate import GameState
from ..judgement import Judgement

if TYPE_CHECKING:
    from ..death import Death


class SalemRole(RoleWithChat, metaclass=abc.ABCMeta):
    """The abstract class for Salem roles. All other roles should inherit from this, plus optionally from other traits,
    such as :class:`SingleTarget`.

    Attributes:
        vote:
            The :class:`Player` that is being voted by this role's player, or ``None`` if this player isn't voting
            for anyone. It's reset to ``None`` after every vote.
        judgement:
            How this role's player has decided to judge the player currently on trial. It's reset to
            :const:`Judgement.ABSTAINED` after every vote.
    """

    def __init__(self, player: Player):
        super().__init__(player)

        self._death: Optional["Death"] = None
        self.vote: Optional[Player] = None
        self.judgement: Judgement = Judgement.ABSTAINED

    def die(self, death: "Death") -> None:
        """Kill the player having this role.

        Warning:
             This method does not generate any event, it is the caller responsibility to do so.

        Arguments:
            death: How the player died, as a :class:`Death`.
        """
        self.game.require_gamestate(GameState.IN_PROGRESS)
        self.on_death()
        self._death = death

    @property
    def death(self):
        """``None`` if the player is alive, their :class:`Death` otherwise."""
        return self._death

    @property
    def alive(self) -> bool:
        """If the player is alive or not."""
        return self._death is None

    @property
    def dead(self) -> bool:
        """If the player is dead or not. It's the opposite of :meth:`.alive`."""
        return not self.alive

    @abc.abstractmethod
    def on_dawn(self) -> None:
        """Triggered when dawn starts."""

    @abc.abstractmethod
    def on_day(self) -> None:
        """Triggered when day starts."""

    @abc.abstractmethod
    def on_dusk(self) -> None:
        """Triggered when dusk starts."""

    @abc.abstractmethod
    def on_night(self) -> None:
        """Triggered when night starts."""

    @abc.abstractmethod
    def on_death(self) -> None:
        """Triggered after the player dies."""

    @abc.abstractmethod
    def available_chat_channels(self) -> List[str]:
        """A list of channels in which this Role can send messages in."""
        available = []
        if self.alive:
            available.append("main")
        return available
