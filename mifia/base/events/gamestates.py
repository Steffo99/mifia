from .event import Event


class GameStartedEvent(Event):
    @property
    def objective(self):
        return self.to.objective


class GameEndedEvent(Event):
    @property
    def objective(self):
        return self.to.objective

    @property
    def result(self):
        return self.to.objective.status()
