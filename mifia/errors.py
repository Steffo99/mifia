class MultipleAssignmentError(Exception):
    """A role or a name is assigned more than once to a player who already had one."""


class GameError(Exception):
    pass


class InvalidStateError(GameError):
    """The game is not in the correct state to perform the operation."""


class InvalidPlayerCountError(GameError):
    """The game doesn't have enough players to start."""
