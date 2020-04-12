from typing import TYPE_CHECKING, Generator

from ...rolelist import RoleList
from ..roles.mafioso import Mafioso
from ..roles.villager import Villager

if TYPE_CHECKING:
    from ..roles.salemrole import SalemRole


class SimpleRoleList(RoleList):
    """A sample simple preset containing only Villagers and Mafiosi."""

    def validate_player_number(self, current: int):
        """Requires 5/14/27 players."""
        return current == 5 or current == 14 or current == 27

    def create_generator(self) -> Generator["SalemRole", None, None]:
        """Yield 4c Villagers for each Mafioso."""
        count = 1
        while True:
            for _ in range(4 * count):
                yield Villager
            yield Mafioso
            count += 1
