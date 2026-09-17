import json
from pathlib import Path

from backend.problems.models import Problem
from backend.problems.validator import validate_problem, validate_problems


DATA_DIRECTORY = Path(__file__).parent / "data"


def load_problem_file(file_path: Path) -> list[Problem]:
    """
    Load and validate problems from a single JSON file.

    Each JSON file must contain a JSON array of problem definitions.
    """

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            f"Invalid problem file '{file_path.name}': "
            "expected a JSON array of problems."
        )

    problems = []

    for index, problem_data in enumerate(data):
        try:
            problem = Problem.model_validate(problem_data)
        except Exception as exc:
            raise ValueError(
                f"Invalid problem definition in "
                f"'{file_path.name}' at index {index}: {exc}"
            ) from exc

        validation_errors = validate_problem(problem)

        if validation_errors:
            error_message = (
                f"Invalid problem definition in "
                f"'{file_path.name}' at index {index} "
                f"({problem.problem_id}):\n"
                + "\n".join(
                    f"- {error}"
                    for error in validation_errors
                )
            )

            raise ValueError(error_message)

        problems.append(problem)

    return problems


def load_all_problems() -> list[Problem]:
    """
    Load and validate all problems from JSON files.

    Individual problems are validated first.
    Then the complete collection is validated to detect
    duplicate problem IDs or titles across files.
    """

    problems = []

    for file_path in sorted(DATA_DIRECTORY.glob("*.json")):
        problems.extend(load_problem_file(file_path))

    validation_errors = validate_problems(problems)

    if validation_errors:
        error_message = (
            "Problem library validation failed:\n"
            + "\n".join(
                f"- {error}"
                for error in validation_errors
            )
        )

        raise ValueError(error_message)

    return problems