import json
import collections
import sqlite3

class Statistics:
    """
    Classe de serviço responsável por calcular e gerar todos os relatórios e estatísticas do sistema.
    Não armazena dados, apenas processa os dados recebidos.
    """
    def __init__(self) -> None:
        """Inicializa a calculadora de estatísticas."""
        pass

    def __str__(self) -> str:
        """Retorna uma descrição da classe."""
        return "Gerador de Estatísticas e Relatórios do Sistema"

    def generate_user_performance_report(self, user_attempts: list, data_layer) -> dict:
        """
        Gera um relatório de desempenho detalhado para um usuário específico.

        Args:
            user_attempts (list): Lista de tentativas do usuário (dicionários do DB).
            data_layer: A instância do objeto de dados para buscar mais informações.

        Returns:
            dict: Dicionário com as estatísticas calculadas para o usuário.
        """
        if not user_attempts:
            return {
                "total_attempts": 0,
                "average_score_percent": 0.0,
                "performance_by_theme": {}
            }

        total_score_achieved = 0
        total_max_possible_score = 0
        
        theme_performance = collections.defaultdict(lambda: {"correct": 0, "total": 0})

        for attempt in user_attempts:
            total_score_achieved += attempt['score']
            total_max_possible_score += attempt.get('max_possible_score') or 0
            
            quiz = data_layer.get_quiz_by_id(attempt['id_quiz'])
            if not quiz:
                continue

            user_answers = json.loads(attempt['answers'])
            for i, question in enumerate(quiz.questions):
                theme = question.theme
                theme_performance[theme]["total"] += 1
                if i < len(user_answers) and user_answers[i] == question.correct_answer:
                    theme_performance[theme]["correct"] += 1

        avg_score_percent = (total_score_achieved / total_max_possible_score * 100) if total_max_possible_score > 0 else 0
        
        final_theme_report = {
            theme: {
                "average_score": (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0,
                "correct_answers": stats["correct"],
                "total_questions": stats["total"]
            } for theme, stats in theme_performance.items()
        }

        return {
            "total_attempts": len(user_attempts),
            "average_score_percent": avg_score_percent,
            "performance_by_theme": final_theme_report
        }

    @staticmethod
    def generate_ranking_report(all_attempts: list) -> list:
        """Gera o ranking de usuários com base na pontuação média."""
        user_scores = collections.defaultdict(lambda: {"name": "", "total_score": 0, "total_max": 0})

        for attempt in all_attempts:
            user_id = attempt['id_user']
            user_scores[user_id]['name'] = attempt['user_name']
            user_scores[user_id]['total_score'] += attempt['score']
            user_scores[user_id]['total_max'] += attempt.get('max_possible_score') or 0
        
        ranking = []
        for user_id, scores in user_scores.items():
            avg_percent = (scores['total_score'] / scores['total_max'] * 100) if scores['total_max'] > 0 else 0
            ranking.append({
                "user_id": user_id,
                "user_name": scores['name'],
                "average_score_percent": avg_percent
            })
        
        return sorted(ranking, key=lambda x: x['average_score_percent'], reverse=True)

    @staticmethod
    def most_missed_questions(data_layer) -> list:
        """
        Retorna as questões mais erradas em todo o sistema.
        
        Args:
            data_layer: A instância do objeto de dados para buscar mais informações.
            
        Returns:
            list: Questões ordenadas por número de erros
        """
        miss_counts = collections.defaultdict(int)
        
        all_quizzes = data_layer.get_all_quizzes()
        quizzes_with_questions = {}
        for quiz_info in all_quizzes:
            quiz = data_layer.get_quiz_by_id(quiz_info['id_quiz'])
            if quiz:
                quizzes_with_questions[quiz.id_quiz] = quiz.questions

        conn = data_layer._get_connection()
        try:
            conn.row_factory = sqlite3.Row
            all_attempts = conn.execute("SELECT id_quiz, answers FROM attempts").fetchall()
        finally:
            conn.close()

        for attempt in all_attempts:
            quiz_id = attempt['id_quiz']
            questions = quizzes_with_questions.get(quiz_id)
            if not questions:
                continue
            
            user_answers = json.loads(attempt['answers'])
            for i, question in enumerate(questions):
                if i < len(user_answers) and user_answers[i] != question.correct_answer:
                    miss_counts[question.id_question] += 1
        
        if not miss_counts:
            return []

        conn = data_layer._get_connection()
        try:
            conn.row_factory = sqlite3.Row
            placeholders = ','.join('?' for _ in miss_counts)
            query = f"SELECT id_question, statement FROM questions WHERE id_question IN ({placeholders})"
            question_rows = conn.execute(query, list(miss_counts.keys())).fetchall()
            question_statements = {row['id_question']: row['statement'] for row in question_rows}
        finally:
            conn.close()

        missed_questions_report = [
            {
                "id_question": q_id,
                "statement": question_statements.get(q_id, "Enunciado não encontrado"),
                "miss_count": count
            } for q_id, count in miss_counts.items()
        ]

        return sorted(missed_questions_report, key=lambda x: x['miss_count'], reverse=True)

    @staticmethod
    def user_evolution_report(user_attempts: list) -> list:
        """
        Gera um relatório da evolução do desempenho de um usuário ao longo do tempo.

        Args:
            user_attempts (list): Lista de tentativas do usuário, contendo 'timestamp',
                                  'score' e 'max_possible_score'.

        Returns:
            list: Uma lista de tuplas (timestamp, performance_percent) ordenada por data.
        """
        evolution = []
        for attempt in user_attempts:
            max_score = attempt.get('max_possible_score') or 0
            performance = (attempt['score'] / max_score * 100) if max_score > 0 else 0
            evolution.append((attempt['timestamp'], performance))
        
        return sorted(evolution, key=lambda x: x[0])