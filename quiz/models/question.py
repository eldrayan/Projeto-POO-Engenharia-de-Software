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
        if len(new_statement) > 0:
            self.__statement = new_statement
        elif (new_statement == self.__statement):
            print("O Enunciado não pode ser o mesmo que o anterior.")
        else: 
            print("Enunciado Inválido")

    @property
    def difficulty(self):
        return self.__difficulty
    
    @difficulty.setter
    def difficulty(self, new_difficulty):
        if (new_difficulty == 1):
            self.__difficulty = 1
        elif (new_difficulty == 2):
            self.__difficulty = 2
        elif (new_difficulty == 3):
            self.__difficulty = 3
        else: 
            print("Dificuldade Inválida")

    @property
    def theme(self):
        return self.__theme
    
    @theme.setter
    def theme(self, new_theme):
        if len(new_theme) > 0:
            self.__theme = new_theme
        elif (new_theme == self.__theme):
            print("O Tema não pode ser o mesmo que o anterior.")
        else: 
            print("Tema Inválido")

    def __str__(self) -> str:
        """Retorna o enunciado da questão como sua representação em string."""
        return f"{self.__statement} (Dificuldade: {self.__difficulty}, Tema: {self.__theme})"

    def __eq__(self, other) -> bool:
        """Compara se duas questões são iguais."""
        if not isinstance(other, Question):
            return False
        return True