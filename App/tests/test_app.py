import pytest
from App.main import create_app
from App.database import db, create_db
from App.controllers import (
    create_user, get_all_users, StudentController, StaffController, view_leaderboard
)


@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        create_db()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


"""
USER TESTS
"""
def test_create_user(app):
    user = create_user("alice", "alicepass", "student")
    assert user is not None
    assert user.username == "alice"
    assert user.check_password("alicepass")

def test_get_all_users(app):
    create_user("john", "johnpass", "staff")
    users = get_all_users()
    assert any(u.username == "john" for u in users)


"""
STUDENT TESTS
"""
def test_create_student(app):
    student, msg = StudentController.create_student("bob", "bobpass", "Bob Marley", "bob@mail.com")
    assert student is not None
    assert student.studentName == "Bob Marley"

def test_student_leaderboard(app):
    s1, _ = StudentController.create_student("alice", "alicepass", "Alice", "alice@mail.com")
    s2, _ = StudentController.create_student("john", "johnpass", "John", "john@mail.com")
    s1.totalHours = 30
    s2.totalHours = 10
    db.session.add(s1)
    db.session.add(s2)
    db.session.commit()

    rankings, _ = view_leaderboard()
    assert rankings[0].studentName == "Alice"
    assert rankings[1].studentName == "John"

def test_student_accolades(app):
    s, _ = StudentController.create_student("eve", "evepass", "Eve", "eve@mail.com")
    staff, _ = StaffController.create_staff("staff_eve", "staffpass", "Staff Eve", "staff_eve@mail.com")
    # Log and confirm 50 hours
    log_entry, msg = StaffController.log_hours(staff.id, s.id, 50, "Service work")
    StaffController.confirm_hours(staff.id, log_entry.logID)
    accolades, msg = StudentController.view_accolades(s.id)
    assert accolades is not None
    assert any(a.milestone == 50 for a in accolades)


"""
STAFF TESTS
"""
def test_create_staff(app):
    staff, msg = StaffController.create_staff("john", "johnpass", "John Doe", "john@mail.com")
    assert staff is not None
    assert staff.staffName == "John Doe"

def test_staff_log_and_confirm_hours(app):
    # Create staff + student
    staff, _ = StaffController.create_staff("john", "johnpass", "John Doe", "john@mail.com")
    student, _ = StudentController.create_student("alice", "alicepass", "Alice", "alice@mail.com")

    # Staff logs hours for student
    log_entry, msg = StaffController.log_hours(staff.id, student.id, 5, "Community Service")
    assert log_entry is not None
    assert log_entry.hours == 5

    # Confirm hours
    confirmed, msg = StaffController.confirm_hours(staff.id, log_entry.logID)
    assert confirmed is not None
    assert confirmed.isConfirmed is True
    assert confirmed.hours == 5
