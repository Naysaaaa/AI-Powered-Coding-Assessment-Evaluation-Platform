from backend.judge.comparator import compare_output
from backend.judge.models.execution_result import ExecutionResult
from backend.judge.models.judge_result import JudgeResult, TestCaseResult
from backend.judge.models.test_case import TestCase
from backend.judge.models.verdict import Verdict


def judge_submission(
    execution_result: ExecutionResult,
    test_cases: list[TestCase],
    comparison_mode: str = "exact",
) -> JudgeResult:
    """
    Evaluate a submission against the provided test cases.

    The deterministic judge is responsible for the final verdict.
    AI is not involved in this decision.
    """

    total_tests = len(test_cases)

    # Handle execution-level failures first.
    if execution_result.status != "SUCCESS":
        verdict = _map_execution_status_to_verdict(execution_result.status)

        test_results = [
            TestCaseResult(
                test_case_id=test_case.test_case_id,
                verdict=verdict,
                actual_output=execution_result.stdout,
            )
            for test_case in test_cases
        ]

        return JudgeResult(
            verdict=verdict,
            total_tests=total_tests,
            passed_tests=0,
            failed_tests=total_tests,
            test_results=test_results,
        )

    # Compare program output with expected output.
    test_results = []

    for test_case in test_cases:
        passed = compare_output(
            test_case.expected_output,
            execution_result.stdout,
            comparison_mode,
        )

        test_results.append(
            TestCaseResult(
                test_case_id=test_case.test_case_id,
                verdict=(
                    Verdict.ACCEPTED
                    if passed
                    else Verdict.WRONG_ANSWER
                ),
                actual_output=execution_result.stdout,
            )
        )

    passed_tests = sum(
        1 for result in test_results
        if result.verdict == Verdict.ACCEPTED
    )

    failed_tests = total_tests - passed_tests

    final_verdict = (
        Verdict.ACCEPTED
        if failed_tests == 0
        else Verdict.WRONG_ANSWER
    )

    return JudgeResult(
        verdict=final_verdict,
        total_tests=total_tests,
        passed_tests=passed_tests,
        failed_tests=failed_tests,
        test_results=test_results,
    )


def _map_execution_status_to_verdict(status: str) -> Verdict:
    """Map execution engine status to deterministic judge verdict."""

    status_mapping = {
        "COMPILATION_ERROR": Verdict.COMPILATION_ERROR,
        "RUNTIME_ERROR": Verdict.RUNTIME_ERROR,
        "TIME_LIMIT_EXCEEDED": Verdict.TIME_LIMIT_EXCEEDED,
        "MEMORY_LIMIT_EXCEEDED": Verdict.MEMORY_LIMIT_EXCEEDED,
        "EXECUTION_ERROR": Verdict.EXECUTION_ERROR,
    }

    return status_mapping.get(status, Verdict.INTERNAL_ERROR)