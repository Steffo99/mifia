from multiprocessing import Queue
from .playerlist import PlayerList
from .errors import InvalidStateError, InvalidPlayerCountError
from .gamestate import GameState
import typing
if typing.TYPE_CHECKING:
    from .command import Command
    from .event import Event
    from .rolelist import RoleList
    from .namelists import NameList


class Game:
    def __init__(self, rolelist: "RoleList", namelist: "NameList", outgoing_queue: Queue):
        self.out_queue: Queue = outgoing_queue
        self.state: GameState = GameState.WAITING_FOR_PLAYERS
        self.players = PlayerList()
        self.rolelist: "RoleList" = rolelist
        self.namelist: "NameList" = namelist

    def handle_incoming_command(self, command: Command):
        pass  # TODO

    def send_outgoing_event(self, event: Event):
        pass  # TODO

    def start_game(self):
        if self.state != GameState.WAITING_FOR_PLAYERS:
            raise InvalidStateError("Game is not GameState.WAITING_FOR_PLAYERS!")
        if not self.rolelist.validate_player_number(len(self.players)):
            raise InvalidPlayerCountError("Game has an invalid player count according to the preset")
        for player in self.players.by_randomness():
            player.assign_role(next(self.rolelist.generator))
            player.assign_name(next(self.namelist.generator))
        self.state = GameState.IN_PROGRESS
