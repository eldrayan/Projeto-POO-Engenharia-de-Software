import pytest
from quiz.models.multiplechoicequestion import MultipleChoiceQuestion

class Test_MultipleChoiceQuestion:
    @pytest.fixture
    def mc_question(self):
        """Retorna um objeto MultipleChoiceQuestion de exemplo."""
        return MultipleChoiceQuestion(
            id_question=1,
            statement="Statement",
            difficulty=1,
            theme="Theme",
            alternatives=["A", "B", "C"],
            correct_answer=0
        )

    def test_set_valid_alternatives(self, mc_question):
        """Testa a definição de uma lista de alternativas válida."""
        new_alts = ["X", "Y", "Z", "W"]
        mc_question.alternatives = new_alts
        assert mc_question.alternatives == new_alts

    def test_set_invalid_alternatives_raises_error(self, mc_question):
        """Testa se a definição de um número inválido de alternativas levanta um ValueError."""
        with pytest.raises(ValueError, match="Alternativas Inválidas."):
            mc_question.alternatives = ["Too", "few"]
        
        with pytest.raises(ValueError, match="Alternativas Inválidas."):
            mc_question.alternatives = ["Too", "many", "options", "for", "one", "question"]

    def test_set_valid_correct_answer(self, mc_question):
        """Testa a definição de um índice de resposta correta válido."""
        mc_question.correct_answer = 2
        assert mc_question.correct_answer == 2

    def test_set_invalid_correct_answer_raises_error(self, mc_question):
        """Testa se a definição de um índice de resposta correta fora dos limites levanta um ValueError."""
        with pytest.raises(ValueError, match="Resposta Correta Inválida."):
            mc_question.correct_answer = 3
        
        with pytest.raises(ValueError, match="Resposta Correta Inválida."):
            mc_question.correct_answer = -1