import pytest
from click.testing import CliRunner
from quiz.cli import cli
from unittest.mock import patch

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_register(runner, test_db):
    with patch('quiz.cli.data', test_db):
        result = runner.invoke(cli, ['register'], input='Test\ntest@cli.com')
        assert result.exit_code == 0
        assert "Usuário 'Test' cadastrado com sucesso!" in result.output

        result = runner.invoke(cli, ['register'], input='Test2\ntest@cli.com')
        assert "Erro ao cadastrar usuário" in result.output

def test_cli_list_empty(runner, test_db):
    with patch('quiz.cli.data', test_db):
        result = runner.invoke(cli, ['list'])
        assert result.exit_code == 0
        assert "Nenhum quiz encontrado" in result.output

def test_cli_list_with_quiz(runner, populated_db):
    db, _, _ = populated_db
    with patch('quiz.cli.data', db):
        result = runner.invoke(cli, ['list'])
        assert result.exit_code == 0
        assert "Quiz Geral" in result.output
        assert "2 questões" in result.output

def test_cli_report_ranking(runner, populated_db):
    db, user, _ = populated_db
    from quiz.models.attempt import Attempt
    db.add_attempt(Attempt(None, 1, user.id_user, 1, 30.0, [2, 0], 1))

    with patch('quiz.cli.data', db):
        result = runner.invoke(cli, ['report', 'ranking'])
        assert result.exit_code == 0
        assert "Ranking de Usuários" in result.output
        assert "Test User" in result.output
        assert "50.00% de aproveitamento" in result.output