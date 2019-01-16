import typing
import uuid
from mifia.utils.jsonhandling import jbytify
import logging
logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from .lobby import Lobby
    from .chat import ChatEvent
    from mifia.main import ConnectedMifiaClient


class User:
    def __init__(self, client: "ConnectedMifiaClient"):
        self.client: "ConnectedMifiaClient" = client
        self.guid: str = str(uuid.uuid4())
        self.name: str = "_Guest"
        self.lobby: typing.Optional[Lobby] = None

    def __repr__(self):
        return f"<User {self.name}>"

    def j(self):
        return {
            "guid": self.guid,
            "name": self.name
        }

    def send_lobby_chatevent(self, event: "ChatEvent"):
        logger.debug(f"Sending {event} to {self}.")
        self.client.sendMessage(jbytify({
            "id": "lobby_chatevent",
            "event": event.j()
        }))
