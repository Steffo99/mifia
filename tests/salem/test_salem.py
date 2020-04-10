import pytest

import mifia.salem as s
import mifia.salem.roles as r
import mifia.salem.judgement as j

import mifia.salem.events as e

from .basic_salem_game import basic_salem_game


def test_mafioso_kill(basic_salem_game: s.Salem):
    innocent: s.SalemPlayer = basic_salem_game.players.with_role(r.Villager)[0]
    mafioso: s.SalemPlayer = basic_salem_game.players.with_role(r.Mafioso)[0]
    mafioso.role.target = innocent

    assert basic_salem_game.events.get_first_event_of_type(e.TargetChangeEvent) is not None

    basic_salem_game.end_night()
    basic_salem_game.end_dawn()

    assert innocent.death is not None
    assert mafioso.role.target is None
    assert basic_salem_game.events.get_first_event_of_type(e.MafiaKill) is not None


def test_town_chat(basic_salem_game: s.Salem):
    player: s.SalemPlayer = basic_salem_game.players.by_randomness()[0]
    player.chat("Hello world!")

    message: e.TownChatMessage = basic_salem_game.events.get_first_event_of_type(e.TownChatMessage)
    assert message is not None
    assert message.sender is player
    assert message.msg == "Hello world!"


def test_mafia_chat(basic_salem_game: s.Salem):
    # TODO: What would the best way to make an evil chat be?
    ...


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
