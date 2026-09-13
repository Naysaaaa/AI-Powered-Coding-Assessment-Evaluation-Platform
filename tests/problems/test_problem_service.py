import pytest

from backend.problems.difficulty import Difficulty
from backend.problems.pattern import DSAPattern
from backend.problems.problem_service import (
    ProblemNotFoundError,
    get_problem,
    list_problems,
)


def test_list_all_problems():
    problems = list_problems()

    assert len(problems) == 2


def test_list_problems_by_difficulty():
    problems = list_problems(
        difficulty=Difficulty.EASY,
    )

    assert len(problems) == 2
    assert all(
        problem.difficulty == Difficulty.EASY
        for problem in problems
    )


def test_list_problems_by_pattern():
    problems = list_problems(
        pattern=DSAPattern.ARRAYS,
    )

    assert len(problems) == 1
    assert problems[0].problem_id == "TWO_SUM"


def test_list_problems_by_difficulty_and_pattern():
    problems = list_problems(
        difficulty=Difficulty.EASY,
        pattern=DSAPattern.STRINGS,
    )

    assert len(problems) == 1
    assert problems[0].problem_id == "REVERSE_STRING"


def test_get_problem():
    problem = get_problem("TWO_SUM")

    assert problem.problem_id == "TWO_SUM"
    assert problem.title == "Two Sum"


def test_get_missing_problem():
    with pytest.raises(ProblemNotFoundError):
        get_problem("UNKNOWN_PROBLEM")