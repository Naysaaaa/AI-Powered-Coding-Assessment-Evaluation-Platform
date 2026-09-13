from pydantic import BaseModel

from backend.judge.models.verdict import Verdict


class TestCaseResult(BaseModel):
    __test__ = False

    test_case_id: str
    verdict: Verdict
    actual_output: str | None = None


class JudgeResult(BaseModel):
    verdict: Verdict
    total_tests: int
    passed_tests: int
    failed_tests: int
    test_results: list[TestCaseResult]