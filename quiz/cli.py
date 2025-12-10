import time
import click
from .data import data
from .config import settings
from .models.quiz import Quiz
from .models.multiplechoicequestion import MultipleChoiceQuestion
from .models.attempt import Attempt
from .models.statistics import Statistics

@click.group()
def cli():
    """
    Inicia a Interface de Linha de Comando (CLI) para o sistema de Quiz.
    """
    click.echo("Bem-vindo ao Sistema de Quiz!")

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
        question_text = click.prompt("Insira o enunciado da questão (ou deixe em branco para finalizar)", default='', show_default=False)
        if not question_text:
            if len(questions) < min_questions:
                plural = "questão" if min_questions == 1 else "questões"
                click.echo(f"Um quiz precisa de pelo menos {min_questions} {plural}. Criação cancelada.")
                return
            break
        
        theme = click.prompt("  Qual o tema da questão?")
        difficulty = click.prompt("  Qual a dificuldade (1-Fácil, 2-Médio, 3-Difícil)?", type=click.IntRange(1, 3))
        
        answers = []
        for i in range(4):
            answer_text = click.prompt(f"  Opção {i+1}")
            answers.append(answer_text)
        
        while True:
            correct_option = click.prompt("  Qual é a opção correta (1-4)?", type=click.IntRange(1, 4))
            correct_answer_index = correct_option - 1
            break

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

@cli.command("take")
def run_quiz():
    """Responde a um quiz."""
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
    attempt_count = data.get_attempt_count_for_quiz(quiz.id_quiz)

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
        click.clear()
        click.echo(f"--- {quiz.title} ---\n")
        click.echo(f"Questão {i + 1} de {len(quiz)}:")
        click.echo(str(question))  

        user_choice = click.prompt("\nSua resposta", type=click.IntRange(1, len(question.alternatives)))
        user_answer_index = user_choice - 1
        user_answers.append(user_answer_index)

        if user_answer_index == question.correct_answer:
            score += 1
            click.secho("✓ Correto!", fg="green")
        else:
            correct_text = question.alternatives[question.correct_answer]
            click.secho(f"✗ Incorreto. A resposta era: {correct_text}", fg="red")
        time.sleep(1.5) 

    total_time = time.time() - start_time

    new_attempt = Attempt(
        id_attempt=None, id_quiz=quiz.id_quiz, score=score,
        time=total_time, answers=user_answers, attempt_number=attempt_count + 1
    )
    data.add_attempt(new_attempt)

    click.clear()
    click.echo("--- Resultado Final ---")
    click.echo(f"Quiz: {quiz.title}")
    click.echo(f"Você acertou {score} de {len(quiz)} questões.")
    click.echo(f"Tempo total: {total_time:.2f} segundos.")
    click.secho("\nSua tentativa foi salva com sucesso.", fg="cyan")

@cli.command("report")
def user_report():
    """Gera o relatório do usuário atual."""
    click.echo("Gerando relatório de performance...")

    report_data = data.get_all_attempts_for_report()

    if not report_data:
        click.echo("Nenhuma tentativa encontrada. Responda a um quiz primeiro usando 'python -m quiz take'.")
        return

    stats_calculator = Statistics()
    report = stats_calculator.generate_performance_report(report_data)

    click.secho(f"\n--- Relatório Geral de Performance ---", bold=True)
    click.echo(f"  Total de tentativas realizadas: {report['total_attempts']}")
    click.echo(f"  Quizzes distintos respondidos: {report['completed_quizzes']}")
    click.echo(f"  Pontuação média geral: {report['average_score_percent']:.2f}%")

start_cli = cli