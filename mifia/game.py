from .playerlist import PlayerList
from .errors import InvalidStateError, InvalidPlayerCountError
from .gamestate import GameState
from .events import Event, GameStartedEvent, GameEndedEvent, PlayerJoinedEvent, PlayerLeftEvent
import typing
import functools
if typing.TYPE_CHECKING:
    from .player import Player
    from .rolelist import RoleList
    from .namelists import NameList


def _require_gamestate(state):
    """Require that the game is in a certain state for the function to be called."""

    def decorator(f):
        if isinstance(state, GameState):
            state_list = [state]
        else:
            state_list = state

        @functools.wraps(f)
        def new_func(self, *args, **kwargs):
            if self.state not in state_list:
                raise InvalidStateError(f"This method can be called only if state is in {state}, but game "
                                        f"currently is in {self.state}")
            return f(*args, **kwargs)

        return new_func

    return decorator


class Game:
    """A Mifia game.

    Instantiate one of these to create a new game lobby."""
    def __init__(self, rolelist: "RoleList", namelist: "NameList"):
        self.state: GameState = GameState.WAITING_FOR_PLAYERS
        self.events: typing.List[Event] = []
        self.players = PlayerList()
        self.rolelist: "RoleList" = rolelist
        self.namelist: "NameList" = namelist

    def _send_event(self, event: Event):
        self.events.append(event)

    @_require_gamestate(GameState.WAITING_FOR_PLAYERS)
    def player_join(self, joiner: "Player"):
        self.players.add(joiner)
        self._send_event(PlayerJoinedEvent(to=self.players.by_randomness(), joiner=joiner))

    @_require_gamestate(GameState.WAITING_FOR_PLAYERS)
    def player_leave(self, leaver: "Player"):
        self.players.remove(leaver)
        self._send_event(PlayerLeftEvent(to=self.players.by_randomness(), leaver=leaver))

    @_require_gamestate(GameState.WAITING_FOR_PLAYERS)
    def start_game(self):
        if not self.rolelist.validate_player_number(len(self.players)):
            raise InvalidPlayerCountError("Game has an invalid player count according to the preset")
        for player in self.players.by_randomness():
            player.role = next(self.rolelist.generator)
            player.name = next(self.namelist.generator)
        self.state = GameState.IN_PROGRESS
        self._send_event(GameStartedEvent(to=self.players.by_randomness()))

    def _victory_check(self):
        for player in self.players.by_randomness():
            if player.objective.status() is ...:
                break
        else:
            self.end_game()

    @_require_gamestate(GameState.IN_PROGRESS)
    def end_game(self):
        self.state = GameState.ENDED
        self._send_event(GameEndedEvent(to=self.players.by_randomness()))
