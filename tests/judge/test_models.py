from backend.judge.models.verdict import Verdict


def test_verdict_accepted():
    assert Verdict.ACCEPTED.value == "ACCEPTED"


def test_verdict_wrong_answer():
    assert Verdict.WRONG_ANSWER.value == "WRONG_ANSWER"


def test_all_verdicts_exist():
    assert len(Verdict) == 8