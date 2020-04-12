from typing import Type, TYPE_CHECKING, List

import secrets
from .player import Player

if TYPE_CHECKING:
    from .role import Role


class PlayerList:
    """A list of :class:`Player`, with utility methods to make getting references to the players easier."""
    def __init__(self, li=None):
        if li is None:
            self._list: List[Player] = []
        else:
            self._list = li

    def __len__(self):
        return len(self._list)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._list)})"

    def __contains__(self, item):
        return item in self._list

    def add(self, player: Player):
        """Add a new player to the list."""
        if not isinstance(player, Player):
            raise TypeError("Only Players can be added to a PlayerList.")
        self._list.append(player)

    def remove(self, player: Player):
        """Remove a player from the list."""
        self._list.remove(player)

    def by_priority(self) -> List[Player]:
        """Get the players contained in the list, sorted by their role priority."""
        return sorted(self._list, key=lambda p: p.role.priority)

    def by_name(self) -> List[Player]:
        """Get the players contained in the list, sorted in alphabetical order."""
        return sorted(self._list, key=lambda p: p.name)

    def by_randomness(self) -> List[Player]:
        """Get the players contained in the list, sorted in a random order."""
        origin = self._list.copy()
        result = []
        for _ in self._list:
            player = secrets.choice(origin)
            result.append(player)
            origin.remove(player)
        assert len(result) == len(self._list)
        return result

    def with_role(self, role: Type["Role"]) -> List[Player]:
        """Get all the players with a specific role contained in the list."""
        return [player for player in self._list if isinstance(player.role, role)]
