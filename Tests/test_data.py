import pytest
from quiz.models.attempt import Attempt

def test_add_and_get_user(test_db, sample_user):
    user_id = test_db.add_user(sample_user)
    retrieved_user = test_db.get_user_by_id(user_id)
    
    assert retrieved_user is not None
    assert retrieved_user.id_user == user_id
    assert retrieved_user.name == "Test User"
    assert retrieved_user.email == "test@user.com"

def test_add_and_get_quiz(test_db, sample_quiz):
    test_db.add_quiz(sample_quiz)
    
    retrieved_quiz = test_db.get_quiz_by_id(1)
    
    assert retrieved_quiz is not None
    assert retrieved_quiz.title == "Quiz Geral"
    assert len(retrieved_quiz.questions) == 2
    assert retrieved_quiz.questions[0].statement == "Qual a capital da França?"

def test_get_attempt_count(populated_db):
    db, user, quiz = populated_db
    quiz_id = 1
    
    attempt1 = Attempt(None, quiz_id, user.id_user, 1, 50.0, [2], 1)
    attempt2 = Attempt(None, quiz_id, user.id_user, 0, 45.0, [0], 2)
    db.add_attempt(attempt1)
    db.add_attempt(attempt2)
    
    count = db.get_attempt_count_for_quiz(quiz_id, user.id_user)
    assert count == 2

def test_delete_quiz(populated_db):
    db, _, _ = populated_db
    quiz_id_to_delete = 1
    
    assert db.get_quiz_by_id(quiz_id_to_delete) is not None
    
    db.delete_quiz_by_id(quiz_id_to_delete)
    
    assert db.get_quiz_by_id(quiz_id_to_delete) is None

def test_unique_email_constraint(test_db, sample_user):
    test_db.add_user(sample_user) 
    
    with pytest.raises(Exception, match="já está cadastrado"):
        test_db.add_user(sample_user) 