import uuid

from .user import User
import datetime


class ChatEvent:
    def __init__(self):
        self.timestamp: datetime.datetime = datetime.datetime.now()
        self.guid: str = str(uuid.uuid4())

    def __repr__(self):
        return f"<{self.__class__.__name__} with timestamp {self.timestamp}>"

    def j(self):
        return {
            "event": self.__class__.__name__,
            "guid": self.guid
        }


class UserChatEvent(ChatEvent):
    def __init__(self, user: User):
        super().__init__()
        self.user: User = user

    def j(self):
        return {
            "event": self.__class__.__name__,
            "guid": self.guid,
            "user": self.user.j()
        }


class UserJoinedEvent(UserChatEvent):
    pass


class UserLeftEvent(UserChatEvent):
    pass


class UserSentMessageEvent(UserChatEvent):
    def __init__(self, user: User, message: str):
        super().__init__(user)
        self.message: str = message

    def j(self):
        return {
            "event": self.__class__.__name__,
            "guid": self.guid,
            "user": self.user.j(),
            "message": self.message
        }
