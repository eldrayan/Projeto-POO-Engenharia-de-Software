class Question:
    """
    Classe base para todas as questões do sistema.
    Contém atributos e métodos para todos os tipos de questão (mas será usado Múltipla Escolha no projeto).

    Atributos:
        id_question (int): O identificador único da questão.
        statement (str): O enunciado da questão.
        difficulty (str): O nível de dificuldade ('Easy', 'Medium', 'Hard').
        theme (str): O tema ou tópico da questão.
    """
    def __init__(self, id_question: int, statement: str, difficulty: int, theme: str) -> None:
        """Inicializa uma nova Questão (classe-base)."""
        self.__id_question = id_question
        self.__statement = statement
        self.__difficulty = difficulty
        self.__theme = theme

    @property
    def id_question(self):
        return self.__id_question
    
    @property
    def statement(self):
        return self.__statement
    
    @statement.setter
    def statement(self, new_statement):
        if not isinstance(new_statement, str) or not new_statement.strip():
            raise ValueError("Enunciado Inválido")
        if hasattr(self, '_Question__statement') and new_statement == self.__statement:
            raise ValueError("O Enunciado não pode ser o mesmo que o anterior.")
        self.__statement = new_statement

    @property
    def difficulty(self):
        return self.__difficulty
    
    @difficulty.setter
    def difficulty(self, new_difficulty):
        if new_difficulty not in [1, 2, 3]:
            raise ValueError("Dificuldade Inválida")
        self.__difficulty = new_difficulty

    @property
    def theme(self):
        return self.__theme
    
    @theme.setter
    def theme(self, new_theme):
        if not isinstance(new_theme, str) or not new_theme.strip():
            raise ValueError("Tema Inválido")
        if hasattr(self, '_Question__theme') and new_theme == self.__theme:
            raise ValueError("O Tema não pode ser o mesmo que o anterior.")
        self.__theme = new_theme

    def __str__(self) -> str:
        """Retorna o enunciado da questão como sua representação em string."""
        return f"{self.__statement} (Dificuldade: {self.__difficulty}, Tema: {self.__theme})"

    def __eq__(self, other) -> bool:
        """Compara se duas questões são iguais."""
        if not isinstance(other, Question):
            return False
        return self.statement.lower() == other.statement.lower() and \
               self.theme.lower() == other.theme.lower()