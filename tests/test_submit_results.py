import os

from fastapi.testclient import TestClient

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg2://quiz:quiz@localhost:5432/quizops",
)

from main import app


def test_submit_results_includes_expected_fields_and_unanswered_questions():
    client = TestClient(app)

    # 1. Obtener un quiz disponible
    quizzes_res = client.get("/quizzes")
    assert quizzes_res.status_code == 200
    quizzes = quizzes_res.json()["items"]
    assert len(quizzes) > 0

    quiz_id = quizzes[0]["quiz_id"]

    # 2. Obtener preguntas del quiz
    questions_res = client.get(f"/quizzes/{quiz_id}/questions")
    assert questions_res.status_code == 200
    questions = questions_res.json()["questions"]
    assert len(questions) >= 1

    first_question = questions[0]

    # 3. Crear intento
    attempt_res = client.post(
        "/attempts",
        json={
            "quiz_id": quiz_id,
            "username": "test_submit_results_user",
        },
    )
    assert attempt_res.status_code == 200
    attempt_id = attempt_res.json()["attempt_id"]

    # 4. Responder solo la primera pregunta
    answer_res = client.post(
        f"/attempts/{attempt_id}/answers",
        json={
            "question_id": first_question["question_id"],
            "chosen_index": 0,
        },
    )
    assert answer_res.status_code == 200
    assert answer_res.json()["ok"] is True

    # 5. Enviar submit dejando preguntas sin responder
    submit_res = client.post(f"/attempts/{attempt_id}/submit")
    assert submit_res.status_code == 200

    payload = submit_res.json()
    results = payload["results"]

    assert isinstance(results, list)
    assert len(results) == len(questions)

    # 6. Validar estructura mínima por resultado
    for result in results:
        assert "is_correct" in result
        assert "correct_option" in result
        assert "chosen_option" in result
        assert "chosen_index" in result
        assert "correct_index" in result

    # 7. Validar pregunta respondida
    answered_result = next(
        r for r in results if r["question_id"] == first_question["question_id"]
    )
    assert answered_result["chosen_index"] == 0
    assert answered_result["chosen_option"] is not None
    assert answered_result["correct_option"] is not None
    assert isinstance(answered_result["is_correct"], bool)

    # 8. Validar que no falle con preguntas sin responder
    unanswered_results = [
        r for r in results if r["question_id"] != first_question["question_id"]
    ]

    for r in unanswered_results:
        assert r["chosen_index"] is None
        assert r["chosen_option"] is None
        assert r["correct_option"] is not None
        assert r["is_correct"] is False