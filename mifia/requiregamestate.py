import functools
from mifia.errors import InvalidStateError


def require_gamestate(*states):
    """Require that the game is in a certain state for the function to be called."""

    def decorator(f):

        @functools.wraps(f)
        def new_func(self, *args, **kwargs):
            if self.state not in states:
                raise InvalidStateError(f"This method can be called only if state is in {states}, but game "
                                        f"currently is in {self.state}")
            return f(*args, **kwargs)

        return new_func

    return decorator
