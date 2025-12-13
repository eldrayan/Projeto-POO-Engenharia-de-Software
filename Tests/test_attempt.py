import pytest
from quiz.models.attempt import Attempt

class Test_Attempt:
    @pytest.fixture
    def attempt(self):
        """Retorna um objeto Attempt de exemplo."""
        return Attempt(
            id_attempt=1,
            id_quiz=1,
            id_user=1,
            score=10,
            time=120.5,
            answers=[1, 2],
            attempt_number=1
        )

    def test_set_valid_score(self, attempt):
        """Testa a definição de um score válido."""
        attempt.score = 20
        assert attempt.score == 20

    def test_set_invalid_score_raises_error(self, attempt):
        """Testa se a definição de um score negativo levanta um ValueError."""
        with pytest.raises(ValueError, match="Score Inválido."):
            attempt.score = -5

    def test_set_valid_time(self, attempt):
        """Testa a definição de um tempo válido."""
        attempt.time = 99.9
        assert attempt.time == 99.9

    def test_set_invalid_time_raises_error(self, attempt):
        """Testa se a definição de um tempo negativo levanta um ValueError."""
        with pytest.raises(ValueError, match="Tempo Inválido."):
            attempt.time = -100.0

    def test_set_valid_answers(self, attempt):
        """Testa a definição de uma lista de respostas válida."""
        new_answers = [0, 1, 2]
        attempt.answers = new_answers
        assert attempt.answers == new_answers

    def test_set_invalid_answers_raises_error(self, attempt):
        """Testa se a definição de um valor que não é lista para respostas levanta um ValueError."""
        with pytest.raises(ValueError, match="Respostas Inválidas."):
            attempt.answers = "not a list"

    def test_set_valid_attempt_number(self, attempt):
        """Testa a definição de um número de tentativa válido."""
        attempt.attempt_number = 2
        assert attempt.attempt_number == 2

    def test_set_invalid_attempt_number_raises_error(self, attempt):
        """Testa se a definição de um número de tentativa inválido (<=0) levanta um ValueError."""
        with pytest.raises(ValueError, match="Número de Tentativa Inválido."):
            attempt.attempt_number = 0