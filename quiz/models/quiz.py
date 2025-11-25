from typing import List, Any
from .multiplechoicequestion import MultipleChoiceQuestion

class Quiz:
    """
    Um quiz, que é uma conjunto de questões e regras.

    Atributos:
        id_quiz (int): O identificador único do quiz.
        title (str): O título do quiz.
        questions (list[Question]): Uma lista de objetos Question.
        attempt_limit (int): O número máximo de tentativas.
        time_limit (int): O tempo limite em minutos para responder o quiz.
    """
    def __init__(self, id_quiz: int, title: str, questions: List[MultipleChoiceQuestion], attempt_limit: int, time_limit: int) -> None:
        """Inicializa um novo Quiz."""
        self.__id_quiz = id_quiz
        self.__title = title
        self.__questions = questions
        self.__attempt_limit = attempt_limit
        self.__time_limit = time_limit

    @property
    def id_quiz(self):
        return self.__id_quiz
    
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, new_title):
        if not isinstance(new_title, str) or len(new_title.strip()) == 0:
            raise ValueError("Título Inválido.")
        else:
            self.__title = new_title
    
    @property
    def questions(self):
        return self.__questions
    
    @questions.setter
    def questions(self, new_questions):
        if not isinstance(new_questions, list) or len(new_questions) == 0:
            raise ValueError("Lista de questões inválida.")
        else:
            self.__questions = new_questions
    
    @property
    def attempt_limit(self):
        return self.__attempt_limit
    
    @attempt_limit.setter
    def attempt_limit(self, new_attempt_limit):
        if not isinstance(new_attempt_limit, int) or new_attempt_limit <= 0:
            raise ValueError("Limite de tentativas inválido.")
        else:
            self.__attempt_limit = new_attempt_limit
    
    @property
    def time_limit(self):
        return self.__time_limit
    
    @time_limit.setter
    def time_limit(self, new_time_limit):
        if not isinstance(new_time_limit, int) or new_time_limit <= 0:
            raise ValueError("Limite de tempo inválido.")
        else:
            self.__time_limit = new_time_limit
        
    def __str__(self) -> str:
        """Retorna o título do quiz."""
        return self.__title
    
    def __len__(self) -> int:
        """Retorna o número de questões que o quiz possui."""
        return len(self.__questions)

    def __iter__(self) -> Any:
        """Permite iterar sobre a lista de questões."""
        return iter(self.__questions)