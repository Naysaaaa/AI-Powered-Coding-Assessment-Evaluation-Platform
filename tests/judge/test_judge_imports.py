from backend.judge import compare_output, judge_submission


def test_judge_package_imports():
    assert callable(compare_output)
    assert callable(judge_submission)