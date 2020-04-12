from ...roles.canchat import CanChat
from ..salemplayer import SalemPlayer


class SalemRole(CanChat):
    def __init__(self, player: SalemPlayer):
        super().__init__(player)
        self.player: SalemPlayer

    def on_dawn(self):
        """Triggered when dawn starts."""

    def on_day(self):
        """Triggered when day starts."""

    def on_dusk(self):
        """Triggered when dusk starts."""

    def on_night(self):
        """Triggered when night starts."""

    def on_death(self):
        """Triggered after the player dies."""
