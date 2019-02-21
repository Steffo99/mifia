from .gamephase import GamePhase


class Moment:
    def __init__(self, phase: GamePhase, cycle: int):
        self.phase = phase
        self.cycle = cycle

    def j(self):
        return {
            "phase": self.phase.value,
            "cycle": self.cycle
        }
