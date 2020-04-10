from typing import Optional, TYPE_CHECKING, Dict, List, Union
from ..events import Event
if TYPE_CHECKING:
    from .moment import Moment
    from .salemplayer import SalemPlayer
    from .roles.salemrole import SalemRole
    from .judgement import Judgement


class PlayerDied(Event):
    """A player has died... Somehow."""
    def __init__(self,
                 to: Union[None, "SalemPlayer", List["SalemPlayer"]],
                 dead: "SalemPlayer"):
        super().__init__(to=to)
        self.dead: SalemPlayer = dead


class MafiaKill(PlayerDied):
    """A player was killed by the Mafia."""
    def __init__(self,
                 to: Union[None, "SalemPlayer", List["SalemPlayer"]],
                 dead: "SalemPlayer",
                 killer: "SalemRole"):
        super().__init__(to=to, dead=dead)
        self.killer: "SalemRole" = killer


class TrialStart(Event):
    """Votes to put a player on trial has ended."""
    def __init__(self,
                 to: Union[None, "SalemPlayer", List["SalemPlayer"]],
                 on_trial: "SalemPlayer",
                 votes: Dict["SalemPlayer", "SalemPlayer"]):
        super().__init__(to=to)
        self.on_trial: "SalemPlayer" = on_trial
        self.votes: Dict["SalemPlayer", "SalemPlayer"] = votes


class PassedJudgement(Event):
    """A judgement was passed to the on-trial player."""
    def __init__(self,
                 to: Union[None, "SalemPlayer", List["SalemPlayer"]],
                 on_trial: "SalemPlayer",
                 judgements: Dict["SalemPlayer", "Judgement"]):
        super().__init__(to=to)
        self.on_trial: "SalemPlayer" = on_trial
        self.judgements: Dict["SalemPlayer", "Judgement"] = judgements


class Lynch(PlayerDied):
    """A player was lynched by the town."""


class MomentChange(Event):
    """The game moment has changed."""
    def __init__(self,
                 to: Union[None, "SalemPlayer", List["SalemPlayer"]],
                 previous_moment: Optional["Moment"],
                 new_moment: "Moment"):
        super().__init__(to=to)
        self.previous_moment: Optional["Moment"] = previous_moment
        self.new_moment: "Moment" = new_moment


class ChatMessage(Event):
    """Any chat message."""
    def __init__(self,
                 to: Union[None, "SalemPlayer", List["SalemPlayer"]],
                 sender: "SalemPlayer",
                 msg: str):
        super().__init__(to=to)
        self.sender: "SalemPlayer" = sender
        self.msg: str = msg

    def __repr__(self):
        return f"<{self.__class__.__name__} -> {len(self.to)}: {self.msg}>"


class TownChatMessage(ChatMessage):
    """A message sent in the town (main) chat."""


class MafiaChatMessage(ChatMessage):
    """A message sent in the mafia (private) chat."""


class TargetChangeEvent(Event):
    """The target of a :class:`SingleTarget` role was changed."""

    def __init__(self,
                 to: Union[None, "SalemPlayer", List["SalemPlayer"]],
                 source: "SalemPlayer",
                 target: Optional["SalemPlayer"]):
        super().__init__(to=to)
        self.source: "SalemPlayer" = source
        self.target: Optional["SalemPlayer"] = target
