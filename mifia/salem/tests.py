import pytest

import mifia.salem as s
import mifia.namelists as nl
import mifia.salem.rolelists as rl
import mifia.salem.roles as r


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


def test_mafioso_kill(basic_salem_game: s.Salem):
    innocent: s.SalemPlayer = basic_salem_game.players.with_role(r.Villager)[0]
    mafioso: s.SalemPlayer = basic_salem_game.players.with_role(r.Mafioso)[0]
    mafioso.role.set_target(innocent)

    basic_salem_game.end_night()
    basic_salem_game.end_dawn()

    assert innocent.death is not None
    assert mafioso.role.target is None
