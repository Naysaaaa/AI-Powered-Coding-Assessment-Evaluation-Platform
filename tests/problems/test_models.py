from backend.problems.difficulty import Difficulty
from backend.problems.models import Example, Problem
from backend.problems.pattern import DSAPattern


def test_difficulty_values():
    assert Difficulty.EASY.value == "Easy"
    assert Difficulty.MEDIUM.value == "Medium"
    assert Difficulty.HARD.value == "Hard"


def test_dsa_pattern_values():
    assert DSAPattern.ARRAYS.value == "Arrays"
    assert DSAPattern.HASHING.value == "Hashing"
    assert DSAPattern.TWO_POINTERS.value == "Two Pointers"
    assert DSAPattern.DYNAMIC_PROGRAMMING.value == "Dynamic Programming"


def test_example_model():
    example = Example(
        input="2 3",
        output="5",
        explanation="Add the two numbers.",
    )

    assert example.input == "2 3"
    assert example.output == "5"
    assert example.explanation == "Add the two numbers."


def test_problem_model():
    problem = Problem(
        problem_id="TWO_SUM",
        title="Two Sum",
        description="Find two numbers that add up to a target.",
        difficulty=Difficulty.EASY,
        topics=[
            DSAPattern.ARRAYS,
            DSAPattern.HASHING,
        ],
        input_format="Array and target",
        output_format="Indices of the two numbers",
        supported_languages=["python", "java", "cpp"],
        expected_time_complexity="O(n)",
        expected_space_complexity="O(n)",
    )

    assert problem.problem_id == "TWO_SUM"
    assert problem.difficulty == Difficulty.EASY
    assert len(problem.topics) == 2
    assert problem.supported_languages == [
        "python",
        "java",
        "cpp",
    ]
    assert problem.hints == []
    assert problem.examples == []
    assert problem.test_cases == []


def test_problem_with_examples_and_hints():
    problem = Problem(
        problem_id="REV_STRING",
        title="Reverse String",
        description="Reverse a string.",
        difficulty=Difficulty.EASY,
        topics=[DSAPattern.STRINGS],
        input_format="A string",
        output_format="The reversed string",
        supported_languages=["python"],
        expected_time_complexity="O(n)",
        expected_space_complexity="O(n)",
        examples=[
            Example(
                input="hello",
                output="olleh",
                explanation="Read the string from right to left.",
            )
        ],
        hints=[
            "Think about two pointers.",
            "Swap characters from both ends.",
        ],
        editorial="Use two pointers moving toward the center.",
    )

    assert len(problem.examples) == 1
    assert len(problem.hints) == 2
    assert problem.editorial is not None
    assert problem.test_cases == []


def test_problem_contains_test_cases():
    problem = Problem(
        problem_id="TEST_CASE_PROBLEM",
        title="Test Problem",
        description="A problem with test cases.",
        difficulty=Difficulty.EASY,
        topics=[DSAPattern.ARRAYS],
        input_format="An integer",
        output_format="The integer",
        supported_languages=["python"],
        expected_time_complexity="O(1)",
        expected_space_complexity="O(1)",
        test_cases=[
            {
                "test_case_id": "TC001",
                "input": "5",
                "expected_output": "5",
                "visibility": "public",
            },
            {
                "test_case_id": "TC002",
                "input": "10",
                "expected_output": "10",
                "visibility": "hidden",
            },
        ],
    )

    assert len(problem.test_cases) == 2

    assert problem.test_cases[0].test_case_id == "TC001"
    assert problem.test_cases[0].visibility == "public"
    assert problem.test_cases[0].input == "5"
    assert problem.test_cases[0].expected_output == "5"

    assert problem.test_cases[1].test_case_id == "TC002"
    assert problem.test_cases[1].visibility == "hidden"
    assert problem.test_cases[1].input == "10"
    assert problem.test_cases[1].expected_output == "10"