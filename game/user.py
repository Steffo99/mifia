import typing
if typing.TYPE_CHECKING:
    from .lobby import Lobby
    from .chat import ChatEvent


class User:
    def __init__(self, peer):
        self.peer: str = peer
        self.name: str = "Guest"
        self.lobby: typing.Optional[Lobby] = None
        self._unsent_events: typing.List[ChatEvent] = []

    def __repr__(self):
        return f"<User {self.name}>"

    def dict(self):
        return {
            "name": self.name
        }

    def send_chatevent(self, event: "ChatEvent"):
        print(f"Scheduled {event} to be sent to {self}")
        self._unsent_events.append(event)

    def answer_poll(self):
        print(f"Answering poll for {self}")
        events = []
        for event in self._unsent_events:
            events.append(event.dict())
        self._unsent_events.clear()
        return events
