import typing
from .role import Role


class RoleList:
    name: str = NotImplemented

    def __init__(self):
        self.generator = self.create_generator()

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return self.name

    def validate_player_number(self, current: int):
        raise NotImplementedError()

    def create_generator(self) -> typing.Generator[Role, None, None]:
        raise NotImplementedError()
