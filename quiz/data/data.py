import sqlite3
import json
from typing import List, Dict

from ..models.user import User
from ..models.quiz import Quiz
from ..models.multiplechoicequestion import MultipleChoiceQuestion
from ..models.attempt import Attempt

DB_FILE = "quiz_database.db"

def get_db_connection():
    """"Cria e retorna uma conexão com a base de dados."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """"Cria as tabelas da base de dados, se já não existir."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        "group" TEXT NOT NULL,
        attempt_counter INTEGER DEFAULT 0
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id_quiz INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        attempt_limit INTEGER,
        time_limit INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id_question INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        statement TEXT NOT NULL,
        difficulty INTEGER,
        theme TEXT,
        alternatives TEXT NOT NULL,
        correct_answer INTEGER NOT NULL,
        FOREIGN KEY (quiz_id) REFERENCES quizzes (id_quiz)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attempts (
        id_attempt INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        quiz_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        time REAL,
        answers TEXT,
        attempt_number INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id_user),
        FOREIGN KEY (quiz_id) REFERENCES quizzes (id_quiz)
    );
    """)


    conn.commit()
    conn.close()

def add_users(user: User) -> User:
    """Adiciona usuário a base de dados e retorna o objeto com o ID atualizado."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (email, name, \"group\") VALUES (?, ?, ?)",
        (user.email, user.name, user.group)
    )
    
    new_id = cursor.lastrowid
    user.id_user = new_id  
    
    conn.commit()
    conn.close()
    return user

def get_all_users() -> List[User]:
    """Faz busca de todos os usuários na DB."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = [User(id_user=row['id_user'], email=row['email'], name=row['name'], group=row['group']) for row in rows]
    return users

def get_users_by_turma() -> Dict[str, List[User]]:
    """Busca todos os usuários e os agrupa por turma."""
    all_users = get_all_users()
    report = {}
    for user in all_users:
        if user.group not in report:
            report[user.group] = []
        report[user.group].append(user)
    return report