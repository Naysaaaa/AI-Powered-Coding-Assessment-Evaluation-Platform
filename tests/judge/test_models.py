from backend.judge.models.execution_result import ExecutionResult
from backend.judge.models.judge_result import JudgeResult, TestCaseResult
from backend.judge.models.test_case import TestCase as JudgeTestCase
from backend.judge.models.verdict import Verdict


def test_verdict_accepted():
    assert Verdict.ACCEPTED.value == "ACCEPTED"


def test_verdict_wrong_answer():
    assert Verdict.WRONG_ANSWER.value == "WRONG_ANSWER"


def test_all_verdicts_exist():
    assert len(Verdict) == 8


def test_public_test_case():
    test_case = JudgeTestCase(
        test_case_id="TC001",
        input="2 3",
        expected_output="5",
        visibility="public",
    )

    assert test_case.test_case_id == "TC001"
    assert test_case.visibility == "public"
    assert test_case.timeout_seconds == 2.0


def test_hidden_test_case():
    test_case = JudgeTestCase(
        test_case_id="TC002",
        input="10 20",
        expected_output="30",
        visibility="hidden",
    )

    assert test_case.visibility == "hidden"


def test_invalid_visibility():
    try:
        JudgeTestCase(
            test_case_id="TC003",
            input="1",
            expected_output="1",
            visibility="private",
        )
        assert False
    except ValueError:
        assert True


def test_execution_result_success():
    result = ExecutionResult(
        status="SUCCESS",
        stdout="5",
        stderr="",
        exit_code=0,
        execution_time=0.25,
        memory_used=1024,
    )

    assert result.status == "SUCCESS"
    assert result.stdout == "5"
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.execution_time == 0.25
    assert result.memory_used == 1024


def test_execution_result_runtime_error():
    result = ExecutionResult(
        status="RUNTIME_ERROR",
        stdout="",
        stderr="IndexError",
        exit_code=1,
        execution_time=0.10,
        memory_used=2048,
    )

    assert result.status == "RUNTIME_ERROR"
    assert result.stderr == "IndexError"
    assert result.exit_code == 1


def test_execution_result_rejects_negative_execution_time():
    try:
        ExecutionResult(
            status="SUCCESS",
            stdout="5",
            stderr="",
            exit_code=0,
            execution_time=-1,
            memory_used=1024,
        )
        assert False
    except ValueError:
        assert True


def test_execution_result_rejects_negative_memory():
    try:
        ExecutionResult(
            status="SUCCESS",
            stdout="5",
            stderr="",
            exit_code=0,
            execution_time=0.2,
            memory_used=-100,
        )
        assert False
    except ValueError:
        assert True


def test_test_case_result():
    result = TestCaseResult(
        test_case_id="TC001",
        verdict=Verdict.ACCEPTED,
        actual_output="5",
    )

    assert result.test_case_id == "TC001"
    assert result.verdict == Verdict.ACCEPTED
    assert result.actual_output == "5"


def test_judge_result():
    test_results = [
        TestCaseResult(
            test_case_id="TC001",
            verdict=Verdict.ACCEPTED,
            actual_output="5",
        ),
        TestCaseResult(
            test_case_id="TC002",
            verdict=Verdict.WRONG_ANSWER,
            actual_output="4",
        ),
    ]

    result = JudgeResult(
        verdict=Verdict.WRONG_ANSWER,
        total_tests=2,
        passed_tests=1,
        failed_tests=1,
        test_results=test_results,
    )

    assert result.verdict == Verdict.WRONG_ANSWER
    assert result.total_tests == 2
    assert result.passed_tests == 1
    assert result.failed_tests == 1
    assert len(result.test_results) == 2


def test_test_case_result_without_actual_output():
    result = TestCaseResult(
        test_case_id="TC003",
        verdict=Verdict.RUNTIME_ERROR,
    )

    assert result.actual_output is None