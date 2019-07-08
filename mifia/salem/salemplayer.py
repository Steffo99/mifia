from ..player import Player
from ..requiregamestate import require_gamestate
from ..gamestate import GameState
import typing
if typing.TYPE_CHECKING:
    from .salem import Salem
    from .deaths import Death


class SalemPlayer(Player):
    def __init__(self, game: "Salem"):
        super().__init__(game)
        self.game: "Salem"
        self.death: typing.Optional["Death"] = None

    @require_gamestate(GameState.IN_PROGRESS)
    def die(self, death):
        """WARNING: This method does not generate any event, it is the caller responsibility to do so."""
        self.role.on_death()
        self.death = death
