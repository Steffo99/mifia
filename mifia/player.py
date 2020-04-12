from typing import Optional, TYPE_CHECKING

from .errors import MultipleAssignmentError

if TYPE_CHECKING:
    from .game import Game
    from .roles.role import Role


class Player:
    def __init__(self, game: "Game"):
        self.game: "Game" = game
        self._name: Optional[str] = None
        self._role: Optional["Role"] = None
        # All players are subscribed to a "player-{_name}" loopback channel and the "main" channel by default
        self.game.event_manager.subscribe(self, self.loopback_channel())
        self.game.event_manager.subscribe(self, "main")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name} {self.role.name}>"

    def loopback_channel(self) -> str:
        """Get the name of the loopback channel of the player.

        The loopback channel is a channel where only the player itself is subscribed, and can be used for private
        system messages."""
        return f"player-{self._name}"

    @property
    def name(self) -> str:
        if self._name is None:
            return "[unnamed player]"
        return self._name

    @name.setter
    def name(self, value: str):
        if self._name is not None:
            raise MultipleAssignmentError("Can't assign a name to a player that already has one.")
        self._name = value

    @property
    def role(self) -> Optional["Role"]:
        return self._role

    @role.setter
    def role(self, value: "Role"):
        if self.role is not None:
            raise MultipleAssignmentError("Can't assign a role to a player that already has one.")
        self._role = value
