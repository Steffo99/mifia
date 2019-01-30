class Death:
    def __init__(self, moment: ...):
        self.moment: ... = moment

    def j(self) -> dict:
        return {
            "death_reason": self.__class__.__name__
        }
