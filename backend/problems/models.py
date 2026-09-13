from pydantic import BaseModel, Field

from backend.judge.models.test_case import TestCase
from backend.problems.difficulty import Difficulty
from backend.problems.pattern import DSAPattern


class Example(BaseModel):
    input: str
    output: str
    explanation: str | None = None


class Problem(BaseModel):
    problem_id: str
    title: str
    description: str
    difficulty: Difficulty
    topics: list[DSAPattern]

    constraints: list[str] = Field(default_factory=list)

    input_format: str
    output_format: str

    examples: list[Example] = Field(default_factory=list)

    starter_code: dict[str, str] = Field(default_factory=dict)

    supported_languages: list[str]

    expected_time_complexity: str
    expected_space_complexity: str

    hints: list[str] = Field(default_factory=list)

    editorial: str | None = None

    test_cases: list[TestCase] = Field(default_factory=list)