import typing
import secrets
from .player import Player
if typing.TYPE_CHECKING:
    from .role import Role


class PlayerList:
    def __init__(self, list=None):
        if list is None:
            self.list: typing.List[Player] = []
        else:
            self.list = list

    def __len__(self):
        return len(self.list)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.list)})"

    def add(self, player: Player):
        self.list.append(player)

    def remove(self, player: Player):
        self.list.remove(player)

    def by_priority(self) -> typing.List[Player]:
        return sorted(self.list, key=lambda p: p.role.priority)

    def by_name(self) -> typing.List[Player]:
        return sorted(self.list, key=lambda p: p.name)

    def by_randomness(self) -> typing.List[Player]:
        origin = self.list.copy()
        result = []
        for _ in self.list:
            player = secrets.choice(origin)
            result.append(player)
            origin.remove(player)
        assert len(result) == len(self.list)
        return result

    def with_role(self, role: typing.Type["Role"]) -> typing.List[Player]:
        return [player for player in self.list if isinstance(player.role, role)]
