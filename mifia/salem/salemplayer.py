from ..player import Player
from ..gamestate import GameState
from .events import TownChatMessage
from .judgement import Judgement
import typing
if typing.TYPE_CHECKING:
    from .salem import Salem
    from .deaths import Death


class SalemPlayer(Player):
    def __init__(self, game: "Salem"):
        super().__init__(game)
        self.game: "Salem"
        self.death: typing.Optional["Death"] = None
        self.vote: typing.Optional[Player] = None
        self.judgement: typing.Optional[Judgement] = Judgement.ABSTAINED

    def die(self, death):
        """WARNING: This method does not generate any event, it is the caller responsibility to do so."""
        self.game.require_gamestate(GameState.IN_PROGRESS)
        self.role.on_death()
        self.death = death

    def chat(self, msg: str):
        self.game.send_event(TownChatMessage(to=self.game.players.by_randomness(), sender=self, msg=msg))
