from grade_tracker import cli as gt
import pytest


@pytest.mark.parametrize('num,precis,expected',
                         [(3.53, 1, "3.5"), (3, 2, "3"), (3.53, 2, "3.53")])
def test_trunc(num, precis, expected):
    assert(gt.trunc(num, precis) == expected)

