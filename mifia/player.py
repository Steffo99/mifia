from .errors import MultipleAssignmentError
import typing
if typing.TYPE_CHECKING:
    from .game import Game
    from .role import Role


class Player:
    def __init__(self, game: "Game"):
        self.game: "Game" = game
        self._name: typing.Optional[str] = None
        self._role: typing.Optional["Role"] = None

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name} {self.role.name}>"

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
    def role(self) -> typing.Optional["Role"]:
        return self._role

    @role.setter
    def role(self, value: "Role"):
        if self.role is not None:
            raise MultipleAssignmentError("Can't assign a role to a player that already has one.")
        self._role = value
