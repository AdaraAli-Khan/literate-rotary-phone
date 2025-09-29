import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import (
    create_user, get_all_users_json, get_all_users,
    StudentController, StaffController,
    initialize, view_leaderboard
)

app = create_app()
migrate = get_migrate(app)

'''
Database init
'''
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('Database initialized')


'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="alice")
@click.argument("password", default="alicepass")
@click.argument("user_type", default="student")
def create_user_command(username, password, user_type):
    user = create_user(username, password, user_type)
    if user:
        print(f'{user.username} ({user.user_type}) created!')
    else:
        print(f'User "{username}" already exists!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    users = get_all_users()
    if not users:
        print("No users found.")
        return
    if format == 'string':
        for user in users:
            print(f"Username: {user.username}, Type: {user.user_type}")
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)


'''
Student Commands
'''
student_cli = AppGroup('student', help='Student object commands')

@student_cli.command("create", help="Creates a student")
@click.argument("username")
@click.argument("password")
@click.argument("studentName")
@click.argument("studentEmail")
def create_student_command(username, password, studentName, studentEmail):
    student, message = StudentController.create_student(username, password, studentName, studentEmail)
    if student:
        print(f'Student {username} created successfully!')
    else:
        print(f'Error: {message}')

@student_cli.command("list", help="Lists students")
def list_student_command():
    students = StudentController.get_students_json()
    for student in students:
        print(f"ID: {student['id']}, Name: {student['studentName']}, Hours: {student['totalHours']}")

@student_cli.command("leaderboard", help="Shows the student leaderboard")
def leaderboard_command():
    rankings, message = view_leaderboard()
    if rankings:
        print("\n===== STUDENT LEADERBOARD =====")
        for i, student in enumerate(rankings, 1):
            print(f"{i}. {student.studentName}: {student.totalHours} hours")
        print("=" * 32)
    else:
        print(f"Error: {message}")

@student_cli.command("accolades", help="Shows student accolades")
@click.argument("username")
def accolades_command(username):
    student = StudentController.get_student_username(username)
    if student:
        accolades, message = StudentController.view_accolades(student.id)
        print(f"\n=== {student.studentName}'s ACCOLADES ===")
        if accolades:
            for accolade in accolades:
                accolade_data = accolade.get_json()
                print(f"{accolade_data['name']} - {accolade_data['milestone']} hours")
        else:
            print("No accolades yet.")
    else:
        print("Student not found")

app.cli.add_command(student_cli)


'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("create", help="Creates a staff member")
@click.argument("username")
@click.argument("password")
@click.argument("staffName")
@click.argument("staffEmail")
def create_staff_command(username, password, staffName, staffEmail):
    staff, message = StaffController.create_staff(username, password, staffName, staffEmail)
    if staff:
        print(f'Staff {username} created successfully!')
    else:
        print(f'Error: {message}')

@staff_cli.command("list", help="Lists staff")
def list_staff_command():
    staff_members = StaffController.get_staff_json()
    if not staff_members:
        print("No staff members found.")
    else:
        for staff in staff_members:
            print(f"ID: {staff['id']}, Name: {staff['staffName']}, Email: {staff['staffEmail']}")

@staff_cli.command("log-hours", help="Log hours for a student")
@click.argument("staff_username")
@click.argument("student_username")
@click.argument("hours", type=int)
@click.argument("description")
def log_hours_command(staff_username, student_username, hours, description):
    staff = StaffController.get_staff_username(staff_username)
    student = StudentController.get_student_username(student_username)
    if not staff:
        print("Staff not found")
        return
    if not student:
        print("Student not found")
        return
    log_entry, message = StaffController.log_hours(staff.id, student.id, hours, description)
    if log_entry:
        print(f"Logged {hours} hours for {student.studentName}: {description} (Log ID {log_entry.logID})")
    else:
        print(f"Error: {message}")

@staff_cli.command("confirm-hours", help="Confirm student hours")
@click.argument("staff_username")
@click.argument("log_id", type=int)
def confirm_hours_command(staff_username, log_id):
    staff = StaffController.get_staff_username(staff_username)
    if not staff:
        print("Staff not found")
        return
    confirmed_log, message = StaffController.confirm_hours(staff.id, log_id)
    if confirmed_log:
        student = StudentController.get_student(confirmed_log.studentID)
        print(f"Confirmed {confirmed_log.hours} hours for {student.studentName} (Total: {student.totalHours})")
    else:
        print(f"Error: {message}")

app.cli.add_command(staff_cli)


'''
Test Commands
'''
test = AppGroup('test', help='Testing commands')

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)
