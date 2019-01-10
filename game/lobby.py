import typing
from .chat import UserJoinedEvent, UserLeftEvent, UserRenamedEvent, ChatEvent
from .user import User


class Lobby:
    def __init__(self, name):
        self.name = name
        self.games = []
        self._chat_events = []
        self.users = []

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

    def user_rename(self, user: User, new_name: str):
        self.broadcast_chat_event(UserRenamedEvent(user, new_name))
        user.name = new_name

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


class TargetedChatEvent:
    def __init__(self, event: ChatEvent, users: typing.List[User]):
        self.event = event
        self.users = users
