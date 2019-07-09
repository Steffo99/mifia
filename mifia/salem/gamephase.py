import enum


class GamePhase(enum.Enum):
    DAY = "DAY"
    DUSK = "DUSK"
    NIGHT = "NIGHT"
    DAWN = "DAWN"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.value}"
