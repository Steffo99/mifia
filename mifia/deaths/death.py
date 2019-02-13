import typing
if typing.TYPE_CHECKING:
    from mifia import Moment


class Death:
    def __init__(self, moment: Moment):
        self.moment: Moment = moment

    def j(self) -> dict:
        return {
            "death_reason": self.__class__.__name__,
            "moment": self.moment.j()
        }
