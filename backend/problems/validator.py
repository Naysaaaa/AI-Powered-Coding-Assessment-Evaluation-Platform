from collections import Counter

from backend.problems.models import Problem


SUPPORTED_LANGUAGES = {
    "python",
    "java",
    "cpp",
}


def validate_problem(problem: Problem) -> list[str]:
    """
    Validate a single problem definition.

    Returns:
        A list of validation errors.
        An empty list means the problem is valid.
    """

    errors: list[str] = []

    # Basic metadata
    if not problem.problem_id.strip():
        errors.append("problem_id cannot be empty.")

    if not problem.title.strip():
        errors.append("title cannot be empty.")

    if not problem.description.strip():
        errors.append("description cannot be empty.")

    # Topics
    if not problem.topics:
        errors.append("At least one DSA pattern is required.")

    # Languages
    if not problem.supported_languages:
        errors.append(
            "At least one supported language is required."
        )

    unsupported_languages = (
        set(problem.supported_languages) - SUPPORTED_LANGUAGES
    )

    if unsupported_languages:
        errors.append(
            "Unsupported languages: "
            + ", ".join(sorted(unsupported_languages))
        )

    # Starter code
    for language in problem.supported_languages:
        starter_code = problem.starter_code.get(language)

        if not starter_code or not starter_code.strip():
            errors.append(
                f"Missing starter code for language: {language}"
            )

    # Complexity metadata
    if not problem.expected_time_complexity.strip():
        errors.append(
            "expected_time_complexity cannot be empty."
        )

    if not problem.expected_space_complexity.strip():
        errors.append(
            "expected_space_complexity cannot be empty."
        )

    # Test cases
    if not problem.test_cases:
        errors.append(
            "At least one test case is required."
        )
        return errors

    test_case_ids = [
        test_case.test_case_id
        for test_case in problem.test_cases
    ]

    duplicate_ids = [
        test_case_id
        for test_case_id, count in Counter(test_case_ids).items()
        if count > 1
    ]

    if duplicate_ids:
        errors.append(
            "Duplicate test case IDs: "
            + ", ".join(sorted(duplicate_ids))
        )

    # Public/hidden coverage
    has_public = any(
        test_case.visibility == "public"
        for test_case in problem.test_cases
    )

    has_hidden = any(
        test_case.visibility == "hidden"
        for test_case in problem.test_cases
    )

    if not has_public:
        errors.append(
            "At least one public test case is required."
        )

    if not has_hidden:
        errors.append(
            "At least one hidden test case is required."
        )

    return errors


def validate_problems(
    problems: list[Problem],
) -> list[str]:
    """
    Validate the complete problem library.

    Checks both individual problems and
    cross-problem uniqueness.
    """

    errors: list[str] = []

    # Duplicate problem IDs
    problem_ids = [
        problem.problem_id
        for problem in problems
    ]

    duplicate_ids = [
        problem_id
        for problem_id, count in Counter(problem_ids).items()
        if count > 1
    ]

    for problem_id in sorted(duplicate_ids):
        errors.append(
            f"Duplicate problem_id: {problem_id}"
        )

    # Duplicate titles
    titles = [
        problem.title.strip().lower()
        for problem in problems
    ]

    duplicate_titles = [
        title
        for title, count in Counter(titles).items()
        if count > 1
    ]

    for title in sorted(duplicate_titles):
        errors.append(
            f"Duplicate problem title: {title}"
        )

    # Individual problem validation
    for problem in problems:
        problem_errors = validate_problem(problem)

        for error in problem_errors:
            errors.append(
                f"{problem.problem_id}: {error}"
            )

    return errors