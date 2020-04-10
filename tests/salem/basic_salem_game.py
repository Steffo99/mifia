import pytest

import mifia.salem as s
import mifia.namelists as nl
import mifia.salem.rolelists as rl


@pytest.fixture
def basic_salem_game() -> s.Salem:
    g = s.Salem(namelist=nl.RoyalGames(), rolelist=rl.SimpleRoleList())

    g.player_join(s.SalemPlayer(g))
    g.player_join(s.SalemPlayer(g))
    g.player_join(s.SalemPlayer(g))
    g.player_join(s.SalemPlayer(g))
    g.player_join(s.SalemPlayer(g))

    g.start_game()

    return g
