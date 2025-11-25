import pytest
from quiz.models.user import User
from quiz.models.quiz import Quiz
from quiz.models.question import Question
from quiz.models.multiplechoicequestion import MultipleChoiceQuestion
from quiz.models.attempt import Attempt
from quiz.models.settings import Settings

class Test_user:
    def test_user_correct_path(self):
        """Teste do caminho correto e mais esperado."""
        user = User(id_user=1, email='teste@exemplo.com', name='Usuario Teste')
        assert user.id_user == 1
        assert user.email == 'teste@exemplo.com'
        assert user.name == 'Usuario Teste'

    def test_user_set_invalid_email_raises_error(self):
        """Testa se um ValueError é levantado ao tentar definir um email inválido."""
        user = User(id_user=1, email='correto@exemplo.com', name='Usuario Teste')
        with pytest.raises(ValueError, match="O formato do email fornecido é inválido."):
            user.email = "emailinvalido"

    def test_user_set_empty_name_raises_error(self):
        """Testa se um ValueError é levantado ao tentar definir um nome vazio."""
        user = User(id_user=1, email='correto@exemplo.com', name='Usuario Teste')
        with pytest.raises(ValueError, match="O nome não pode estar vazio."):
            user.name = "   "

    def test_user_set_equal_name_raises_error(self):
        """Testa se um ValueError é levantado ao tentar definir um nome igual ao anterior."""
        user = User(id_user=1, email='correto@exemplo.com', name='Nome Atual')
        with pytest.raises(ValueError, match="O novo nome não pode ser o mesmo que o nome atual."):
            user.name = 'Nome Atual'

class Test_quiz:
    pass

class Test_question:
    pass

class Test_multiplechoicequestion:
    pass

class Test_attempt:
    pass

class Test_settings:
    pass

class Test_statistics:
    pass
