import time
import click
from .data import data
from .config import settings
from .models.quiz import Quiz
from .models.user import User
from .models.multiplechoicequestion import MultipleChoiceQuestion
from .models.attempt import Attempt
from .models.statistics import Statistics

@click.group()
def cli():
    """
    Inicia a Interface de Linha de Comando (CLI) para o sistema de Quiz.
    """
    click.echo("Bem-vindo ao Sistema de Quiz!")

@cli.command("register")
def register_user():
    """Cadastra um novo usuário."""
    click.echo("--- Cadastro de Novo Usuário ---")
    name = click.prompt("Nome")
    email = click.prompt("Email")
    
    new_user = User(id_user=None, name=name, email=email)
    
    try:
        user_id = data.add_user(new_user)
        click.secho(f"Usuário '{name}' cadastrado com sucesso! ID: {user_id}", fg="green")
    except Exception as e:
        click.secho(f"Erro ao cadastrar usuário: {e}", fg="red")

def get_user_from_prompt():
    """Exibe uma lista de usuários e solicita a seleção de um."""
    users = data.get_all_users()
    if not users:
        return None
    click.echo("Selecione o usuário:")
    for user in users:
        click.echo(f"  ID {user['id_user']}: {user['name']} ({user['email']})")
    user_id = click.prompt("Digite o ID do usuário", type=click.Choice([str(u['id_user']) for u in users]))
    return data.get_user_by_id(int(user_id))

@cli.command("create")
def create_quiz():
    """Cria um novo quiz."""
    click.echo("Prosseguindo para a criação do quiz...")
    
    title = click.prompt("Qual é o título do quiz?")
    time_limit = click.prompt("Qual o tempo limite em minutos?", type=int, default=30)
    default_attempts = settings.get('default_attempt_limit', 3)
    attempt_limit = click.prompt("Qual o limite de tentativas?", type=int, default=default_attempts)
    
    questions = []
    min_questions = settings.get('min_questions_per_quiz', 1)
    while True:
        if len(questions) >= min_questions:
            question_text = click.prompt("Insira o enunciado da questão (ou deixe em branco para finalizar)", default='', show_default=False)
        else:
            question_text = click.prompt(f"Insira o enunciado da questão ({min_questions - len(questions)} restante(s))")

        if not question_text:
            break
        
        theme = click.prompt("  Qual o tema da questão?")
        difficulty = click.prompt("  Qual a dificuldade (1-Fácil, 2-Médio, 3-Difícil)?", type=click.IntRange(1, 3))
        
        num_alternatives = click.prompt("  Quantas alternativas (3-5)?", type=click.IntRange(3, 5), default=4)
        answers = []
        for i in range(num_alternatives):
            answer_text = click.prompt(f"  Opção {i+1}")
            answers.append(answer_text)
        
        correct_option = click.prompt(f"  Qual é a opção correta (1-{num_alternatives})?", type=click.IntRange(1, num_alternatives))
        correct_answer_index = correct_option - 1
        
        new_question = MultipleChoiceQuestion(
            id_question=None,
            statement=question_text,
            difficulty=difficulty,
            theme=theme,
            alternatives=answers,
            correct_answer=correct_answer_index
        )
        questions.append(new_question)
        click.echo("Questão adicionada.")

    new_quiz = Quiz(
        id_quiz=None, 
        title=title,
        questions=questions,
        attempt_limit=attempt_limit,
        time_limit=time_limit
    )

    data.add_quiz(new_quiz)
    click.echo(f"\nQuiz '{title}' foi salvo com sucesso com {len(questions)} questões.")

@cli.command("list")
def list_quizzes():
    """Lista todos os quizzes disponíveis."""
    quizzes = data.get_all_quizzes()
    if not quizzes:
        click.echo("Nenhum quiz encontrado. Crie um primeiro usando 'python -m quiz create'.")
        return

    click.secho("\n--- Quizzes Disponíveis ---", bold=True)
    for quiz_info in quizzes:
        quiz_obj = data.get_quiz_by_id(quiz_info['id_quiz'])
        plural = "questão" if len(quiz_obj.questions) == 1 else "questões"
        click.echo(f"  ID {quiz_info['id_quiz']}: {quiz_info['title']} ({len(quiz_obj.questions)} {plural})")


