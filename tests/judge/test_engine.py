from backend.judge.engine import judge_submission
from backend.judge.models.execution_result import ExecutionResult
from backend.judge.models.test_case import TestCase
from backend.judge.models.verdict import Verdict


def create_test_cases():
    return [
        TestCase(
            test_case_id="TC001",
            input="2 3",
            expected_output="5",
            visibility="public",
        ),
        TestCase(
            test_case_id="TC002",
            input="10 20",
            expected_output="30",
            visibility="hidden",
        ),
    ]


def test_judge_accepts_correct_submission():
    execution_result = ExecutionResult(
        status="SUCCESS",
        stdout="5",
        stderr="",
        exit_code=0,
        execution_time=0.2,
        memory_used=1024,
    )

    result = judge_submission(
        execution_result,
        create_test_cases()[:1],
    )

    assert result.verdict == Verdict.ACCEPTED
    assert result.total_tests == 1
    assert result.passed_tests == 1
    assert result.failed_tests == 0


def test_judge_rejects_wrong_answer():
    execution_result = ExecutionResult(
        status="SUCCESS",
        stdout="4",
        stderr="",
        exit_code=0,
        execution_time=0.2,
        memory_used=1024,
    )

    result = judge_submission(
        execution_result,
        create_test_cases()[:1],
    )

    assert result.verdict == Verdict.WRONG_ANSWER
    assert result.total_tests == 1
    assert result.passed_tests == 0
    assert result.failed_tests == 1


def test_judge_handles_runtime_error():
    execution_result = ExecutionResult(
        status="RUNTIME_ERROR",
        stdout="",
        stderr="IndexError",
        exit_code=1,
        execution_time=0.1,
        memory_used=1024,
    )

    result = judge_submission(
        execution_result,
        create_test_cases(),
    )

    assert result.verdict == Verdict.RUNTIME_ERROR
    assert result.passed_tests == 0
    assert result.failed_tests == 2


def test_judge_handles_compilation_error():
    execution_result = ExecutionResult(
        status="COMPILATION_ERROR",
        stdout="",
        stderr="SyntaxError",
        exit_code=1,
        execution_time=0.05,
        memory_used=512,
    )

    result = judge_submission(
        execution_result,
        create_test_cases(),
    )

    assert result.verdict == Verdict.COMPILATION_ERROR


def test_judge_handles_timeout():
    execution_result = ExecutionResult(
        status="TIME_LIMIT_EXCEEDED",
        stdout="",
        stderr="",
        exit_code=-1,
        execution_time=2.0,
        memory_used=1024,
    )

    result = judge_submission(
        execution_result,
        create_test_cases(),
    )

    assert result.verdict == Verdict.TIME_LIMIT_EXCEEDED


def test_judge_uses_whitespace_normalization():
    execution_result = ExecutionResult(
        status="SUCCESS",
        stdout="5\n",
        stderr="",
        exit_code=0,
        execution_time=0.2,
        memory_used=1024,
    )

    result = judge_submission(
        execution_result,
        create_test_cases()[:1],
        comparison_mode="whitespace_normalized",
    )

    assert result.verdict == Verdict.ACCEPTED