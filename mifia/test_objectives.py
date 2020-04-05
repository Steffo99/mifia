import pytest

import mifia.objectives as mo


@pytest.fixture
def player():
    return ...


def test_autowin(player):
    obj = mo.AutoWin(player)
    assert obj.status() is True


def test_autolose(player):
    obj = mo.AutoLose(player)
    assert obj.status() is False


def test_noobjective(player):
    obj = mo.NoObjective(player)
    assert obj.status() is None


def test_pendingobjective(player):
    obj = mo.PendingObjective(player)
    assert obj.status() is ...


def test_andobjective(player):
    o1 = mo.AutoWin(player)
    o2 = mo.AutoWin(player)
    o12 = mo.AndObjective(player, [o1, o2])
    assert o12.status() is True

    o3 = mo.AutoWin(player)
    o4 = mo.AutoLose(player)
    o34 = mo.AndObjective(player, [o3, o4])
    assert o34.status() is False

    o5 = mo.AutoLose(player)
    o6 = mo.AutoLose(player)
    o56 = mo.AndObjective(player, [o5, o6])
    assert o56.status() is False

    o7 = mo.AutoWin(player)
    o8 = mo.PendingObjective(player)
    o78 = mo.AndObjective(player, [o7, o8])
    assert o78.status() is ...

    o9 = mo.AutoLose(player)
    o10 = mo.PendingObjective(player)
    o910 = mo.AndObjective(player, [o9, o10])
    assert o910.status() is False

    o11 = mo.AutoWin(player)
    o12 = mo.NoObjective(player)
    o1112 = mo.AndObjective(player, [o11, o12])
    assert o1112.status() is True

    o13 = mo.AutoLose(player)
    o14 = mo.NoObjective(player)
    o1314 = mo.AndObjective(player, [o13, o14])
    assert o1314.status() is False


def test_orobjective(player):
    o1 = mo.AutoWin(player)
    o2 = mo.AutoWin(player)
    o12 = mo.OrObjective(player, [o1, o2])
    assert o12.status() is True

    o3 = mo.AutoWin(player)
    o4 = mo.AutoLose(player)
    o34 = mo.OrObjective(player, [o3, o4])
    assert o34.status() is True

    o5 = mo.AutoLose(player)
    o6 = mo.AutoLose(player)
    o56 = mo.OrObjective(player, [o5, o6])
    assert o56.status() is False

    o7 = mo.AutoWin(player)
    o8 = mo.PendingObjective(player)
    o78 = mo.OrObjective(player, [o7, o8])
    assert o78.status() is True

    o9 = mo.AutoLose(player)
    o10 = mo.PendingObjective(player)
    o910 = mo.OrObjective(player, [o9, o10])
    assert o910.status() is ...

    o11 = mo.AutoWin(player)
    o12 = mo.NoObjective(player)
    o1112 = mo.OrObjective(player, [o11, o12])
    assert o1112.status() is True

    o13 = mo.AutoLose(player)
    o14 = mo.NoObjective(player)
    o1314 = mo.OrObjective(player, [o13, o14])
    assert o1314.status() is False
