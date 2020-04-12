from typing import Type, List, Dict, Optional, TYPE_CHECKING
from .events import Event
from .playerlist import PlayerList
if TYPE_CHECKING:
    from .player import Player


class EventManager:
    def __init__(self, li=None):
        self.list: List[Event] = li if li else []
        self._subscribers: Dict[str, PlayerList] = {}

    def __len__(self):
        return len(self.list)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.list)})"

    def __getitem__(self, item):
        if not isinstance(item, str):
            raise TypeError("Channel names must be strings.")
        return self._subscribers.get(item, PlayerList())

    def post(self, event: Event):
        """Post an event."""
        self.list.append(event)

    def get_first_event_of_type(self, event_type: Type[Event]) -> Optional[Event]:
        for event in self.list:
            if isinstance(event, event_type):
                return event
        return None

    def subscribe(self, player: "Player", channel: str):
        """Make a player subscribe to a channel."""
        if not isinstance(channel, str):
            raise TypeError("Channel names must be strings.")
        if channel not in self._subscribers:
            self._subscribers[channel] = PlayerList()
        if player not in self._subscribers[channel]:
            self._subscribers[channel].add(player)
