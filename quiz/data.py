import sqlite3
import json
from .config import settings
from .models.quiz import Quiz
from .models.multiplechoicequestion import MultipleChoiceQuestion
from .models.attempt import Attempt

class Database:
    """
    Gerencia todas as interações com o banco de dados SQLite.
    """
    def __init__(self, db_file: str):
        """
        Inicializa a classe, definindo o caminho para o arquivo do banco de dados.
        """
        self.db_file = db_file

    def _get_connection(self):
        """Cria e retorna uma nova conexão com o banco de dados."""
        return sqlite3.connect(self.db_file)

    def create_tables(self):
        """
        Cria todas as tabelas necessárias no banco de dados, se ainda não existirem.
        """
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS quizzes (
                        id_quiz INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        attempt_limit INTEGER NOT NULL,
                        time_limit INTEGER NOT NULL
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS questions (
                        id_question INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_quiz INTEGER NOT NULL,
                        statement TEXT NOT NULL,
                        difficulty INTEGER NOT NULL,
                        theme TEXT NOT NULL,
                        alternatives TEXT NOT NULL, -- Armazenado como JSON
                        correct_answer INTEGER NOT NULL,
                        FOREIGN KEY (id_quiz) REFERENCES quizzes (id_quiz) ON DELETE CASCADE
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS attempts (
                        id_attempt INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_quiz INTEGER NOT NULL,
                        score INTEGER NOT NULL,
                        time REAL NOT NULL,
                        answers TEXT NOT NULL, -- Armazenado como JSON
                        attempt_number INTEGER NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (id_quiz) REFERENCES quizzes (id_quiz) ON DELETE CASCADE
                    )
                """)
        finally:
            conn.close()

    def add_quiz(self, quiz: Quiz):
        """
        Adiciona um novo quiz e todas as suas questões ao banco de dados.

        Args:
            quiz (Quiz): O objeto Quiz a ser salvo.
        """
        conn = self._get_connection()
        try:
            with conn:
                cursor = conn.execute(
                    "INSERT INTO quizzes (title, attempt_limit, time_limit) VALUES (?, ?, ?)",
                    (quiz.title, quiz.attempt_limit, quiz.time_limit)
                )
                id_quiz = cursor.lastrowid 

                questions_data = []
                for question in quiz.questions:
                    alternatives_json = json.dumps(question.alternatives)
                    questions_data.append((
                        id_quiz, question.statement, question.difficulty,
                        question.theme, alternatives_json, question.correct_answer
                    ))

                conn.executemany(
                    "INSERT INTO questions (id_quiz, statement, difficulty, theme, alternatives, correct_answer) VALUES (?, ?, ?, ?, ?, ?)",
                    questions_data
                )
        finally:
            conn.close()

    def get_all_quizzes(self) -> list:
        """
        Busca todos os quizzes disponíveis (ID e título) no banco de dados.

        Returns:
            list: Uma lista de dicionários, cada um representando um quiz.
        """
        conn = self._get_connection()
        try:
            conn.row_factory = sqlite3.Row  
            cursor = conn.execute("SELECT id_quiz, title FROM quizzes ORDER BY id_quiz")
            quizzes = cursor.fetchall()
            return [dict(row) for row in quizzes]
        finally:
            conn.close()

    def get_quiz_by_id(self, quiz_id: int) -> Quiz | None:
        """
        Busca um quiz completo pelo seu ID, incluindo todas as suas questões.

        Args:
            quiz_id (int): O ID do quiz a ser buscado.

        Returns:
            Quiz | None: O objeto Quiz montado ou None se não for encontrado.
        """
        conn = self._get_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM quizzes WHERE id_quiz = ?", (quiz_id,))
            quiz_row = cursor.fetchone()
            if not quiz_row:
                return None

            cursor = conn.execute("SELECT * FROM questions WHERE id_quiz = ? ORDER BY id_question", (quiz_id,))
            question_rows = cursor.fetchall()

            questions = [
                MultipleChoiceQuestion(
                    id_question=q_row['id_question'],
                    statement=q_row['statement'],
                    difficulty=q_row['difficulty'],
                    theme=q_row['theme'],
                    alternatives=json.loads(q_row['alternatives']),
                    correct_answer=q_row['correct_answer']
                ) for q_row in question_rows
            ]

            return Quiz(
                id_quiz=quiz_row['id_quiz'],
                title=quiz_row['title'],
                questions=questions,
                attempt_limit=quiz_row['attempt_limit'],
                time_limit=quiz_row['time_limit']
            )
        finally:
            conn.close()

    def get_attempt_count_for_quiz(self, quiz_id: int) -> int:
        """Conta quantas tentativas já foram feitas para um quiz específico."""
        conn = self._get_connection()
        try:
            cursor = conn.execute("SELECT COUNT(id_attempt) FROM attempts WHERE id_quiz = ?", (quiz_id,))
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def add_attempt(self, attempt: Attempt):
        """Adiciona um novo registro de tentativa ao banco de dados."""
        conn = self._get_connection()
        try:
            with conn:
                answers_json = json.dumps(attempt.answers)
                conn.execute(
                    "INSERT INTO attempts (id_quiz, score, time, answers, attempt_number) VALUES (?, ?, ?, ?, ?)",
                    (attempt.id_quiz, attempt.score, attempt.time, answers_json, attempt.attempt_number)
                )
        finally:
            conn.close()

    def get_all_attempts_for_report(self) -> list:
        """
        Busca dados agregados de todas as tentativas para gerar relatórios.

        Returns:
            list: Uma lista de dicionários com dados de cada tentativa.
        """
        conn = self._get_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT
                    a.id_quiz,
                    q.title as quiz_title,
                    a.score,
                    (SELECT COUNT(id_question) FROM questions WHERE id_quiz = a.id_quiz) as total_questions
                FROM attempts a
                JOIN quizzes q ON a.id_quiz = q.id_quiz
            """)
            attempts_data = cursor.fetchall()
            return [dict(row) for row in attempts_data]
        finally:
            conn.close()

data = Database(settings.get('database_file'))