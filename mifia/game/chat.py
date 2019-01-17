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
            "event_name": self.__class__.__name__,
            "guid": self.guid,
            "timestamp": self.timestamp.timestamp()
        }


class UserChatEvent(ChatEvent):
    def __init__(self, user: User):
        super().__init__()
        self.user: User = user

    def j(self):
        j = super().j()
        j["user"] = self.user.j()
        return j


class UserJoinedEvent(UserChatEvent):
    pass


class UserLeftEvent(UserChatEvent):
    pass


class UserSentMessageEvent(UserChatEvent):
    def __init__(self, user: User, message: str):
        super().__init__(user)
        self.message: str = message

    def j(self):
        j = super().j()
        j["message"] = self.message
        return j


class UserChangedNameEvent(UserChatEvent):
    def __init__(self, user, old_name):
        super().__init__(user)
        self.old_name = old_name
        self.new_name = user.name

    def j(self):
        j = super().j()
        j["old_name"] = self.old_name
        j["new_name"] = self.new_name
        return j
