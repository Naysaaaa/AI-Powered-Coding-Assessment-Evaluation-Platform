import pytest

from backend.judge.comparator import compare_output


def test_exact_match():
    assert compare_output("5", "5", "exact") is True


def test_exact_mismatch():
    assert compare_output("5", "6", "exact") is False


def test_exact_detects_whitespace_difference():
    assert compare_output("5", "5\n", "exact") is False


def test_whitespace_normalized_match():
    assert compare_output(
        "5",
        "5\n",
        "whitespace_normalized",
    ) is True


def test_whitespace_normalized_ignores_extra_spaces():
    assert compare_output(
        "5 10 15",
        "5    10     15",
        "whitespace_normalized",
    ) is True


def test_whitespace_normalized_ignores_newlines():
    assert compare_output(
        "5\n10\n15",
        "5 10 15",
        "whitespace_normalized",
    ) is True


def test_whitespace_normalized_mismatch():
    assert compare_output(
        "5 10 15",
        "5 10 16",
        "whitespace_normalized",
    ) is False


def test_invalid_comparison_mode():
    with pytest.raises(ValueError):
        compare_output("5", "5", "invalid")