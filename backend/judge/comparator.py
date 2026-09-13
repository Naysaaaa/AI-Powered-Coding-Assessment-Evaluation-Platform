from typing import Literal


ComparisonMode = Literal["exact", "whitespace_normalized"]


def compare_output(
    expected: str,
    actual: str,
    mode: ComparisonMode = "exact",
) -> bool:
    """
    Compare expected and actual program output.

    Modes:
    - exact: outputs must match exactly
    - whitespace_normalized: ignores differences in whitespace
    """

    if mode == "exact":
        return expected == actual

    if mode == "whitespace_normalized":
        expected_normalized = " ".join(expected.split())
        actual_normalized = " ".join(actual.split())

        return expected_normalized == actual_normalized

    raise ValueError(f"Unsupported comparison mode: {mode}")