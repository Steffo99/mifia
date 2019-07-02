import typing
if typing.TYPE_CHECKING:
    from .player import Player


class Objective:
    def __init__(self, player):
        self.player: Player = player

    def status(self) -> typing.Union[..., bool]:
        raise NotImplementedError()


class AutoWin(Objective):
    """You always win the game."""
    def status(self) -> typing.Union[..., bool]:
        return True


class AutoLose(Objective):
    """You always lose the game."""
    def status(self) -> typing.Union[..., bool]:
        return False


class NoObjective(Objective):
    """You don't have an objective, therefore you can't win, but neither you can't lose."""
    def status(self):
        return None


class AndObjective(Objective):
    """You win if ALL subobjectives are completed."""
    def __init__(self, player, subobjectives: typing.List[Objective]):
        super().__init__(player)
        self.subobjectives: typing.List[Objective] = subobjectives

    def status(self):
        status = True
        for objective in self.subobjectives:
            objstatus = objective.status()
            if objstatus is ...:
                return ...
            else:
                status = status and objective.status()
        return status


class OrObjective(Objective):
    """You win if at least ONE subobjective is completed."""
    def __init__(self, player, subobjectives: typing.List[Objective]):
        super().__init__(player)
        self.subobjectives: typing.List[Objective] = subobjectives

    def status(self):
        undefined = False
        for objective in self.subobjectives:
            objstatus = objective.status()
            if objstatus is True:
                return True
            if objstatus is ...:
                undefined = True
        if undefined:
            return ...
        else:
            return False
