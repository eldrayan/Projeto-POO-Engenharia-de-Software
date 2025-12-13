import pytest
from quiz.models.statistics import Statistics
from quiz.models.attempt import Attempt

def test_generate_ranking_report():
    stats = Statistics()
    
    mock_attempts = [
        {"id_user": 1, "user_name": "Alice", "score": 8, "max_possible_score": 10},
        {"id_user": 2, "user_name": "Bob", "score": 5, "max_possible_score": 10},
        {"id_user": 1, "user_name": "Alice", "score": 10, "max_possible_score": 10},
    ]
        
    ranking = stats.generate_ranking_report(mock_attempts)
    
    assert len(ranking) == 2
    assert ranking[0]["user_name"] == "Alice"
    assert ranking[0]["average_score_percent"] == 90.0
    assert ranking[1]["user_name"] == "Bob"
    assert ranking[1]["average_score_percent"] == 50.0

def test_generate_user_performance_report(populated_db):
    db, user, quiz = populated_db
    stats = Statistics()

    attempt = Attempt(None, id_quiz=1, id_user=user.id_user, score=1, time=30.0, answers=[2, 0], attempt_number=1)
    db.add_attempt(attempt)
    
    user_attempts_data = db.get_attempts_by_user_id(user.id_user)
    report = stats.generate_user_performance_report(user_attempts_data, db)

    assert report["total_attempts"] == 1
    assert report["average_score_percent"] == 50.0
    assert "Geografia" in report["performance_by_theme"]
    assert "Matemática" in report["performance_by_theme"]
    assert report["performance_by_theme"]["Geografia"]["average_score"] == 100.0 
    assert report["performance_by_theme"]["Matemática"]["average_score"] == 0.0 

def test_most_missed_questions(populated_db):
    db, user, quiz = populated_db
    stats = Statistics()

    attempt1 = Attempt(None, id_quiz=1, id_user=user.id_user, score=1, time=30.0, answers=[2, 0], attempt_number=1)
    attempt2 = Attempt(None, id_quiz=1, id_user=user.id_user, score=0, time=30.0, answers=[0, 0], attempt_number=2)
    db.add_attempt(attempt1)
    db.add_attempt(attempt2)

    missed_report = stats.most_missed_questions(db)

    assert len(missed_report) == 2
    
    assert missed_report[0]["miss_count"] == 2
    assert "2+2" in missed_report[0]["statement"]

    assert missed_report[1]["miss_count"] == 1
    assert "França" in missed_report[1]["statement"]