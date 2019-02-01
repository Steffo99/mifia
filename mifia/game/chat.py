import uuid
import datetime
import typing

if typing.TYPE_CHECKING:
    from .user import User


class ChatEvent:
    def __init__(self):
        self.timestamp: datetime.datetime = datetime.datetime.now()
        self.guid: str = str(uuid.uuid4())

    def __repr__(self):
        return f"<{self.__class__.__name__} with timestamp {self.timestamp}>"

    def j(self) -> dict:
        return {
            "event_name": self.__class__.__name__,
            "guid": self.guid,
            "timestamp": self.timestamp.timestamp()
        }


class UserChatEvent(ChatEvent):
    def __init__(self, user: "User"):
        super().__init__()
        self.user: "User" = user

    def j(self) -> dict:
        return {
            **super().j(),
            "user": self.user.j()
        }


class UserJoinedEvent(UserChatEvent):
    pass


class UserLeftEvent(UserChatEvent):
    pass


class UserSentMessageEvent(UserChatEvent):
    def __init__(self, user: "User", message: str):
        super().__init__(user)
        self.message: str = message

    def j(self) -> dict:
        return {
            **super().j(),
            "message": self.message
        }


class UserRenamedEvent(UserChatEvent):
    def __init__(self, user: "User", new_name: str):
        super().__init__(user)
        self.old_name: str = user.name
        self.new_name: str = new_name

    def j(self) -> dict:
        return {
            **super().j(),
            "old_name": self.old_name,
            "new_name": self.new_name
        }
