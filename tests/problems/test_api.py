from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.api.problems import router


app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_get_all_problems():
    response = client.get("/api/problems")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    problem_ids = {
        problem["problem_id"]
        for problem in data
    }

    assert problem_ids == {
        "TWO_SUM",
        "REVERSE_STRING",
    }


def test_get_problem_by_id():
    response = client.get("/api/problems/TWO_SUM")

    assert response.status_code == 200

    data = response.json()

    assert data["problem_id"] == "TWO_SUM"
    assert data["title"] == "Two Sum"
    assert data["difficulty"] == "Easy"


def test_get_unknown_problem():
    response = client.get("/api/problems/UNKNOWN")

    assert response.status_code == 404


def test_filter_by_difficulty():
    response = client.get(
        "/api/problems?difficulty=Easy"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert all(
        problem["difficulty"] == "Easy"
        for problem in data
    )


def test_filter_by_pattern():
    response = client.get(
        "/api/problems?pattern=Arrays"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["problem_id"] == "TWO_SUM"


def test_filter_by_difficulty_and_pattern():
    response = client.get(
        "/api/problems"
        "?difficulty=Easy"
        "&pattern=Strings"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["problem_id"] == "REVERSE_STRING"


def test_problem_api_does_not_expose_test_cases():
    response = client.get("/api/problems/TWO_SUM")

    assert response.status_code == 200

    data = response.json()

    assert "test_cases" not in data


def test_problem_list_api_does_not_expose_test_cases():
    response = client.get("/api/problems")

    assert response.status_code == 200

    data = response.json()

    for problem in data:
        assert "test_cases" not in problem