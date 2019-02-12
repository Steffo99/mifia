from .game import Game


class Salem(Game):
    """A game mode where discussion takes place during the dawn, a player is voted during the day and a judgement is passed on them during the dusk.
     If they are found guilty, they are lynched, while if they are found innocent, nothing happens.
     In either case, the game moves on to the night, where nothing* happens."""

