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

    def generate_performance_report(self, attempts_data: list) -> dict:
        """
        Gera um relatório de performance com base em todas as tentativas.
        
        Args:
            attempts_data (list): Uma lista de dicionários vinda do banco de dados.
            
        Returns:
            dict: Um dicionário com as estatísticas calculadas.
        """
        if not attempts_data:
            return {
                "total_attempts": 0,
                "completed_quizzes": 0,
                "average_score_percent": 0.0
            }

        total_attempts = len(attempts_data)
        completed_quiz_ids = {row['id_quiz'] for row in attempts_data}
        
        total_score_percent = 0
        for row in attempts_data:
            if row['total_questions'] > 0:
                total_score_percent += (row['score'] / row['total_questions']) * 100
        
        average_score = total_score_percent / total_attempts if total_attempts > 0 else 0

        return {
            "total_attempts": total_attempts,
            "completed_quizzes": len(completed_quiz_ids),
            "average_score_percent": average_score
        }

    @staticmethod
    def most_missed_questions(attempts: list) -> list:
        """
        Retorna as questões mais erradas em todo o sistema.
        
        Args:
            attempts (list): Lista de tentativas
            
        Returns:
            list: Questões ordenadas por número de erros
        """
        pass

    def performance_evolution(self, attempts: list) -> list:
        """
        Mostra a evolução de desempenho ao longo do tempo.
        
        Args:
            attempts (list): Uma lista de objetos Attempt.
            
        Returns:
            list: Histórico de desempenho ordenado por data
        """
        pass