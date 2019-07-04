from ..events import Event
import typing
if typing.TYPE_CHECKING:
    from .moment import Moment
    from .salemplayer import SalemPlayer
    from .roles.salemrole import SalemRole
    from .judgement import Judgement


class PlayerDied(Event):
    """A player has died... Somehow."""
    def __init__(self,
                 to: typing.Union[None, "SalemPlayer", typing.List["SalemPlayer"]],
                 dead: "SalemPlayer"):
        super().__init__(to=to)
        self.dead: SalemPlayer = dead


class MafiaKill(PlayerDied):
    """A player was killed by the Mafia."""
    def __init__(self,
                 to: typing.Union[None, "SalemPlayer", typing.List["SalemPlayer"]],
                 dead: "SalemPlayer",
                 killer: "SalemRole"):
        super().__init__(to=to, dead=dead)
        self.killer: "SalemRole" = killer


class TrialStart(Event):
    """Votes to put a player on trial has ended."""
    def __init__(self,
                 to: typing.Union[None, "SalemPlayer", typing.List["SalemPlayer"]],
                 on_trial: "SalemPlayer",
                 vote_counts: typing.Dict["SalemPlayer", int]):
        super().__init__(to=to)
        self.on_trial: "SalemPlayer" = on_trial
        self.vote_counts: typing.Dict["SalemPlayer", int] = vote_counts


class PassedJudgement(Event):
    """A judgement was passed to the on-trial player."""
    def __init__(self,
                 to: typing.Union[None, "SalemPlayer", typing.List["SalemPlayer"]],
                 on_trial: "SalemPlayer",
                 judgements: typing.Dict[SalemPlayer, Judgement]):
        super().__init__(to=to)
        self.on_trial: "SalemPlayer" = on_trial
        self.judgements: typing.Dict[SalemPlayer, Judgement] = judgements


class Lynch(PlayerDied):
    """A player was lynched by the town."""


class MomentChange(Event):
    """The game moment has changed."""
    def __init__(self,
                 to: typing.Union[None, "SalemPlayer", typing.List["SalemPlayer"]],
                 previous_moment: typing.Optional["Moment"],
                 new_moment: "Moment"):
        super().__init__(to=to)
        self.previous_moment: typing.Optional["Moment"] = previous_moment
        self.new_moment: "Moment" = new_moment
