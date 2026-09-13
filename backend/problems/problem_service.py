from backend.problems.difficulty import Difficulty
from backend.problems.models import Problem
from backend.problems.pattern import DSAPattern
from backend.problems.repository import (
    get_all_problems,
    get_problem_by_id,
    get_problems_by_difficulty,
    get_problems_by_pattern,
)


class ProblemNotFoundError(Exception):
    """Raised when a requested problem does not exist."""


def list_problems(
    difficulty: Difficulty | None = None,
    pattern: DSAPattern | None = None,
) -> list[Problem]:
    """
    Return problems with optional difficulty and pattern filtering.
    """

    if difficulty is not None and pattern is not None:
        return [
            problem
            for problem in get_all_problems()
            if problem.difficulty == difficulty
            and pattern in problem.topics
        ]

    if difficulty is not None:
        return get_problems_by_difficulty(difficulty)

    if pattern is not None:
        return get_problems_by_pattern(pattern)

    return get_all_problems()


def get_problem(problem_id: str) -> Problem:
    """
    Return a problem by ID.

    Raises:
        ProblemNotFoundError: If the problem does not exist.
    """

    problem = get_problem_by_id(problem_id)

    if problem is None:
        raise ProblemNotFoundError(
            f"Problem '{problem_id}' was not found."
        )

    return problem