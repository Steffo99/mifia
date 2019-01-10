import twisted.internet
import autobahn.twisted.websocket
import json
from game.lobby import Lobby, User
from game.chat import UserSentMessageEvent, UserRenamedEvent

lobby = Lobby("Unica")


class MifiaProtocol(autobahn.twisted.websocket.WebSocketServerProtocol):
    def onOpen(self):
        user = User(self.peer)
        lobby.user_join(user)

    def onConnect(self, request):
        pass

    def onMessage(self, payload: bytes, is_binary):
        # ARCH: use moar classes
        j = json.loads(payload)
        if j["command"] == "poll":
            user = lobby.find_user(peer=self.peer)
            data = user.answer_poll()
            string = json.dumps(data)
            byte = bytes(string, encoding="utf8")
            self.sendMessage(byte, isBinary=False)
        elif j["command"] == "send_message":
            user = lobby.find_user(peer=self.peer)
            user.lobby.broadcast_chat_event(UserSentMessageEvent(user, j["content"]))
        elif j["command"] == "change_name":
            user = lobby.find_user(peer=self.peer)
            user.lobby.broadcast_chat_event(UserRenamedEvent(user, j["new_name"]))

    def onClose(self, was_clean, code, reason):
        user = lobby.find_user(peer=self.peer)
        lobby.user_leave(user)


if __name__ == '__main__':
    print("Opening ws...")
    factory = autobahn.twisted.websocket.WebSocketServerFactory(u"ws://127.0.0.1:1234")
    factory.protocol = MifiaProtocol
    twisted.internet.reactor.listenTCP(1234, factory)
    twisted.internet.reactor.run()
