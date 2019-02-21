from ..base import Player
import typing
if typing.TYPE_CHECKING:
    from .salem import Salem
    from .deaths import Death


class SalemPlayer(Player):
    def __init__(self, game: "Salem"):
        super().__init__(game)
        self.game: "Salem"
        self.death: typing.Optional["Death"] = None

    def kill(self, death):
        self.role.on_death()
        self.death = death
