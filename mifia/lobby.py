import typing
from .chat import UserJoinedEvent, UserLeftEvent, ChatEvent, UserSentMessageEvent
from .user import User
import uuid

import logging
logger = logging.getLogger(__name__)


class UserNotInLobbyError(Exception):
    pass


class Lobby:
    def __init__(self, name):
        self.name: str = name
        self.games: typing.List = []
        self.users: typing.List[User] = []
        self.guid: str = str(uuid.uuid4())

    def __repr__(self):
        return f"<Lobby {self.name} with {len(self.users)}>"

    def user_join(self, user: User):
        self.users.append(user)
        user.lobby = self
        self.broadcast_chatevent(UserJoinedEvent(user))
        logger.info(f"{user} joined {self}.")

    def user_leave(self, user: User):
        user.lobby = None
        self.users.remove(user)
        self.broadcast_chatevent(UserLeftEvent(user))
        logger.info(f"{user} left {self}.")

    def user_lobby_message(self, user: User, message: str):
        self.broadcast_chatevent(UserSentMessageEvent(user, message))
        logger.info(f"{user} says: {message}")

    def broadcast_chatevent(self,
                            event: ChatEvent,
                            users: typing.Optional[typing.List[User]]=None,
                            *,
                            raise_for_missing_users: bool=True):
        """Send a chat event to all the specified users, or, if the users parameter is not specified, to all the users
        in the lobby. Also, store it in the chat event log together with the user list."""
        if users is None:
            users = self.users
        for user in users:
            if user not in self.users:
                if raise_for_missing_users:
                    raise UserNotInLobbyError(f"{user} is not in {self}")
                else:
                    continue
            user.send_lobby_chatevent(event)

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
