class User:
    """
    Representa o perfil do usuário único do sistema, agregando suas estatísticas.

    Atributos:
        id_user (int): O identificador único do usuário.
        attempt_counter (int): O número total de tentativas de quiz.
    """
    def __init__(self, id_user: int = 1, attempt_counter: int = 0) -> None:
        """Inicializa um objeto User."""
        self.__id_user = id_user
        self.__attempt_counter = attempt_counter

    @property
    def id_user(self):
        """O ID fixo do usuário único."""
        return self.__id_user

    @property
    def attempt_counter(self):
        """Retorna o número de tentativas realizadas."""
        return self.__attempt_counter

    def increment_attempts(self):
        """Incrementa o contador de tentativas."""
        self.__attempt_counter += 1
