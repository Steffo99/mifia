from .requiregamestate import require_gamestate
from .playerlist import PlayerList
from .errors import InvalidPlayerCountError
from .gamestate import GameState
from . import events
import typing

if typing.TYPE_CHECKING:
    from .player import Player
    from .rolelist import RoleList
    from .namelists import NameList


class Game:
    """A Mifia game.

    Instantiate one of these to create a new game lobby."""
    def __init__(self, rolelist: "RoleList", namelist: "NameList"):
        self.state: GameState = GameState.WAITING_FOR_PLAYERS
        self.events: typing.List[events.Event] = []
        self.players = PlayerList()
        self.rolelist: "RoleList" = rolelist
        self.namelist: "NameList" = namelist

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.state}, with {len(self.players)} players>"

    def send_event(self, event: events.Event):
        self.events.append(event)

    @require_gamestate(GameState.WAITING_FOR_PLAYERS)
    def player_join(self, joiner: "Player"):
        self.players.add(joiner)
        self.send_event(events.PlayerJoined(to=self.players.by_randomness(), joiner=joiner))

    @require_gamestate(GameState.WAITING_FOR_PLAYERS)
    def player_leave(self, leaver: "Player"):
        self.players.remove(leaver)
        self.send_event(events.PlayerLeft(to=self.players.by_randomness(), leaver=leaver))

    @require_gamestate(GameState.WAITING_FOR_PLAYERS)
    def start_game(self):
        if not self.rolelist.validate_player_number(len(self.players)):
            raise InvalidPlayerCountError("Game has an invalid player count according to the preset")
        for player in self.players.by_randomness():
            player.role = next(self.rolelist.generator)(player)
            player.name = next(self.namelist.generator)
        self.state = GameState.IN_PROGRESS
        self.send_event(events.GameStarted(to=self.players.by_randomness()))

    @require_gamestate(GameState.IN_PROGRESS)
    def victory_check(self):
        for player in self.players.by_priority():
            if player.role.objective.status() is ...:
                break
        else:
            self.end_game()

    @require_gamestate(GameState.IN_PROGRESS)
    def end_game(self):
        self.state = GameState.ENDED
        results_dict = {}
        for player in self.players.by_priority():
            results_dict[player] = player.role.objective.status()
        self.send_event(events.GameEnded(to=self.players.by_priority(), results=results_dict))
