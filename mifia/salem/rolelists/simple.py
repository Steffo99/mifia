import typing
import math
from ...rolelist import RoleList
if typing.TYPE_CHECKING:
    from ..roles import SalemRole
    from ..roles import Villager, Mafioso


class SimpleRoleList(RoleList):
    """A sample simple preset containing only Villagers and Mafiosi."""

    def validate_player_number(self, current: int):
        """Requires 4*(n!)+n players."""
        n = 1
        while True:
            target = 4 * math.factorial(n) + n
            if current == target:
                return True
            elif current > target:
                n += 1
                continue
            else:
                return False

    def create_generator(self) -> typing.Generator["SalemRole", None, None]:
        """Yield 4*(n!) Villagers and n Mafiosi."""
        count = 1
        while True:
            for _ in range(4 * count):
                yield Villager
            yield Mafioso
            count += 1
