import json
import os
from pathlib import Path

from sqlalchemy import create_engine, text


DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://quiz:quiz@db:5432/quizops",
)


def get_or_create_quiz(conn, title, description):
    row = conn.execute(
        text(
            """
            SELECT quiz_id
            FROM quizzes
            WHERE title = :title
            """
        ),
        {"title": title},
    ).mappings().first()

    if row:
        return row["quiz_id"]

    return conn.execute(
        text(
            """
            INSERT INTO quizzes(title, description)
            VALUES(:title, :description)
            RETURNING quiz_id
            """
        ),
        {"title": title, "description": description},
    ).scalar_one()


def get_or_create_question(conn, q):
    row = conn.execute(
        text(
            """
            SELECT question_id
            FROM questions
            WHERE prompt = :prompt
              AND COALESCE(topic, '') = COALESCE(:topic, '')
            """
        ),
        {
            "prompt": q["prompt"],
            "topic": q.get("topic"),
        },
    ).mappings().first()

    if row:
        return row["question_id"]

    return conn.execute(
        text(
            """
            INSERT INTO questions(
                prompt,
                options,
                correct_index,
                topic,
                difficulty,
                explanation
            )
            VALUES(
                :prompt,
                CAST(:options AS jsonb),
                :correct_index,
                :topic,
                :difficulty,
                :explanation
            )
            RETURNING question_id
            """
        ),
        {
            "prompt": q["prompt"],
            "options": json.dumps(q["options"], ensure_ascii=False),
            "correct_index": q["correct_index"],
            "topic": q.get("topic"),
            "difficulty": q.get("difficulty", 1),
            "explanation": q.get("explanation"),
        },
    ).scalar_one()


def link_question_to_quiz(conn, quiz_id, question_id):
    conn.execute(
        text(
            """
            INSERT INTO quiz_questions(quiz_id, question_id)
            VALUES(:quiz_id, :question_id)
            ON CONFLICT (quiz_id, question_id) DO NOTHING
            """
        ),
        {"quiz_id": quiz_id, "question_id": question_id},
    )


def main():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    file_path = Path("/data/questions/sql_python_de.json")
    payload = json.loads(file_path.read_text(encoding="utf-8"))

    questions = payload["questions"]
    topics = sorted({q["topic"] for q in questions if q.get("topic")})

    with engine.begin() as conn:
        integrador_title = f'{payload["title"]} - Integrador'
        integrador_description = "Quiz integrador con preguntas de todos los topics."

        integrador_quiz_id = get_or_create_quiz(
            conn,
            integrador_title,
            integrador_description,
        )

        topic_quiz_ids = {}
        for topic in topics:
            topic_title = f'{payload["title"]} - {topic}'
            topic_description = f'Quiz temático del topic: {topic}.'

            topic_quiz_ids[topic] = get_or_create_quiz(
                conn,
                topic_title,
                topic_description,
            )

        for q in questions:
            question_id = get_or_create_question(conn, q)

            topic = q.get("topic")
            if topic in topic_quiz_ids:
                link_question_to_quiz(conn, topic_quiz_ids[topic], question_id)

            link_question_to_quiz(conn, integrador_quiz_id, question_id)

    print("Seed OK.")
    print(f"Topics detectados: {len(topics)}")
    print(f"Quizzes temáticos creados/verificados: {len(topics)}")
    print("Quiz integrador creado/verificado: 1")
    print(f"Preguntas procesadas: {len(questions)}")


if __name__ == "__main__":
    main()