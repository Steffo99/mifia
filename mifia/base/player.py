from .errors import MultipleAssignmentError
import typing
if typing.TYPE_CHECKING:
    from .game import Game
    from .role import Role
    from .objectives import Objective
    from mifia.salem.deaths.death import Death


class Player:
    def __init__(self, game: "Game"):
        self.game: "Game" = game
        self.connected: bool = True

        self.name: typing.Optional[str] = None
        self.death: typing.Optional["Death"] = None

        self.role: typing.Optional[typing.Type["Role"]] = None
        self.objective: typing.Optional["Objective"] = None

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
