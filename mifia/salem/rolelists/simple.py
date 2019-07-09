import typing
from ...rolelist import RoleList
from ..roles import SalemRole, Villager, Mafioso


class SimpleRoleList(RoleList):
    """A sample simple preset containing only Villagers and Mafiosi."""

    def validate_player_number(self, current: int):
        """Requires 5/14/27 players."""
        return current == 5 or current == 14 or current == 27

    def create_generator(self) -> typing.Generator[SalemRole, None, None]:
        """Yield 4c Villagers for each Mafioso."""
        count = 1
        while True:
            for _ in range(4 * count):
                yield Villager
            yield Mafioso
            count += 1
