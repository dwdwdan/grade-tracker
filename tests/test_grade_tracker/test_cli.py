from grade_tracker import cli as gt
from unittest.mock import Mock
import pytest


@pytest.mark.parametrize('num,precis,expected',
                         [(3.53, 1, "3.5"), (3, 2, "3"), (3.53, 2, "3.53")])
def test_trunc(num, precis, expected):
    assert(gt.trunc(num, precis) == expected)


def test_check_module_tree_succeeds(monkeypatch):
    module_dict = [
        {
            "module": "Module1",
            "weighting": 25,
        },
        {
            "module": "Module2",
            "weighting": 75,
            "modules": [
                {
                    "module": "Module3",
                    "weighting": 20
                },
                {
                    "module": "Module4",
                    "weighting": 79
                }
            ]
        }
    ]
    args = Mock()
    args.total_weighting_tolerance = 5
    monkeypatch.setattr(gt, "args", args, False)

    result = gt.check_module_tree(module_dict)

    assert(result is None)


def test_check_module_tree_fails(monkeypatch):
    module_dict = [
        {
            "module": "Module1",
            "weighting": 25,
        },
        {
            "module": "Module2",
            "weighting": 75,
            "modules": [
                {
                    "module": "Module3",
                    "weighting": 10
                },
                {
                    "module": "Module4",
                    "weighting": 80
                }
            ]
        }
    ]
    args = Mock()
    args.total_weighting_tolerance = 5
    monkeypatch.setattr(gt, "args", args, False)

    with pytest.raises(SystemExit):
        gt.check_module_tree(module_dict)
