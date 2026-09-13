from pydantic import BaseModel

from backend.problems.difficulty import Difficulty
from backend.problems.pattern import DSAPattern


class ExampleResponse(BaseModel):
    input: str
    output: str
    explanation: str | None = None


class ProblemResponse(BaseModel):
    problem_id: str
    title: str
    description: str
    difficulty: Difficulty
    topics: list[DSAPattern]

    constraints: list[str]

    input_format: str
    output_format: str

    examples: list[ExampleResponse]

    starter_code: dict[str, str]

    supported_languages: list[str]

    expected_time_complexity: str
    expected_space_complexity: str

    hints: list[str]

    editorial: str | None = None