from typing import Optional, TYPE_CHECKING, Dict
from ..events import Event
if TYPE_CHECKING:
    from .moment import Moment
    from .salemplayer import SalemPlayer
    from .judgement import Judgement


class PlayerDied(Event):
    """A player has died."""
    def __init__(self,
                 channel: str,
                 dead: "SalemPlayer"):
        super().__init__(channel)
        self.dead: SalemPlayer = dead


class TrialStart(Event):
    """Votes to put a player on trial has ended."""
    def __init__(self,
                 channel: str,
                 on_trial: "SalemPlayer",
                 votes: Dict["SalemPlayer", "SalemPlayer"]):
        super().__init__(channel)
        self.on_trial: "SalemPlayer" = on_trial
        self.votes: Dict["SalemPlayer", "SalemPlayer"] = votes


class PassedJudgement(Event):
    """A judgement was passed to the on-trial player."""
    def __init__(self,
                 channel: str,
                 on_trial: "SalemPlayer",
                 judgements: Dict["SalemPlayer", "Judgement"]):
        super().__init__(channel)
        self.on_trial: "SalemPlayer" = on_trial
        self.judgements: Dict["SalemPlayer", "Judgement"] = judgements


class Lynch(PlayerDied):
    """A player was lynched by the town."""


class MomentChange(Event):
    """The game moment has changed."""
    def __init__(self,
                 channel: str,
                 previous_moment: Optional["Moment"],
                 new_moment: "Moment"):
        super().__init__(channel)
        self.previous_moment: Optional["Moment"] = previous_moment
        self.new_moment: "Moment" = new_moment

