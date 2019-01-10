from .user import User
import datetime


class ChatEvent:
    def __init__(self):
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return f"<{self.__class__.__name__} with timestamp {self.timestamp}>"

    def dict(self):
        return {
            "event": self.__class__.__name__
        }


class UserChatEvent(ChatEvent):
    def __init__(self, user: User):
        super().__init__()
        self.user: User = user

    def dict(self):
        return {
            "event": self.__class__.__name__,
            "user": self.user.dict()
        }


class UserJoinedEvent(UserChatEvent):
    pass


class UserLeftEvent(UserChatEvent):
    pass


class UserRenamedEvent(UserChatEvent):
    def __init__(self, user: User, new_name: str):
        super().__init__(user)
        self.previous_name = user.name
        self.current_name = new_name

    def dict(self):
        return {
            "event": self.__class__.__name__,
            "user": self.user.dict(),
            "previous_name": self.previous_name,
            "current_name": self.current_name
        }


class UserSentMessageEvent(UserChatEvent):
    def __init__(self, user: User, message: str):
        super().__init__(user)
        self.message = message

    def dict(self):
        return {
            "event": self.__class__.__name__,
            "user": self.user.dict(),
            "message": self.message
        }
