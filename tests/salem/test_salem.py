import pytest
from typing import *

from mifia.player import Player
from mifia.salem.salem import Salem
from mifia.salem.roles.mafioso import Mafioso
from mifia.salem.roles.villager import Villager
from mifia.salem.judgement import Judgement

from mifia.roles.singletarget import TargetChangeEvent
from mifia.salem.events import PlayerDied, Lynch
from mifia.roles.rolewithchat import ChatMessage, InaccessibleChannelError

from .fixtures import basic_salem_game


def test_mafioso_kill(basic_salem_game: Salem):
    innocent: Player = basic_salem_game.players.with_role(Villager)[0]
    mafioso: Player = basic_salem_game.players.with_role(Mafioso)[0]
    mafioso.role.target = innocent

    assert basic_salem_game.event_manager.get_first_event_of_type(TargetChangeEvent) is not None

    basic_salem_game.end_night()
    basic_salem_game.end_dawn()

    assert innocent.role.death is not None
    assert mafioso.role.target is None
    assert basic_salem_game.event_manager.get_first_event_of_type(PlayerDied) is not None


def test_town_chat(basic_salem_game: Salem):
    player: Player = basic_salem_game.players.by_randomness()[0]
    player.role.chat("main", "Hello world!")

    message: Optional[ChatMessage] = basic_salem_game.event_manager.get_first_event_of_type(ChatMessage)
    assert message is not None
    assert message.channel == "main"
    assert message.sender is player
    assert message.msg == "Hello world!"


def test_mafia_chat(basic_salem_game: Salem):
    player: Player = basic_salem_game.players.with_role(Mafioso)[0]
    player.role.chat("mafia", "Hello world!")

    message: Optional[ChatMessage] = basic_salem_game.event_manager.get_first_event_of_type(ChatMessage)
    assert message is not None
    assert message.channel == "mafia"
    assert message.sender is player
    assert message.msg == "Hello world!"


def test_inaccessible_chat(basic_salem_game: Salem):
    player: Player = basic_salem_game.players.by_randomness()[0]
    with pytest.raises(InaccessibleChannelError):
        player.role.chat("__INVALID__", "Hello world!")


def test_lynch(basic_salem_game: Salem):
    target = basic_salem_game.players.by_randomness()[0]

    basic_salem_game.end_night()
    basic_salem_game.end_dawn()

    for player in basic_salem_game.players.by_randomness():
        player.role.vote = target
        assert player.role.vote == target

    assert basic_salem_game.vote_count()[target] == 5

    basic_salem_game.end_day()

    assert basic_salem_game.on_trial is target

    for player in basic_salem_game.players.by_randomness():
        assert player.role.vote is None
        player.role.judgement = Judgement.GUILTY

    basic_salem_game.end_dusk()

    assert target.role.death is not None

    lynch: Optional[Lynch] = basic_salem_game.event_manager.get_first_event_of_type(Lynch)
    assert lynch is not None
    assert lynch.channel == "main"
    assert lynch.dead == target

    for player in basic_salem_game.players.by_randomness():
        assert player.role.judgement is None
