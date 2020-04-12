import pytest

from mifia.salem.salem import Salem
from mifia.salem.salemplayer import SalemPlayer
from mifia.namelists.royalgames import RoyalGames
from mifia.salem.rolelists.simple import SimpleRoleList


@pytest.fixture
def empty_salem_game() -> Salem:
    return Salem(namelist=RoyalGames(), rolelist=SimpleRoleList())


@pytest.fixture
def basic_salem_game() -> Salem:
    g = Salem(namelist=RoyalGames(), rolelist=SimpleRoleList())

    g.player_join(SalemPlayer(g))
    g.player_join(SalemPlayer(g))
    g.player_join(SalemPlayer(g))
    g.player_join(SalemPlayer(g))
    g.player_join(SalemPlayer(g))

    g.start_game()

    return g
