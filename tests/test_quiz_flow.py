import os

from fastapi.testclient import TestClient

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg2://quiz:quiz@localhost:5432/quizops",
)

from main import app


def test_quiz_flow():
    client = TestClient(app)

    # 1. Listar quizzes
    quizzes_res = client.get("/quizzes")
    assert quizzes_res.status_code == 200

    quizzes_payload = quizzes_res.json()
    assert "items" in quizzes_payload
    assert isinstance(quizzes_payload["items"], list)
    assert len(quizzes_payload["items"]) > 0

    quiz = quizzes_payload["items"][0]
    quiz_id = quiz["quiz_id"]

    # 2. Obtener preguntas del quiz
    questions_res = client.get(f"/quizzes/{quiz_id}/questions")
    assert questions_res.status_code == 200

    questions_payload = questions_res.json()
    assert questions_payload["quiz_id"] == quiz_id
    assert "questions" in questions_payload
    assert isinstance(questions_payload["questions"], list)
    assert len(questions_payload["questions"]) > 0

    first_question = questions_payload["questions"][0]
    question_id = first_question["question_id"]

    # 3. Crear intento
    attempt_res = client.post(
        "/attempts",
        json={
            "quiz_id": quiz_id,
            "username": "test_quiz_flow_user",
        },
    )
    assert attempt_res.status_code == 200

    attempt_payload = attempt_res.json()
    assert "attempt_id" in attempt_payload
    attempt_id = attempt_payload["attempt_id"]

    # 4. Guardar una respuesta
    answer_res = client.post(
        f"/attempts/{attempt_id}/answers",
        json={
            "question_id": question_id,
            "chosen_index": 0,
        },
    )
    assert answer_res.status_code == 200
    assert answer_res.json()["ok"] is True

    # 5. Enviar submit
    submit_res = client.post(f"/attempts/{attempt_id}/submit")
    assert submit_res.status_code == 200

    submit_payload = submit_res.json()

    # 6. Validar respuesta final
    assert submit_payload["attempt_id"] == attempt_id
    assert "score" in submit_payload
    assert "max_score" in submit_payload
    assert "results" in submit_payload

    assert isinstance(submit_payload["score"], int)
    assert isinstance(submit_payload["max_score"], int)
    assert isinstance(submit_payload["results"], list)

    assert submit_payload["max_score"] == len(questions_payload["questions"])
    assert len(submit_payload["results"]) == len(questions_payload["questions"])

    first_result = submit_payload["results"][0]
    assert "question_id" in first_result
    assert "prompt" in first_result
    assert "options" in first_result
    assert "chosen_index" in first_result
    assert "correct_index" in first_result
    assert "is_correct" in first_result
    assert "chosen_option" in first_result
    assert "correct_option" in first_result
