from typing import List

from ...objectives import PendingObjective
from .salemrole import SalemRole


class Villager(SalemRole):
    """A role that does nothing."""

    name: str = "Villager"
    default_priority: int = 0

    # TODO: just for testing!
    default_objective = PendingObjective

    def on_dawn(self) -> None:
        pass

    def on_day(self) -> None:
        pass

    def on_dusk(self) -> None:
        pass

    def on_night(self) -> None:
        pass

    def on_death(self) -> None:
        pass

    def available_chat_channels(self) -> List[str]:
        return super().available_chat_channels()