@cli.command("take")
def run_quiz():
    """Responde a um quiz."""
    user = get_user_from_prompt()
    if not user:
        click.echo("Nenhum usuário encontrado. Cadastre um usuário com 'python -m quiz register'.")
        return
    click.secho(f"\nUsuário selecionado: {user.name}", fg="cyan")

    quizzes = data.get_all_quizzes()
    if not quizzes:
        click.echo("Nenhum quiz encontrado. Crie um primeiro usando 'python -m quiz create'.")
        return

    click.echo("Escolha um quiz para responder:")
    for quiz_info in quizzes:
        click.echo(f"  {quiz_info['id_quiz']}. {quiz_info['title']}")

    valid_quiz_ids = [q['id_quiz'] for q in quizzes]
    quiz_id_str = click.prompt(
        "\nDigite o ID do quiz que deseja responder",
        type=click.Choice([str(i) for i in valid_quiz_ids])
    )
    quiz_id = int(quiz_id_str)

    quiz = data.get_quiz_by_id(quiz_id)
    attempt_count = data.get_attempt_count_for_quiz(quiz.id_quiz, user.id_user)

    if attempt_count >= quiz.attempt_limit:
        click.echo(f"\nVocê já atingiu o limite de {quiz.attempt_limit} tentativas para este quiz.")
        return

    click.echo(f"\n--- Iniciando Quiz: {quiz.title} ---")
    click.echo(f"Você tem {quiz.time_limit} minutos. Esta é sua tentativa número {attempt_count + 1} de {quiz.attempt_limit}.")
    click.confirm("Pressione Enter para começar...", default=True, show_default=False, prompt_suffix='')

    user_answers = []
    score = 0
    start_time = time.time()

    for i, question in enumerate(quiz.questions):
        if (time.time() - start_time) / 60 > quiz.time_limit:
            click.secho("\nO tempo limite foi atingido! O quiz será encerrado.", fg="yellow")
            break
        click.clear()
        click.echo(f"--- {quiz.title} ---\n")
        click.echo(f"Questão {i + 1} de {len(quiz)}:")
        click.echo(str(question))  

        user_choice = click.prompt("\nSua resposta", type=click.IntRange(1, len(question.alternatives)))
        user_answer_index = user_choice - 1
        user_answers.append(user_answer_index)

        if user_answer_index == question.correct_answer:
            weights = settings.get('difficulty_weights', {"1": 1, "2": 1, "3": 1})
            score += weights.get(str(question.difficulty), 1)
            click.secho("✓ Correto!", fg="green")
        else:
            correct_text = question.alternatives[question.correct_answer]
            click.secho(f"✗ Incorreto. A resposta era: {correct_text}", fg="red")
        time.sleep(1.5)

    total_time = time.time() - start_time

    new_attempt = Attempt(
        id_attempt=None, id_quiz=quiz.id_quiz, id_user=user.id_user, score=score,
        time=total_time, answers=user_answers, attempt_number=attempt_count + 1
    )
    data.add_attempt(new_attempt)

    click.clear()
    click.secho("--- Resultado Final ---", bold=True)
    click.echo(f"Quiz: {quiz.title}")
    click.echo(f"Sua pontuação final foi: {score} pontos.")
    click.echo(f"Tempo total: {total_time:.2f} segundos.")

    click.secho("\n--- Gabarito ---", bold=True)
    for i, question in enumerate(quiz.questions):
        user_ans_idx = user_answers[i] if i < len(user_answers) else -1
        user_ans_text = question.alternatives[user_ans_idx] if user_ans_idx != -1 else "Não respondida"
        correct_ans_text = question.alternatives[question.correct_answer]
        
        is_correct = user_ans_idx == question.correct_answer
        click.echo(f"\nQ{i+1}: {question.statement}")
        click.echo(f"  Sua resposta: {user_ans_text}", fg="green" if is_correct else "red")
        if not is_correct:
            click.echo(f"  Resposta correta: {correct_ans_text}")

    click.secho("\nSua tentativa foi salva com sucesso.", fg="cyan")

