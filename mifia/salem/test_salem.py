import pytest

import mifia.salem as s
import mifia.namelists as nl
import mifia.salem.rolelists as rl
import mifia.salem.roles as r
import mifia.salem.judgement as j


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


def test_lynch(basic_salem_game: s.Salem):
    target = basic_salem_game.players.by_randomness()[0]

    basic_salem_game.end_night()
    basic_salem_game.end_dawn()

    for player in basic_salem_game.players.by_randomness():
        player.vote = target

    basic_salem_game.end_day()

    assert basic_salem_game.on_trial is target

    for player in basic_salem_game.players.by_randomness():
        assert player.vote is None
        player.judgement = j.Judgement.GUILTY

    basic_salem_game.end_dusk()

    assert target.death is not None

    for player in basic_salem_game.players.by_randomness():
        assert player.judgement is None
