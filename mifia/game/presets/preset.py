import typing
from ..roles import Role


class Preset:
    name: str = NotImplemented

    def __init__(self):
        self.generator = self.create_generator()

    def validate_player_number(self, current: int):
        raise NotImplementedError()

    def create_generator(self) -> typing.Generator[Role, None, None]:
        raise NotImplementedError()
