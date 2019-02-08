import typing
if typing.TYPE_CHECKING:
    from ..player import Player


class Objective:
    def __init__(self, player):
        self.player: Player = None

    def is_complete(self) -> bool:
        raise NotImplementedError()


class AutoWin(Objective):
    def is_complete(self) -> bool:
        return True


class AutoLose(Objective):
    def is_complete(self) -> bool:
        return False


class AndObjective(Objective):
    def __init__(self, player, *args: typing.List[Objective]):
        super().__init__(player)
        self.subobjectives: typing.List[Objective] = args

    def is_complete(self):
        status = True
        for objective in self.subobjectives:
            status = status and objective.is_complete()
        return status


class OrObjective(Objective):
    def __init__(self, player, *args: typing.List[Objective]):
        super().__init__(player)
        self.subobjectives: typing.List[Objective] = args

    def is_complete(self):
        status = False
        for objective in self.subobjectives:
            status = status or objective.is_complete()
        return status
