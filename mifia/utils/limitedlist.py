import typing


class LimitedList(list):
    def __init__(self, *args, max_length: int = 0, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = max(max_length, len(self))

    def append(self, *args, **kwargs):
        if len(self) + 1 > self.max_length:
            raise OverflowError("LimitedList would go over its maximum length")
        return super().append(*args, **kwargs)

    def insert(self, *args, **kwargs):
        if len(self) + 1 > self.max_length:
            raise OverflowError("LimitedList would go over its maximum length")
        return super().insert(*args, **kwargs)

    def extend(self, collection: typing.Collection):
        try:
            if len(self) + len(collection) > self.max_length:
                raise OverflowError("LimitedList would go over its maximum length")
        except AttributeError:
            raise OverflowError("An unknown length item was added to LimitedList")
        return super().extend(collection)

    def __add__(self, other: typing.List):
        if isinstance(other, LimitedList):
            new_length = self.max_length + other.max_length
            return LimitedList(super().__add__(other), max_length=new_length)
        if len(self) + len(other) > self.max_length:
            raise OverflowError("LimitedList would go over its maximum length")
        return LimitedList(super().__add__(other), max_length=self.max_length)

    def __iadd__(self, other: typing.Collection):
        if isinstance(other, LimitedList):
            self.max_length += other.max_length
            return super().__iadd__(other)
        try:
            if len(self) + len(other) > self.max_length:
                raise OverflowError("LimitedList would go over its maximum length")
        except AttributeError:
            raise OverflowError("An unknown length item was added to LimitedList")
        return super().__iadd__(other)

    def __mul__(self, other: int):
        if len(self) * other > self.max_length:
            raise OverflowError("LimitedList would go over its maximum length")
        return LimitedList(super().__mul__(other), max_length=self.max_length)

    def __rmul__(self, other: int):
        if len(self) * other > self.max_length:
            raise OverflowError("LimitedList would go over its maximum length")
        return LimitedList(super().__rmul__(other), max_length=self.max_length)

    def __imul__(self, other):
        if len(self) * other > self.max_length:
            raise OverflowError("LimitedList would go over its maximum length")
        return super().__imul__(other)

    def __repr__(self):
        return f"LimitedList({super().__repr__()}, max_length={self.max_length})"
