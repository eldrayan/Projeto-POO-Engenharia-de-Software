from typing import List, Any

class Attempt:
    """
    Armazena o resultado de uma única tentativa de um usuário em um quiz.

    Atributos:
        id_attempt (int): O identificador único da tentativa.
        id_quiz (int): O ID do quiz que foi respondido.
        id_user (int): O ID do usuário que respondeu.
        score (int): A pontuação final.
        time (float): O tempo que o usuário levou.
        answers (list): Uma lista de respostas dadas pelo usuário.
        attempt_number (int): O número desta tentativa.
    """
    def __init__(self, id_attempt: int, id_quiz: int, id_user:int, score: int, time: float, answers: List[Any], attempt_number: int) -> None:
        """Inicializa um novo registro de tentativa."""
        self.__id_attempt = id_attempt
        self.__id_quiz = id_quiz
        self.__id_user = id_user
        self.__score = score
        self.__time = time
        self.__answers = answers
        self.__attempt_number = attempt_number
        
    @property
    def id_attempt(self):
        return self.__id_attempt
    
    @property
    def id_quiz(self):
        return self.__id_quiz
    
    @property
    def id_user(self):
        return self.__id_user

    @property
    def score(self):
        return self.__score
    
    @score.setter
    def score(self, new_score):
        if not isinstance(new_score, int) or new_score < 0:
            raise ValueError("Score Inválido.")
        else:
            self.__score = new_score

    @property
    def time(self):
        return self.__time
    
    @time.setter
    def time(self, new_time):
        if not isinstance(new_time, (int, float)) or new_time < 0:
            raise ValueError("Tempo Inválido.")
        else:
            self.__time = new_time

    @property
    def answers(self):
        return self.__answers
    
    @answers.setter
    def answers(self, new_answers):
        if not isinstance(new_answers, list):
            raise ValueError("Respostas Inválidas.")
        else:
            self.__answers = new_answers

    @property
    def attempt_number(self):
        return self.__attempt_number
    
    @attempt_number.setter
    def attempt_number(self, new_attempt_number):
        if not isinstance(new_attempt_number, int) or new_attempt_number <= 0:
            raise ValueError("Número de Tentativa Inválido.")
        else:
            self.__attempt_number = new_attempt_number

    def __str__(self) -> str:
        """Retorna um resumo da tentativa."""
        return f"Tentativa #{self.__attempt_number} - Quiz {self.__id_quiz} - Score: {self.__score} - Tempo: {self.__time}s"