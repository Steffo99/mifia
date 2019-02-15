import typing
if typing.TYPE_CHECKING:
    from .player import Player


class Objective:
    def __init__(self, player):
        self.player: Player = player

    def status(self) -> typing.Union[..., bool]:
        raise NotImplementedError()


class AutoWin(Objective):
    def status(self) -> typing.Union[..., bool]:
        return True


class AutoLose(Objective):
    def status(self) -> typing.Union[..., bool]:
        return False


class AndObjective(Objective):
    def __init__(self, player, *args: typing.List[Objective]):
        super().__init__(player)
        self.subobjectives: typing.List[Objective] = args

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
    def __init__(self, player, *args: typing.List[Objective]):
        super().__init__(player)
        self.subobjectives: typing.List[Objective] = args

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