@cli.command("delete")
def delete_quiz():
    """Deleta um quiz existente."""
    quizzes = data.get_all_quizzes()
    if not quizzes:
        click.echo("Nenhum quiz para deletar.")
        return

    click.echo("Escolha um quiz para deletar:")
    for quiz_info in quizzes:
        click.echo(f"  {quiz_info['id_quiz']}. {quiz_info['title']}")

    valid_quiz_ids = [q['id_quiz'] for q in quizzes]
    quiz_id_str = click.prompt(
        "\nDigite o ID do quiz que deseja deletar",
        type=click.Choice([str(i) for i in valid_quiz_ids])
    )
    quiz_id = int(quiz_id_str)

    if click.confirm(f"Você tem certeza que quer deletar o quiz{quiz_id}? Esta ação não pode ser desfeita."):
        data.delete_quiz_by_id(quiz_id)
        click.secho(f"Quiz ID {quiz_id} foi deletado com sucesso.", fg="green")

@cli.group()
def report():
    """Grupo de comandos para geração de relatórios."""
    pass

@report.command("performance")
def performance_report():
    """Gera um relatório de performance detalhado para um usuário."""
    user = get_user_from_prompt()
    if not user:
        click.echo("Nenhum usuário encontrado para gerar relatório.")
        return
    click.secho(f"\nGerando relatório para: {user.name}", fg="cyan")

    user_attempts = data.get_attempts_by_user_id(user.id_user)
    if not user_attempts:
        click.echo("Este usuário ainda não realizou nenhuma tentativa.")
        return

    stats_calculator = Statistics()
    report_data = stats_calculator.generate_user_performance_report(user_attempts, data)

    click.secho(f"\n--- Relatório de Performance: {user.name} ---", bold=True)
    click.echo(f"  Total de tentativas realizadas: {report_data['total_attempts']}")
    click.echo(f"  Taxa de acerto média geral: {report_data['average_score_percent']:.2f}%")
    
    click.secho("\nDesempenho por Tema:", bold=True)
    if report_data['performance_by_theme']:
        for theme, stats in report_data['performance_by_theme'].items():
            click.echo(f"  - {theme}: {stats['average_score']:.2f}% de acerto ({stats['correct_answers']}/{stats['total_questions']})")
    else:
        click.echo("  Nenhum tema registrado nas tentativas.")

@report.command("ranking")
def ranking_report():
    """Exibe o ranking de usuários por pontuação média."""
    click.secho("\n--- Ranking de Usuários ---", bold=True)
    all_attempts = data.get_all_attempts_for_ranking()
    if not all_attempts:
        click.echo("Nenhuma tentativa registrada no sistema para gerar ranking.")
        return
    
    ranking_data = Statistics.generate_ranking_report(all_attempts)

    for i, user_rank in enumerate(ranking_data):
        click.echo(f"  {i+1}º. {user_rank['user_name']} - {user_rank['average_score_percent']:.2f}% de aproveitamento")

@report.command("missed-questions")
def missed_questions_report():
    """Exibe as questões mais erradas do sistema."""
    click.secho("\n--- Questões Mais Erradas do Sistema ---", bold=True)
    report_data = Statistics.most_missed_questions(data)
    if not report_data:
        click.echo("Nenhum erro registrado ainda.")
        return
    
    for item in report_data[:10]:
        click.echo(f"  - Erros: {item['miss_count']} | ID: {item['id_question']} | Enunciado: \"{item['statement'][:50]}...\"")

@report.command("evolution")
def evolution_report():
    """Exibe a evolução de desempenho de um usuário ao longo do tempo."""
    user = get_user_from_prompt()
    if not user:
        click.echo("Nenhum usuário encontrado para gerar relatório.")
        return
    click.secho(f"\nGerando relatório de evolução para: {user.name}", fg="cyan")

    user_attempts = data.get_attempts_by_user_id(user.id_user)
    if not user_attempts:
        click.echo("Este usuário ainda não realizou nenhuma tentativa.")
        return
    
    report_data = Statistics.user_evolution_report(user_attempts)

    click.secho(f"\n--- Evolução de Desempenho: {user.name} ---", bold=True)
    for timestamp, performance in report_data:
        click.echo(f"  - Data: {timestamp} | Desempenho: {performance:.2f}%")

start_cli = cli