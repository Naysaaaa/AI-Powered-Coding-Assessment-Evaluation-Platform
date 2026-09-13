from backend.problems.difficulty import Difficulty
from backend.problems.pattern import DSAPattern
from backend.problems.repository import (
    get_all_problems,
    get_problem_by_id,
    get_problems_by_difficulty,
    get_problems_by_pattern,
)


def test_get_all_problems():
    problems = get_all_problems()

    assert len(problems) == 2


def test_get_problem_by_id():
    problem = get_problem_by_id("TWO_SUM")

    assert problem is not None
    assert problem.problem_id == "TWO_SUM"
    assert problem.title == "Two Sum"


def test_get_nonexistent_problem():
    problem = get_problem_by_id("DOES_NOT_EXIST")

    assert problem is None


def test_get_problems_by_difficulty():
    problems = get_problems_by_difficulty(Difficulty.EASY)

    assert len(problems) == 2
    assert all(problem.difficulty == Difficulty.EASY for problem in problems)


def test_get_problems_by_pattern():
    problems = get_problems_by_pattern(DSAPattern.ARRAYS)

    assert len(problems) == 1
    assert problems[0].problem_id == "TWO_SUM"


def test_two_sum_has_required_metadata():
    problem = get_problem_by_id("TWO_SUM")

    assert problem is not None
    assert DSAPattern.ARRAYS in problem.topics
    assert DSAPattern.HASHING in problem.topics
    assert problem.expected_time_complexity == "O(n)"
    assert problem.expected_space_complexity == "O(n)"
    assert "python" in problem.supported_languages
    assert len(problem.hints) == 3