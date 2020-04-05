from .playerlist import PlayerList
from .errors import InvalidPlayerCountError, InvalidStateError
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

    def require_gamestate(self, *states):
        if self.state not in states:
            raise InvalidStateError(f"This method can be called only if state is in {states}, but game "
                                    f"currently is in {self.state}")

    def send_event(self, event: events.Event):
        self.events.append(event)

    def player_join(self, joiner: "Player"):
        self.require_gamestate(GameState.WAITING_FOR_PLAYERS)
        self.players.add(joiner)
        self.send_event(events.PlayerJoined(to=self.players.by_randomness(), joiner=joiner))

    def player_leave(self, leaver: "Player"):
        self.require_gamestate(GameState.WAITING_FOR_PLAYERS)
        self.players.remove(leaver)
        self.send_event(events.PlayerLeft(to=self.players.by_randomness(), leaver=leaver))

    def start_game(self):
        self.require_gamestate(GameState.WAITING_FOR_PLAYERS)

        if not self.rolelist.validate_player_number(len(self.players)):
            raise InvalidPlayerCountError("Game has an invalid player count according to the preset")
        for player in self.players.by_randomness():
            player.role = next(self.rolelist.generator)(player)
            player.name = next(self.namelist.generator)
        self.state = GameState.IN_PROGRESS
        self.send_event(events.GameStarted(to=self.players.by_randomness()))

    def victory_check(self):
        self.require_gamestate(GameState.IN_PROGRESS)
        for player in self.players.by_priority():
            if player.role.objective.status() is ...:
                break
        else:
            self.end_game()

    def end_game(self):
        self.require_gamestate(GameState.IN_PROGRESS)
        self.state = GameState.ENDED
        results_dict = {}
        for player in self.players.by_priority():
            results_dict[player] = player.role.objective.status()
        self.send_event(events.GameEnded(to=self.players.by_priority(), results=results_dict))
