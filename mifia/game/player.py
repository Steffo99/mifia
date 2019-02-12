import uuid
from .errors import MultipleAssignmentError
import typing
if typing.TYPE_CHECKING:
    from .games import Game
    from .user import User
    from .roles import Role
    from .objectives import Objective
    from .deaths import Death




class Player:
    def __init__(self, game: "RoleGame", user: "User"):
        self.game: "RoleGame" = game
        self.user: "User" = user
        self.guid: str = str(uuid.uuid4())

        self.name: typing.Optional[str] = None
        self.death: typing.Optional["Death"] = None

        self.role: typing.Optional["Role"] = None
        self.objective: typing.Optional["Objective"] = None

    def j_public(self) -> dict:
        return {
            "name": self.name,
            "death": self.death.j() if self.death is not None else None
        }

    def kill(self, death):
        self.role.on_death()
        self.death = death

    def assign_role(self, role: "Role"):
        if role is not None:
            raise MultipleAssignmentError("Can't assign a role to a player that already has one.")
        self.role = role

    def assign_name(self, name: str):
        if name is not None:
            raise MultipleAssignmentError("Can't assign a name to a player that already has one.")
        self.name = name
