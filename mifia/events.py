import typing
if typing.TYPE_CHECKING:
    from mifia.player import Player


class Event:
    """An abstract game event.

    Attributes:
        channel: the name of the channel this event should be sent in."""

    def __init__(self, channel: str):
        """Create the event.

        Args:
            channel: the name of the channel this event should be sent in.
        """
        self.channel = channel

    def __repr__(self):
        return f"<{self.__class__.__name__} -> {self.channel}>"


class GameStarted(Event):
    """The game has advanced from the :py:const:`mifia.GameState.WAITING_FOR_PLAYERS` to the
    :py:const:`mifia.GameState.IN_PROGRESS`."""


class GameEnded(Event):
    """The game has advanced from the :py:const:`mifia.GameState.IN_PROGRESS` to the
    :py:const:`mifia.GameState.ENDED`.

    Attributes:
        results: A dict that maps players to a value that is either :py:const:`None` (null result), :py:const:`True`
         (win) or :py:const:`False` (loss)."""

    def __init__(self,
                 channel: str,
                 results: typing.Dict["Player", typing.Optional[bool]]):
        super().__init__(channel)
        self.results: typing.Dict["Player", typing.Optional[bool]] = results


class PlayerJoined(Event):
    """A new player has joined the game during the :py:const:`mifia.GameState.WAITING_FOR_PLAYERS`.

    Attributes:
        joiner: The :py:class:`mifia.Player` that has joined the game."""

    def __init__(self,
                 channel: str,
                 joiner: "Player"):
        super().__init__(channel)
        self.joiner = joiner


class PlayerLeft(Event):
    """A player has left the game during the :py:const:`mifia.GameState.WAITING_FOR_PLAYERS`.

    Attributes:
        leaver: The :py:class:`mifia.Player` that left the game."""
    
    def __init__(self,
                 channel: str,
                 leaver: "Player"):
        super().__init__(channel)
        self.leaver = leaver
