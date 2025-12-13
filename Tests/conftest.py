import pytest
import json
from unittest.mock import patch

import tempfile
import os
from quiz.data import Database
from quiz.models.user import User
from quiz.models.quiz import Quiz
from quiz.models.multiplechoicequestion import MultipleChoiceQuestion
from quiz.models.attempt import Attempt

@pytest.fixture(scope="function")
def test_db():
    """
    Fixture para criar um banco de dados SQLite em um arquivo temporário para cada função de teste.
    Isso garante que os testes sejam isolados e compatíveis com a implementação da classe Database.
    """
    fd, db_path = tempfile.mkstemp(suffix=".db")
    
    try:
        db = Database(db_path)
        db.create_tables()
        yield db
    finally:
        os.close(fd)
        os.unlink(db_path)

@pytest.fixture
def sample_user():
    """Retorna um objeto User de exemplo."""
    return User(name="Test User", email="test@user.com")


@pytest.fixture
def sample_questions():
    """Retorna uma lista de questões de exemplo."""
    return [
        MultipleChoiceQuestion(
            id_question=None,
            statement="Qual a capital da França?",
            difficulty=1,
            theme="Geografia",
            alternatives=["Berlim", "Londres", "Paris", "Madri"],
            correct_answer=2
        ),
        MultipleChoiceQuestion(
            id_question=None,
            statement="Qual o resultado de 2+2?",
            difficulty=1,
            theme="Matemática",
            alternatives=["3", "4", "5"],
            correct_answer=1
        )
    ]


@pytest.fixture
def sample_quiz(sample_questions):
    """Retorna um objeto Quiz de exemplo com questões."""
    return Quiz(
        id_quiz=None,
        title="Quiz Geral",
        questions=sample_questions,
        attempt_limit=3,
        time_limit=10
    )


@pytest.fixture
def populated_db(test_db, sample_user, sample_quiz):
    """
    Fixture que retorna um banco de dados já populado com um usuário e um quiz.
    """
    # Adiciona usuário
    user_id = test_db.add_user(sample_user)
    sample_user.id_user = user_id

    # Adiciona quiz
    test_db.add_quiz(sample_quiz)

    return test_db, sample_user, sample_quiz