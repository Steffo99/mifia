from .playerlist import PlayerList
from .errors import InvalidStateError, InvalidPlayerCountError
from .gamestate import GameState
from mifia.events import Event, GameEndedEvent, PlayerJoined, PlayerLeft
import typing
if typing.TYPE_CHECKING:
    from .player import Player
    from .rolelist import RoleList
    from .namelists import NameList
    from multiprocessing import Queue


class Game:
    def __init__(self, rolelist: "RoleList", namelist: "NameList", outgoing_queue: "Queue"):
        self.out_queue: "Queue" = outgoing_queue
        self.state: GameState = GameState.WAITING_FOR_PLAYERS
        self.players = PlayerList()
        self.rolelist: "RoleList" = rolelist
        self.namelist: "NameList" = namelist

    def send_event(self, event: "Event"):
        processed = event.to.role.on_event(event)
        self.out_queue.put(processed)

    def player_join(self, joiner: "Player"):
        self.players.add(joiner)
        for player in self.players.by_name():
            self.send_event(PlayerJoined(to=player, joiner=joiner))

    def player_leave(self, leaver: "Player"):
        if self.state == GameState.WAITING_FOR_PLAYERS:
            self.players.remove(leaver)
        else:
            leaver.connected = False
        for player in self.players.by_name():
            self.send_event(PlayerLeft(to=player, leaver=leaver))

    def start_game(self):
        if self.state != GameState.WAITING_FOR_PLAYERS:
            raise InvalidStateError("Game is not GameState.WAITING_FOR_PLAYERS!")
        if not self.rolelist.validate_player_number(len(self.players)):
            raise InvalidPlayerCountError("Game has an invalid player count according to the preset")
        for player in self.players.by_randomness():
            player.assign_role(next(self.rolelist.generator))
            player.assign_name(next(self.namelist.generator))
        self.state = GameState.IN_PROGRESS

    def victory_check(self):
        for player in self.players.by_randomness():
            if player.objective.status() is ...:
                break
        else:
            self.end_game()

    def end_game(self):
        self.state = GameState.ENDED
        for player in self.players.by_name():
            self.send_event(GameEndedEvent(player))
