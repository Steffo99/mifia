import twisted.internet
import autobahn.twisted.websocket
import json
from game.lobby import Lobby, User
from game.chat import UserSentMessageEvent
import uuid

lobby = Lobby("Unica")


def jbytify(data) -> bytes:
    string = json.dumps(data)
    byte = bytes(string, encoding="utf8")
    return byte


class MifiaProtocol(autobahn.twisted.websocket.WebSocketServerProtocol):
    def onOpen(self):
        user = User(peer=self.peer)
        lobby.user_join(user)

    def onConnect(self, request):
        pass

    def onMessage(self, payload: bytes, is_binary):
        # ARCH: use moar classes
        j = json.loads(payload)
        user = lobby.find_user(peer=self.peer)
        response = {
            "request": j["command"],
            "success": False
        }
        if j["command"] == "lobby.get_self":
            response["success"] = True
            response["data"] = user.j()
        elif j["command"] == "lobby.get_unread_messages":
            response["success"] = True
            response["data"] = user.fetch_unsent_events()
        elif j["command"] == "lobby.get_games_list":
            response["success"] = True
            response["data"] = user.lobby.j_games()
        elif j["command"] == "lobby.get_users_list":
            response["success"] = True
            response["data"] = user.lobby.j_users()
        elif j["command"] == "lobby.send_chat_message":
            response["success"] = True
            user.lobby.broadcast_chat_event(UserSentMessageEvent(user, j["content"]))
        self.sendMessage(jbytify(response), isBinary=False)

    def onClose(self, was_clean, code, reason):
        user = lobby.find_user(peer=self.peer)
        lobby.user_leave(user)


if __name__ == '__main__':
    print("Opening ws...")
    factory = autobahn.twisted.websocket.WebSocketServerFactory(u"ws://127.0.0.1:1234")
    factory.protocol = MifiaProtocol
    twisted.internet.reactor.listenTCP(1234, factory)
    twisted.internet.reactor.run()
