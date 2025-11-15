class User:

    def __init__(self, id_user, email, name):
        self.id_user = id_user
        self.email = email
        self.name = name

    def answer_quiz(self, quiz):
        pass

class Question:

    def __init__(self, id_question, statement, difficulty, theme):
        self.id_question = id_question
        self.statement = statement
        self.difficulty = difficulty
        self.theme = theme

    def __str__(self):
        pass

    def __eq__(self, other):
        pass

class MultipleChoiceQuestion(Question):

    def __init__(self, id_question, statement, difficulty, theme, alternatives, correct_answer):
        super().__init__(id_question, statement, difficulty, theme)
        self.alternatives = alternatives
        self.correct_answer = correct_answer
        

    def __str__(self):
        pass

class Quiz:

    def __init__(self, id_quiz, title, questions, attempt_limit, time_limit):
        self.id_quiz = id_quiz
        self.title = title
        self.questions = questions
        self.attempt_limit = attempt_limit
        self.time_limit = time_limit
        
    def __str__(self):
        pass
    
    def __len__(self):
        pass

    def __iter__(self):
        pass

class Attempt:

    def __init__(self, id_attempt, id_quiz, id_user, score, time, answers, attempt_number):
        self.id_attempt = id_attempt
        self.id_quiz = id_quiz
        self.id_user = id_user
        self.score = score
        self.time = time
        self.answers = answers
        self.attempt_number = attempt_number
        
    def __str__(self):
        pass

class Statistics:
    
    def __init__(self):
        pass

    def __str__(self):
        pass

    def generate_rankings(self):
        pass

    def show_user_performance(self):
        pass

    def most_missed_questions(self):
        pass

    def user_evolution(self):
        pass

class Settings:

    def __init__(self, id_config, standard_duration, attempt_limit, difficulty_weights):
        self.id_config = id_config
        self.standard_duration = standard_duration
        self.attempt_limit = attempt_limit
        self.difficulty_weights = difficulty_weights
        
    def __str__(self):
        pass