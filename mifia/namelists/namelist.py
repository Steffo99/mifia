import typing
import random


class NameList:
    list_name = NotImplemented
    names: typing.List[str] = []

    def __init__(self):
        self.generator = self.create_generator()

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return self.name

    def create_generator(self) -> typing.Generator[str, None, None]:
        while True:
            shuffled = self.names.copy()
            random.shuffle(shuffled)
            counter = 1
            for name in shuffled:
                if counter > 1:
                    yield name + str(counter)
                else:
                    yield name
            counter += 1
