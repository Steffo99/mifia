from ..base import Player
import typing
if typing.TYPE_CHECKING:
    from ..base import Game
    from .deaths import Death


class SalemPlayer(Player):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self.death: typing.Optional[typing.Type["Death"]] = None
