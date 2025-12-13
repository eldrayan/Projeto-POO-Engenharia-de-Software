import pytest
from quiz.models.settings import Settings

class Test_Settings:
    @pytest.fixture
    def settings_obj(self):
        """Retorna um objeto Settings de exemplo."""
        return Settings(standard_duration=30, attempt_limit=3, difficulty_weights={"1": 1, "2": 2})

    def test_set_valid_standard_duration(self, settings_obj):
        """Testa a definição de uma duração padrão válida."""
        settings_obj.standard_duration = 60
        assert settings_obj.standard_duration == 60

    def test_set_invalid_standard_duration_raises_error(self, settings_obj):
        """Testa se a definição de uma duração inválida levanta um ValueError."""
        with pytest.raises(ValueError, match="Duração Padrão Inválida."):
            settings_obj.standard_duration = 0

    def test_set_valid_attempt_limit(self, settings_obj):
        """Testa a definição de um limite de tentativas válido."""
        settings_obj.attempt_limit = 5
        assert settings_obj.attempt_limit == 5

    def test_set_invalid_attempt_limit_raises_error(self, settings_obj):
        """Testa se a definição de um limite de tentativas inválido levanta um ValueError."""
        with pytest.raises(ValueError, match="Limite de Tentativas Inválido."):
            settings_obj.attempt_limit = -1

    def test_set_valid_difficulty_weights(self, settings_obj):
        """Testa a definição de pesos de dificuldade válidos."""
        new_weights = {"1": 1, "2": 2, "3": 3}
        settings_obj.difficulty_weights = new_weights
        assert settings_obj.difficulty_weights == new_weights

    def test_set_invalid_difficulty_weights_raises_error(self, settings_obj):
        """Testa se a definição de pesos de dificuldade inválidos levanta um ValueError."""
        with pytest.raises(ValueError, match="Pesos de Dificuldade Inválidos."):
            settings_obj.difficulty_weights = {}