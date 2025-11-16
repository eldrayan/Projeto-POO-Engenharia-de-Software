class User:
    """
    Um usuário do sistema de quiz.

    Atributos:
        id_user (int): O identificador único do usuário.
        email (str): O email do usuário para logar.
        name (str): O nome de exibição do usuário.
    """
    def __init__(self, id_user, email, name):
        """Inicializa um objeto User."""
        self.id_user = id_user
        self.email = email
        self.name = name

    def answer_quiz(self, quiz):
        """
        Método vazio para a ação de um usuário responder a um quiz.
        A lógica será implementada nas próximas semanas.
        """
        pass

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
    def __init__(self, id_question, statement, difficulty, theme):
        """Inicializa uma nova Questão (classe-base)."""
        self.id_question = id_question
        self.statement = statement
        self.difficulty = difficulty
        self.theme = theme

    def __str__(self):
        """Retorna o enunciado da questão como sua representação em string."""
        pass

    def __eq__(self, other):
        """Compara se duas questões são iguais."""
        pass

class MultipleChoiceQuestion(Question):
    """
    Uma questão de múltipla escolha.
    Herda da classe-base 'Question' e adiciona atributos específicos a múltipla escohla.

    Atributos:
        (Herda id_question, statement, difficulty e theme)
        alternatives (list[str]): Uma lista de strings com as alternativas.
        correct_answer (int): O índice da alternativa correta na lista.
    """
    def __init__(self, id_question, statement, difficulty, theme, alternatives, correct_answer):
        """
        Inicializa a questão de múltipla escolha.
        Chama a classe mãe super() para os atributos herdados.
        """
        super().__init__(id_question, statement, difficulty, theme)
        
        self.alternatives = alternatives
        self.correct_answer = correct_answer
        
    def __str__(self):
        """
        Sobrescreve (overwrite) o método __str__ da classe mãe para incluir as alternativas na representação em string.
        """
        pass

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
    def __init__(self, id_quiz, title, questions, attempt_limit, time_limit):
        """Inicializa um novo Quiz."""
        self.id_quiz = id_quiz
        self.title = title
        self.questions = questions
        self.attempt_limit = attempt_limit
        self.time_limit = time_limit
        
    def __str__(self):
        """Retorna o título do quiz."""
        pass
    
    def __len__(self):
        """Retorna o número de questões que o quiz posssui."""
        pass

    def __iter__(self):
        """Permite iterar sobre a lista de questões."""
        pass

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
    def __init__(self, id_attempt, id_quiz, id_user, score, time, answers, attempt_number):
        """Inicializa um novo registro de tentativa."""
        self.id_attempt = id_attempt
        self.id_quiz = id_quiz
        self.id_user = id_user
        self.score = score
        self.time = time
        self.answers = answers
        self.attempt_number = attempt_number
        
    def __str__(self):
        """Retorna um resumo da tentativa."""
        pass

class Statistics:
    """
    Classe de serviço responsável por calcular e gerar todos os relatórios e estatísticas do sistema.
    Não armazena dados, apenas processa os dados recebidos.
    """
    def __init__(self):
        """Inicializa a calculadora de estatísticas."""
        pass

    def __str__(self):
        """Retorna uma descrição da classe."""
        pass

    def generate_rankings(self):
        """Gera o ranking de usuários com base na pontuação média."""
        pass

    def show_user_performance(self):
        """Mostra o desempenho de um usuário específico."""
        pass

    def most_missed_questions(self):
        """Retorna as questões mais erradas em todo o sistema."""
        pass

    def user_evolution(self):
        """Mostra a evolução de desempenho de um usuário ao longo do tempo."""
        pass

class Settings:
    """
    Carrega e armazena as configurações globais do sistema, lidas a partir de um arquivo externo.

    Atributos:
        (id_config): O identificador único das configurações.
        standard_duration (int): Duração padrão de quiz em minutos.
        attempt_limit (int): Limite padrão de tentativas por usuário.
        difficulty_weights (dict): Pesos para cálculo de pontuação.
    """
    def __init__(self, id_config, standard_duration, attempt_limit, difficulty_weights):
        """Inicializa o objeto de configurações."""
        self.id_config = id_config
        self.standard_duration = standard_duration
        self.attempt_limit = attempt_limit
        self.difficulty_weights = difficulty_weights
        
    def __str__(self):
        """Retorna um resumo das configurações atuais."""
        pass