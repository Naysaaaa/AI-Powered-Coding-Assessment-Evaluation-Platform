from backend.judge.models.test_case import TestCase
from backend.problems.difficulty import Difficulty
from backend.problems.models import Problem
from backend.problems.pattern import DSAPattern
from backend.problems.validator import (
    validate_problem,
    validate_problems,
)


def create_valid_problem(
    problem_id: str = "TEST_PROBLEM",
    title: str = "Test Problem",
) -> Problem:
    return Problem(
        problem_id=problem_id,
        title=title,
        description="A valid test problem.",
        difficulty=Difficulty.EASY,
        topics=[DSAPattern.ARRAYS],
        input_format="An integer",
        output_format="An integer",
        starter_code={
            "python": "print()",
        },
        supported_languages=["python"],
        expected_time_complexity="O(1)",
        expected_space_complexity="O(1)",
        test_cases=[
            TestCase(
                test_case_id="PUBLIC_001",
                input="1",
                expected_output="1",
                visibility="public",
            ),
            TestCase(
                test_case_id="HIDDEN_001",
                input="2",
                expected_output="2",
                visibility="hidden",
            ),
        ],
    )


def test_valid_problem_has_no_errors():
    problem = create_valid_problem()

    errors = validate_problem(problem)

    assert errors == []


def test_problem_requires_test_cases():
    problem = create_valid_problem()

    problem.test_cases = []

    errors = validate_problem(problem)

    assert "At least one test case is required." in errors


def test_problem_requires_public_test_case():
    problem = create_valid_problem()

    problem.test_cases = [
        TestCase(
            test_case_id="HIDDEN_001",
            input="2",
            expected_output="2",
            visibility="hidden",
        )
    ]

    errors = validate_problem(problem)

    assert "At least one public test case is required." in errors


def test_problem_requires_hidden_test_case():
    problem = create_valid_problem()

    problem.test_cases = [
        TestCase(
            test_case_id="PUBLIC_001",
            input="1",
            expected_output="1",
            visibility="public",
        )
    ]

    errors = validate_problem(problem)

    assert "At least one hidden test case is required." in errors


def test_duplicate_test_case_ids_are_detected():
    problem = create_valid_problem()

    problem.test_cases[1].test_case_id = "PUBLIC_001"

    errors = validate_problem(problem)

    assert any(
        "Duplicate test case IDs" in error
        for error in errors
    )


def test_duplicate_problem_ids_are_detected():
    problem_one = create_valid_problem(
        problem_id="PROBLEM_001",
        title="Problem One",
    )

    problem_two = create_valid_problem(
        problem_id="PROBLEM_001",
        title="Problem Two",
    )

    errors = validate_problems(
        [problem_one, problem_two]
    )

    assert "Duplicate problem_id: PROBLEM_001" in errors


def test_duplicate_titles_are_detected():
    problem_one = create_valid_problem(
        problem_id="PROBLEM_001",
        title="Same Problem",
    )

    problem_two = create_valid_problem(
        problem_id="PROBLEM_002",
        title="Same Problem",
    )

    errors = validate_problems(
        [problem_one, problem_two]
    )

    assert "Duplicate problem title: same problem" in errors