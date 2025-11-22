from typing import Any, List
from attempt import Attempt


class User:
    """
    Um usuário do sistema de quiz.

    Atributos:
        id_user (int): O identificador único do usuário.
        email (str): O email do usuário para logar.
        name (str): O nome de exibição do usuário.
    """
    def __init__(self, id_user: int, email: str, name: str, attempt_counter: int = 0) -> None:
        """Inicializa um objeto User."""
        self.id_user = id_user
        self.email = email
        self.name = name
        self.__attempt_counter = attempt_counter

    @property
    def id_user(self):
        return self.__id_user

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, new_email):
        if not isinstance(new_email, str) or len(new_email) <= 10 or "@" not in new_email:
            print("Email Inválido")
        elif(new_email == self.__email):
            print("O Email não pode ser o mesmo que o anterior.")
        else: 
            self.__email = new_email
            
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str) or len(new_name.strip()) == 0:
            print("Nome Inválido")
        elif(new_name == self.__name):
            print("O nome não pode ser o mesmo que o anterior.")
        else: 
            self.__name = new_name


        

    def answer_quiz(self, quiz: Any, user_answers: List[int]) -> Attempt:
        """
        Registra as respostas do usuário em um quiz.

        Args:
            quiz: o objeto quiz que vai ser respondido
            user_answers: lista com indices das alternativas escolhidas

        Returns:
            Attempt: Objeto contendo registro da tentativa
        """
        if not isinstance(user_answers, list) or len(user_answers) != len(quiz.questions):
            print("Respostas inválidas ou incompletas")
            return None
        
        score = 0
        for i, question in enumerate(quiz.questions):
            if user_answers[i] == question.correct_answer:
                score += 1

        self.__attempt_counter += 1

        attempt = Attempt(
            id_attempt=self.__attempt_counter,
            id_quiz = quiz.id_quiz,
            id_user = self.__id_user,
            score = score,
            time = 0.0,  
            answers = user_answers,
            attempt_number = self.__attempt_counter
        )
        return attempt

