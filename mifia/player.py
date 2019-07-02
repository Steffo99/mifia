from .errors import MultipleAssignmentError
import typing
if typing.TYPE_CHECKING:
    from .game import Game
    from .role import Role
    from .objectives import Objective


class Player:
    def __init__(self, game: "Game"):
        self._game: "Game" = game
        self.connected: bool = True
        self._name: typing.Optional[str] = None
        self._role: typing.Optional["Role"] = None
        self.objective: typing.Optional["Objective"] = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if self.name is not None:
            raise MultipleAssignmentError("Can't assign a name to a player that already has one.")
        self._name = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value: "Role"):
        if self.role is not None:
            raise MultipleAssignmentError("Can't assign a role to a player that already has one.")
        self._role = value
