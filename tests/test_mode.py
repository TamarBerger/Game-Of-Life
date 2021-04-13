from game.game_of_life import Mode
import pytest


@pytest.fixture
def mode():
    return Mode()


def test_mode_init(mode):
    assert mode.mode == mode.DEAD and mode.game_level == 0


def test_mode_kill(mode):
    mode.kill()
    assert mode.mode == mode.DEAD


def test_mode_revive(mode):
    mode.revive()
    assert mode.mode == mode.ALIVE


def test_mode_level_setting(mode):
    random_level = 8
    mode.set_level(random_level)
    assert mode.game_level == random_level


def test_live_mode_string(mode):
    mode.revive()
    assert str(mode) == "1"


def test_dead_mode_string(mode):
    mode.kill()
    assert str(mode) == "0"