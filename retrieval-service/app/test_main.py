from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_empty_question_is_rejected():
    response = client.post(
        "/ask",
        json={
            "question": "",
        },
    )

    assert response.status_code == 422


def test_whitespace_question_is_rejected():
    response = client.post(
        "/ask",
        json={
            "question": "     ",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Question cannot be empty."
    )


def test_successful_question(monkeypatch):
    expected_result = {
        "answer": "Sequential search checks elements one by one.",
        "sources": [
            {
                "source": "DAA_Unit_2.pdf",
                "page_start": 7,
                "page_end": 7,
            }
        ],
        "answered": True,
    }

    def mock_answer(question: str):
        assert question == "What is sequential search?"
        return expected_result

    monkeypatch.setattr(
        "app.main.pipeline.answer",
        mock_answer,
    )

    response = client.post(
        "/ask",
        json={
            "question": "What is sequential search?",
        },
    )

    assert response.status_code == 200
    assert response.json() == expected_result

def test_pipeline_error_returns_503(monkeypatch):
    def mock_answer(question: str):
        raise RuntimeError(
            "Unable to connect to the AI service."
        )

    monkeypatch.setattr(
        "app.main.pipeline.answer",
        mock_answer,
    )

    response = client.post(
        "/ask",
        json={
            "question": "What is sequential search?",
        },
    )

    assert response.status_code == 503

    assert response.json()["detail"] == (
        "Unable to connect to the AI service."
    )