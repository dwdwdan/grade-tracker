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


@pytest.mark.parametrize('ignore_unmarked,expected', [(False, 55), (True, 62.5)])
def test_calc_percentage(monkeypatch, ignore_unmarked, expected):
    module_dict = [
        {
            "module": "Module1",
            "weighting": 25,
            "percent": 100
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
                    "weighting": 80,
                    "percent": 50
                }
            ]
        }
    ]
    expected_percent = expected

    args = Mock()
    args.indent_string = "  "
    args.post_string = "%"
    args.ignore_unmarked = ignore_unmarked
    monkeypatch.setattr(gt, "args", args, False)

    actual_percent = gt.calc_percentage(module_dict, "", "")

    assert(expected_percent == actual_percent)
