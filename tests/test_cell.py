import re

from game.game_of_life import Cell
import pytest


@pytest.fixture
def cell():
    return Cell()


def test_cell_init(cell):
    assert str(cell.mode) == "0" and str(cell.previous_mode) == "0"


def test_cell_string(cell):
    str_structure = re.compile(
        r"(?:[a-zA-Z\s]+: [01]\n){2}"
        r"[a-zA-Z\s]+: \d+\n"
    )
    assert str_structure.match(str(cell)) is not None
