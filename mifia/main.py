import typing
import twisted.internet
import autobahn.twisted.websocket
import json
from mifia.game.lobby import Lobby, User
from mifia.utils.jsonhandling import jbytify, dejbytify

import logging
logger = logging.getLogger(__name__)


class ConnectedMifiaClient(autobahn.twisted.websocket.WebSocketServerProtocol):

    def __init__(self):
        super().__init__()
        self.user: typing.Optional[User] = None

    def onOpen(self):
        logger.info(f"{self.peer} opened a connection.")
        self.factory.client_connected(self)

    # noinspection PyPep8Naming
    def onMessage(self, payload, isBinary):
        logger.debug(f"{self.peer} sent {payload}.")
        try:
            j = dejbytify(payload)
        except json.JSONDecodeError:
            self.send_message({
                "success": False,
                "reason": "JSON parsing error"
            })
            logger.warning(f"JSON parsing error in {payload}")
        else:
            self.factory.client_message(self, j)

    def onClose(self, was_clean, code, reason):
        logger.info(f"{self.peer} closed a connection.")
        self.factory.client_disconnected(self)

    def send_message(self, data: typing.Union[dict, list]):
        self.sendMessage(jbytify(data))


class MifiaServer(autobahn.twisted.websocket.WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol = ConnectedMifiaClient
        self.main_lobby: Lobby = Lobby("lo Lobby")
        self.client_commands = {
            "lobby.info": self.cmd_lobby_info,
            "lobby.sendmsg": self.cmd_lobby_sendmsg
        }

    def client_connected(self, client):
        user = User(client)
        client.user = user
        self.main_lobby.user_join(user)

    @staticmethod
    def client_disconnected(client):
        user = client.user
        user.lobby.user_leave(user)

    def client_message(self, client, message: dict):
        try:
            request_id = message["id"]
        except KeyError:
            self.send_message({
                "success": False,
                "reason": "Missing id"
            })
            logger.debug(f"Missing id in {message}")
            return
        try:
            command = message["command"]
        except KeyError:
            client.send_message({
                "success": False,
                "id": request_id,
                "reason": "Missing command",
            })
            logger.debug(f"Missing command in {message}")
            return
        try:
            command_method = self.client_commands[command]
        except KeyError:
            client.send_message({
                "success": False,
                "id": request_id,
                "reason": "Invalid command"
            })
            logger.debug(f"Invalid command in {message}")
            return
        try:
            data = message["data"]
        except KeyError:
            client.send_message({
                "success": False,
                "id": request_id,
                "reason": "Missing data"
            })
            logger.debug(f"Missing data in {message}")
            return
        logger.debug(f"{client} called {command}")
        response = command_method(client, data)
        response["id"] = request_id
        client.send_message(response)

    @staticmethod
    def cmd_lobby_info(client, data):
        return {
            "success": True,
            "games": client.user.lobby.j_games(),
            "users": client.user.lobby.j_users()
        }

    @staticmethod
    def cmd_lobby_sendmsg(client, data):
        try:
            text = data["text"]
        except KeyError:
            return {
                "success": False,
                "reason": "Missing message text"
            }
        client.user.lobby.user_lobby_message(client.user, text)
        return {
            "success": True
        }


if __name__ == '__main__':
    print("Opening ws...")
    factory = MifiaServer(u"ws://127.0.0.1:1234")
    twisted.internet.reactor.listenTCP(1234, factory)
    twisted.internet.reactor.run()
