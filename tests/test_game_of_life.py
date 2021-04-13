from game.game_of_life import game_of_life
# import pytest


def test_game_never_dies():
    initial_list = [(0, 0), (0, 1), (1, 0), (1, 1)]
    board_after = game_of_life(initial_list)
    assert board_after.check_if_all_dead() is False


def test_game_dies():
    initial_list = [(0, 0), (0, 1)]
    board_after = game_of_life(initial_list)
    assert board_after.check_if_all_dead()



