from fastapi import APIRouter, HTTPException, Query

from backend.problems.api_models import ProblemResponse
from backend.problems.difficulty import Difficulty
from backend.problems.pattern import DSAPattern
from backend.problems.problem_service import (
    ProblemNotFoundError,
    get_problem,
    list_problems,
)


router = APIRouter(
    prefix="/api/problems",
    tags=["Problems"],
)


@router.get(
    "",
    response_model=list[ProblemResponse],
)
def get_problems(
    difficulty: Difficulty | None = Query(default=None),
    pattern: DSAPattern | None = Query(default=None),
) -> list[ProblemResponse]:
    """
    Return student-safe problem information.

    Hidden test cases are never exposed through this endpoint.
    """

    return list_problems(
        difficulty=difficulty,
        pattern=pattern,
    )


@router.get(
    "/{problem_id}",
    response_model=ProblemResponse,
)
def get_problem_by_id(
    problem_id: str,
) -> ProblemResponse:
    """
    Return a single student-safe problem.

    Hidden test cases are never exposed through this endpoint.
    """

    try:
        return get_problem(problem_id)

    except ProblemNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc