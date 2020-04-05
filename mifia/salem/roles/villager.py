from ...objectives import AutoLose
from .salemrole import SalemRole


class Villager(SalemRole):
    """A role that does nothing."""

    name: str = "Villager"
    default_priority: int = 0
    # TODO: just for testing!
    default_objective = AutoLose