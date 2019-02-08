import typing
import uuid

if typing.TYPE_CHECKING:
    from .game import MifiaGame
    from .user import User
    from .roles import Role
    from .objectives import Objective
    from mifia.game.deaths.death import Death


class Player:
    def __init__(self, game: MifiaGame, user: User):
        self.game: MifiaGame = game
        self.user: User = user
        self.guid: str = str(uuid.uuid4())

        self.name: typing.Optional[str] = None
        self.death: typing.Optional[Death] = None

        self.role: typing.Optional[Role] = None
        self.objective: typing.Optional[Objective] = None

    def j_public(self) -> dict:
        return {
            "name": self.name,
            "death": self.death.j() if self.death is not None else None
        }

    def kill(self, death):
        self.role.on_death()
        self.death = death
