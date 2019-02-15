import typing
import secrets
from .player import Player


class PlayerList:
    def __init__(self):
        self.list: typing.List[Player] = []

    def by_priority(self) -> typing.List[Player]:
        return sorted(self.list, key=lambda p: p.role.priority)

    def by_name(self) -> typing.List[Player]:
        return sorted(self.list, key=lambda p: p.name)

    def by_randomness(self) -> typing.List[Player]:
        origin = self.list.copy()
        result = []
        for _ in origin:
            player = secrets.choice(origin)
            result.append(player)
            origin.remove(player)
        assert len(result) == len(self.list)
        return result

    def __len__(self):
        return len(self.list)
