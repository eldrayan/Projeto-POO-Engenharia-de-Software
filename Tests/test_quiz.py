import pytest
from quiz.models.quiz import Quiz
from quiz.models.multiplechoicequestion import MultipleChoiceQuestion

class Test_Quiz:
    @pytest.fixture
    def quiz(self):
        """Returns a sample Quiz object."""
        q1 = MultipleChoiceQuestion(1, "Q1", 1, "T1", ["a", "b", "c"], 0)
        return Quiz(
            id_quiz=1,
            title="Sample Quiz",
            questions=[q1],
            attempt_limit=3,
            time_limit=10
        )

    def test_set_valid_title(self, quiz):
        """Tests setting a valid title."""
        quiz.title = "New Title"
        assert quiz.title == "New Title"

    def test_set_invalid_title_raises_error(self, quiz):
        """Tests that setting an empty title raises ValueError."""
        with pytest.raises(ValueError, match="Título Inválido."):
            quiz.title = "   "

    def test_set_valid_attempt_limit(self, quiz):
        """Tests setting a valid attempt limit."""
        quiz.attempt_limit = 5
        assert quiz.attempt_limit == 5

    def test_set_invalid_attempt_limit_raises_error(self, quiz):
        """Tests that setting an invalid attempt limit (<=0) raises ValueError."""
        with pytest.raises(ValueError, match="Limite de tentativas inválido."):
            quiz.attempt_limit = 0

    def test_set_valid_time_limit(self, quiz):
        """Tests setting a valid time limit."""
        quiz.time_limit = 20
        assert quiz.time_limit == 20

    def test_set_invalid_time_limit_raises_error(self, quiz):
        """Tests that setting an invalid time limit (<=0) raises ValueError."""
        with pytest.raises(ValueError, match="Limite de tempo inválido."):
            quiz.time_limit = -5