from typing import Literal

from pydantic import BaseModel, Field


class TestCase(BaseModel):
    __test__ = False

    test_case_id: str
    input: str
    expected_output: str
    visibility: Literal["public", "hidden"]

    timeout_seconds: float = Field(default=2.0, gt=0)