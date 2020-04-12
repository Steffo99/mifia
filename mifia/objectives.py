from typing import *

import abc

if TYPE_CHECKING:
    from .player import Player


class Objective(abc.ABC):
    def __init__(self, player):
        self.player: Player = player

    @abc.abstractmethod
    def status(self) -> Union[Literal[Ellipsis], Literal[None], bool]:
        raise NotImplementedError()


class AutoWin(Objective):
    """You always win the game."""
    def status(self) -> Union[Literal[Ellipsis], Literal[None], bool]:
        return True


class AutoLose(Objective):
    """You always lose the game."""
    def status(self) -> Union[Literal[Ellipsis], Literal[None], bool]:
        return False


class NoObjective(Objective):
    """You don't have an objective, therefore you can't win, but neither you can't lose."""
    def status(self) -> Union[Literal[Ellipsis], Literal[None], bool]:
        return None


class PendingObjective(Objective):
    """An objective that's always pending."""
    def status(self) -> Union[Literal[Ellipsis], Literal[None], bool]:
        return ...


class AndObjective(Objective):
    """You win if ALL subobjectives are completed."""
    def __init__(self, player, subobjectives: List[Objective]):
        super().__init__(player)
        self.subobjectives: List[Objective] = subobjectives

    def status(self):
        worst = True
        all_none = True

        for objective in self.subobjectives:
            objstatus = objective.status()

            if worst is True:
                if objstatus is ...:
                    worst = ...
                elif objstatus is False:
                    worst = False
            elif worst is ...:
                if objstatus is False:
                    worst = False

            if objstatus is not None:
                all_none = False

        if all_none:
            return None
        else:
            return worst


class OrObjective(Objective):
    """You win if at least ONE subobjective is completed."""
    def __init__(self, player, subobjectives: List[Objective]):
        super().__init__(player)
        self.subobjectives: List[Objective] = subobjectives

    def status(self) -> Union[Literal[Ellipsis], Literal[None], bool]:
        best = False
        all_none = True

        for objective in self.subobjectives:
            objstatus = objective.status()

            if best is False:
                if objstatus is ...:
                    best = ...
                elif objstatus is True:
                    best = True
            elif best is ...:
                if objstatus is True:
                    best = True

            if objstatus is not None:
                all_none = False

        if all_none:
            return None
        else:
            return best
