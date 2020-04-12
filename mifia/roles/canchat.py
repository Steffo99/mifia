from typing import *

from ..errors import GameError
from ..events import Event
from .role import Role

if TYPE_CHECKING:
    from ..player import Player


class ChatMessage(Event):
    """A chat message."""
    def __init__(self,
                 channel: str,
                 sender: "Player",
                 msg: str):
        super().__init__(channel)
        self.sender: "Player" = sender
        self.msg: str = msg

    def __repr__(self):
        return f"<{self.__class__.__name__} -> {len(self.channel)}: {self.msg}>"


class InaccessibleChannelError(GameError):
    """The role is not authorized to send chat messages in the specified channel."""


class CanChat(Role):
    """A role that can send messages in a specific list of channels. """

    def __init__(self, player: "Player"):
        super().__init__(player)

    # noinspection PyMethodMayBeStatic
    def available_chat_channels(self) -> List[str]:
        """A list of channels where this Role can send messages in."""
        return ["main"]

    def chat(self, channel: str, msg: str):
        """Send a message in a specific chat channel."""
        if channel not in self.available_chat_channels():
            raise InaccessibleChannelError(f"Not authorized to send messages in channel '{channel}'.")
        self.game.event_manager.post(ChatMessage(
            channel=channel,
            sender=self.player,
            msg=msg
        ))
