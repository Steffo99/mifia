from ..player import Player
from ..errors import InvalidStateError
from ..gamestate import GameState
from .events import TownChatMessage
import typing
if typing.TYPE_CHECKING:
    from .salem import Salem
    from .deaths import Death
    from .judgement import Judgement


class SalemPlayer(Player):
    def __init__(self, game: "Salem"):
        super().__init__(game)
        self.game: "Salem"
        self.death: typing.Optional["Death"] = None
        self.vote: typing.Optional[Player] = None
        self.judgement: typing.Optional["Judgement"] = Judgement.ABSTAINED

    def die(self, death):
        """WARNING: This method does not generate any event, it is the caller responsibility to do so."""
        if self.game.state != GameState.IN_PROGRESS:
            raise InvalidStateError(f"This method can be called only if state is in {GameState.IN_PROGRESS}, but game "
                                    f"currently is in {self.game.state}")
        self.role.on_death()
        self.death = death

    def chat(self, msg: str):
        self.game.send_event(TownChatMessage(to=self.game.players.by_randomness(), sender=self, msg=msg))
