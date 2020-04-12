from typing import Optional, TYPE_CHECKING

from ..player import Player
from ..gamestate import GameState
from .judgement import Judgement

if TYPE_CHECKING:
    from .salem import Salem
    from .roles.salemrole import SalemRole
    from .death import Death


class SalemPlayer(Player):
    def __init__(self, game: "Salem"):
        super().__init__(game)
        self.game: "Salem"
        self.role: "SalemRole"

        self.death: Optional["Death"] = None
        self.vote: Optional[Player] = None
        self.judgement: Optional[Judgement] = Judgement.ABSTAINED

    def die(self, death) -> None:
        """Set the player's death to a value. In other words, kill the player.

        Warning:
             This method does not generate any event, it is the caller responsibility to do so."""
        self.game.require_gamestate(GameState.IN_PROGRESS)
        self.role.on_death()
        self.death = death
