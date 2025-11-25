from typing import Dict

class Settings:
    """
    Carrega e armazena as configurações globais do sistema, lidas a partir de um arquivo externo.

    Atributos:
        standard_duration (int): Duração padrão de quiz em minutos.
        attempt_limit (int): Limite padrão de tentativas por usuário.
        difficulty_weights (dict): Pesos para cálculo de pontuação.
    """
    def __init__(self, standard_duration: int, attempt_limit: int, difficulty_weights: Dict[int, int]) -> None:
        """Inicializa o objeto de configurações."""
        self.__standard_duration = standard_duration
        self.__attempt_limit = attempt_limit
        self.__difficulty_weights = difficulty_weights

    @property
    def standard_duration(self):
        return self.__standard_duration
    
    @standard_duration.setter
    def standard_duration(self, new_standard_duration):
        if not isinstance(new_standard_duration, int) or new_standard_duration <= 0:
            raise ValueError("Duração Padrão Inválida.")
        else:
            self.__standard_duration = new_standard_duration
    
    @property
    def attempt_limit(self):
        return self.__attempt_limit
    
    @attempt_limit.setter
    def attempt_limit(self, new_attempt_limit):
        if not isinstance(new_attempt_limit, int) or new_attempt_limit <= 0:
            raise ValueError("Limite de Tentativas Inválido.")
        else:
            self.__attempt_limit = new_attempt_limit
    
    @property
    def difficulty_weights(self):
        return self.__difficulty_weights
    
    @difficulty_weights.setter
    def difficulty_weights(self, new_difficulty_weights):
        if not isinstance(new_difficulty_weights, dict) or len(new_difficulty_weights) == 0:
            raise ValueError("Pesos de Dificuldade Inválidos.")
        else:
            self.__difficulty_weights = new_difficulty_weights
        
    def __str__(self) -> str:
        """Retorna um resumo das configurações atuais."""
        return f"Duração Padrão: {self.__standard_duration}min | Limite de Tentativas: {self.__attempt_limit} | Pesos: {self.__difficulty_weights}"