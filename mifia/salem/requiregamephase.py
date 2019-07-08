import functools
from mifia.errors import InvalidStateError


def require_gamephase(*phases):
    """Require that the game is in a certain phase for the function to be called."""

    def decorator(f):

        @functools.wraps(f)
        def new_func(self, *args, **kwargs):
            if self.moment.phase not in phases:
                raise InvalidStateError(f"This method can be called only if moment is in {phases}, but game "
                                        f"currently is in {self.moment.phase}")
            return f(*args, **kwargs)

        return new_func

    return decorator
