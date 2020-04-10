from typing import Type, TYPE_CHECKING, List
import secrets
from .player import Player
if TYPE_CHECKING:
    from .role import Role


class PlayerList:
    def __init__(self, li=None):
        if li is None:
            self.list: List[Player] = []
        else:
            self.list = li

    def __len__(self):
        return len(self.list)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.list)})"

    def add(self, player: Player):
        self.list.append(player)

    def remove(self, player: Player):
        self.list.remove(player)

    def by_priority(self) -> List[Player]:
        return sorted(self.list, key=lambda p: p.role.priority)

    def by_name(self) -> List[Player]:
        return sorted(self.list, key=lambda p: p.name)

    def by_randomness(self) -> List[Player]:
        origin = self.list.copy()
        result = []
        for _ in self.list:
            player = secrets.choice(origin)
            result.append(player)
            origin.remove(player)
        assert len(result) == len(self.list)
        return result

    def with_role(self, role: Type["Role"]) -> List[Player]:
        return [player for player in self.list if isinstance(player.role, role)]
