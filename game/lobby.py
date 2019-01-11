import typing
from .chat import UserJoinedEvent, UserLeftEvent, ChatEvent
from .user import User
import uuid


class Lobby:
    def __init__(self, name):
        self.name: str = name
        self.games: typing.List = []
        self._chat_events: typing.List[ChatEvent] = []
        self.users: typing.List[User] = []
        self.guid: str = str(uuid.uuid4())

    def __repr__(self):
        return f"<Lobby {self.name} with {len(self.users)}>"

    def find_user(self, *, peer: str):
        for user in self.users:
            if user.peer == peer:
                return user

    def user_join(self, user: User):
        self.users.append(user)
        user.lobby = self
        self.broadcast_chat_event(UserJoinedEvent(user))

    def user_leave(self, user: User):
        user.lobby = None
        self.users.remove(user)
        self.broadcast_chat_event(UserLeftEvent(user))

    def broadcast_chat_event(self, event: ChatEvent, users: typing.Optional[typing.List[User]]=None):
        """Send a chat event to all the specified users, or, if the users parameter is not specified, to all the users
        in the lobby. Also, store it in the chat event log together with the user list."""
        if users is None:
            users = self.users
        for user in users:
            if user not in users:
                # ARCH: maybe raise an exception?
                print(f"Skipped {user} while broadcasting {event}: not in lobby {self}")
                continue
            user.send_chatevent(event)

    def j_games(self) -> list:
        result = []
        for game in self.games:
            result.append(game.j_lobby_data())
        return result

    def j_users(self) -> list:
        result = []
        for user in self.users:
            result.append(user.j())
        return result


class TargetedChatEvent:
    def __init__(self, event: ChatEvent, users: typing.List[User]):
        self.event = event
        self.users = users
