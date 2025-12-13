import pytest
from quiz.models.question import Question
from quiz.models.multiplechoicequestion import MultipleChoiceQuestion
from quiz.models.quiz import Quiz
from quiz.models.user import User
from quiz.models.attempt import Attempt

def test_question_equality():
    q1 = Question(id_question=1, statement="Enunciado", difficulty=1, theme="Tema")
    q2 = Question(id_question=2, statement="Enunciado", difficulty=2, theme="Tema")
    q3 = Question(id_question=3, statement="Outro Enunciado", difficulty=1, theme="Tema")
    assert q1 == q2
    assert q1 != q3

def test_multiple_choice_question_str(sample_questions):
    question = sample_questions[0]
    expected_str = "Qual a capital da França?\n  1. Berlim\n  2. Londres\n  3. Paris\n  4. Madri"
    assert str(question) == expected_str

def test_multiple_choice_question_alternatives_validation():
    with pytest.raises(ValueError, match="Alternativas Inválidas."):
        MultipleChoiceQuestion(1, "Q", 1, "T", ["a"], 0) 

    with pytest.raises(ValueError, match="Alternativas Inválidas."):
        MultipleChoiceQuestion(1, "Q", 1, "T", ["a", "b", "c", "d", "e", "f"], 0)

def test_multiple_choice_question_correct_answer_validation():
    with pytest.raises(ValueError, match="Resposta Correta Inválida."):
        MultipleChoiceQuestion(1, "Q", 1, "T", ["a", "b", "c"], 3) 

    with pytest.raises(ValueError, match="Resposta Correta Inválida."):
        MultipleChoiceQuestion(1, "Q", 1, "T", ["a", "b", "c"], -1) 

def test_quiz_special_methods(sample_quiz, sample_questions):
    assert len(sample_quiz) == 2
    assert str(sample_quiz) == "Quiz Geral"
    
    iterated_questions = [q for q in sample_quiz]
    assert iterated_questions == sample_questions

# Teste 6: Validação do título do Quiz
def test_quiz_title_validation(sample_quiz):
    with pytest.raises(ValueError, match="Título Inválido."):
        sample_quiz.title = ""

    with pytest.raises(ValueError, match="Título Inválido."):
        sample_quiz.title = "   "

def test_quiz_attempt_limit_validation(sample_quiz):
    with pytest.raises(ValueError, match="Limite de tentativas inválido."):
        sample_quiz.attempt_limit = 0

    with pytest.raises(ValueError, match="Limite de tentativas inválido."):
        sample_quiz.attempt_limit = -1

def test_quiz_time_limit_validation(sample_quiz):
    with pytest.raises(ValueError, match="Limite de tempo inválido."):
        sample_quiz.time_limit = 0

def test_user_creation():
    user = User(name="Nome Válido", email="email@valido.com")
    assert user.name == "Nome Válido"
    assert user.email == "email@valido.com"

def test_attempt_creation():
    attempt = Attempt(id_attempt=1, id_quiz=1, id_user=1, score=10, time=120.5, answers=[1, 2], attempt_number=1)
    assert attempt.score == 10
    assert attempt.time == 120.5

def test_attempt_invalid_score():
    attempt = Attempt(1, 1, 1, 10, 120.5, [], 1)
    with pytest.raises(ValueError, match="Score Inválido."):
        attempt.score = -5

def test_attempt_invalid_time():
    attempt = Attempt(1, 1, 1, 10, 120.5, [], 1)
    with pytest.raises(ValueError, match="Tempo Inválido."):
        attempt.time = -100.0