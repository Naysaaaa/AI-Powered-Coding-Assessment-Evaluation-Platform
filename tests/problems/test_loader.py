import json

import pytest

from backend.problems.loader import (
    load_all_problems,
    load_problem_file,
)


def test_load_all_problems():
    problems = load_all_problems()

    assert len(problems) == 2


def test_loaded_problem_ids():
    problems = load_all_problems()

    problem_ids = {
        problem.problem_id
        for problem in problems
    }

    assert problem_ids == {
        "TWO_SUM",
        "REVERSE_STRING",
    }


def test_load_two_sum():
    problems = load_all_problems()

    two_sum = next(
        problem
        for problem in problems
        if problem.problem_id == "TWO_SUM"
    )

    assert two_sum.title == "Two Sum"
    assert two_sum.difficulty.value == "Easy"
    assert len(two_sum.examples) == 2
    assert len(two_sum.hints) == 3
    assert len(two_sum.test_cases) == 4


def test_load_reverse_string():
    problems = load_all_problems()

    reverse_string = next(
        problem
        for problem in problems
        if problem.problem_id == "REVERSE_STRING"
    )

    assert reverse_string.title == "Reverse String"
    assert len(reverse_string.test_cases) == 4


def test_load_single_problem_file(tmp_path):
    problem_data = [
        {
            "problem_id": "VALIDATION_TEST",
            "title": "Validation Test",
            "description": "A valid problem for loader testing.",
            "difficulty": "Easy",
            "topics": ["Arrays"],
            "constraints": [],
            "input_format": "An integer",
            "output_format": "An integer",
            "examples": [],
            "starter_code": {
                "python": "print(1)",
            },
            "supported_languages": ["python"],
            "expected_time_complexity": "O(1)",
            "expected_space_complexity": "O(1)",
            "hints": [],
            "editorial": None,
            "test_cases": [
                {
                    "test_case_id": "PUBLIC_001",
                    "input": "1",
                    "expected_output": "1",
                    "visibility": "public",
                    "timeout_seconds": 2.0,
                },
                {
                    "test_case_id": "HIDDEN_001",
                    "input": "2",
                    "expected_output": "2",
                    "visibility": "hidden",
                    "timeout_seconds": 2.0,
                },
            ],
        }
    ]

    file_path = tmp_path / "valid_problem.json"

    file_path.write_text(
        json.dumps(problem_data),
        encoding="utf-8",
    )

    problems = load_problem_file(file_path)

    assert len(problems) == 1
    assert problems[0].problem_id == "VALIDATION_TEST"


def test_load_problem_rejects_invalid_definition(tmp_path):
    invalid_problem_data = [
        {
            "problem_id": "INVALID_TEST",
            "title": "Invalid Test",
            "description": "This problem has no test cases.",
            "difficulty": "Easy",
            "topics": ["Arrays"],
            "constraints": [],
            "input_format": "An integer",
            "output_format": "An integer",
            "examples": [],
            "starter_code": {
                "python": "print(1)",
            },
            "supported_languages": ["python"],
            "expected_time_complexity": "O(1)",
            "expected_space_complexity": "O(1)",
            "hints": [],
            "editorial": None,
            "test_cases": [],
        }
    ]

    file_path = tmp_path / "invalid_problem.json"

    file_path.write_text(
        json.dumps(invalid_problem_data),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="At least one test case is required",
    ):
        load_problem_file(file_path)


def test_load_all_problems_rejects_duplicate_problem_ids(
    tmp_path,
    monkeypatch,
):
    problem_template = {
        "problem_id": "DUPLICATE_TEST",
        "title": "Duplicate Test",
        "description": "A problem used to test duplicate IDs.",
        "difficulty": "Easy",
        "topics": ["Arrays"],
        "constraints": [],
        "input_format": "An integer",
        "output_format": "An integer",
        "examples": [],
        "starter_code": {
            "python": "print(1)",
        },
        "supported_languages": ["python"],
        "expected_time_complexity": "O(1)",
        "expected_space_complexity": "O(1)",
        "hints": [],
        "editorial": None,
        "test_cases": [
            {
                "test_case_id": "PUBLIC_001",
                "input": "1",
                "expected_output": "1",
                "visibility": "public",
                "timeout_seconds": 2.0,
            },
            {
                "test_case_id": "HIDDEN_001",
                "input": "2",
                "expected_output": "2",
                "visibility": "hidden",
                "timeout_seconds": 2.0,
            },
        ],
    }

    file_one = tmp_path / "arrays.json"
    file_two = tmp_path / "strings.json"

    file_one.write_text(
        json.dumps([problem_template]),
        encoding="utf-8",
    )

    file_two.write_text(
        json.dumps([problem_template]),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "backend.problems.loader.DATA_DIRECTORY",
        tmp_path,
    )

    with pytest.raises(
        ValueError,
        match="Duplicate problem_id: DUPLICATE_TEST",
    ):
        load_all_problems()