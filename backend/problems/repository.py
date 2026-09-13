from backend.problems.difficulty import Difficulty
from backend.problems.loader import load_all_problems
from backend.problems.models import Problem
from backend.problems.pattern import DSAPattern


def get_all_problems() -> list[Problem]:
    """Return all available problems."""
    return load_all_problems()


def get_problem_by_id(problem_id: str) -> Problem | None:
    """Return a problem by its ID."""
    for problem in get_all_problems():
        if problem.problem_id == problem_id:
            return problem

    return None


def get_problems_by_difficulty(
    difficulty: Difficulty,
) -> list[Problem]:
    """Return problems matching the requested difficulty."""
    return [
        problem
        for problem in get_all_problems()
        if problem.difficulty == difficulty
    ]


def get_problems_by_pattern(
    pattern: DSAPattern,
) -> list[Problem]:
    """Return problems containing the requested DSA pattern."""
    return [
        problem
        for problem in get_all_problems()
        if pattern in problem.topics
    ]