import pytest
from quiz.models.question import Question

class Test_Question:
    @pytest.fixture
    def question(self):
        """Retorna um objeto Question de exemplo para testes."""
        return Question(id_question=1, statement="Statement", difficulty=1, theme="Theme")

    def test_set_valid_statement(self, question):
        """Testa a definição de um enunciado válido."""
        question.statement = "New Statement"
        assert question.statement == "New Statement"

    def test_set_invalid_statement_raises_error(self, question):
        """Testa se a definição de um enunciado inválido (vazio) levanta um ValueError."""
        with pytest.raises(ValueError, match="Enunciado Inválido"):
            question.statement = "   "

    def test_set_same_statement_raises_error(self, question):
        """Testa se a definição do mesmo enunciado levanta um ValueError."""
        with pytest.raises(ValueError, match="O Enunciado não pode ser o mesmo que o anterior."):
            question.statement = "Statement"

    def test_set_valid_difficulty(self, question):
        """Testa a definição de uma dificuldade válida."""
        question.difficulty = 3
        assert question.difficulty == 3

    def test_set_invalid_difficulty_raises_error(self, question):
        """Testa se a definição de uma dificuldade inválida levanta um ValueError."""
        with pytest.raises(ValueError, match="Dificuldade Inválida"):
            question.difficulty = 4

    def test_set_valid_theme(self, question):
        """Testa a definição de um tema válido."""
        question.theme = "New Theme"
        assert question.theme == "New Theme"

    def test_set_invalid_theme_raises_error(self, question):
        """Testa se a definição de um tema inválido (vazio) levanta um ValueError."""
        with pytest.raises(ValueError, match="Tema Inválido"):
            question.theme = ""