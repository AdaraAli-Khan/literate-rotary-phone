
import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users,StudentController,StaffController, initialize, view_leaderboard )

# Staff CLI commands  
staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("list", help="Lists all staff members")
def list_staff_command():
    staff_members = StaffController.get_staff_json()
    if not staff_members:
        print("No staff members found.")
    else:
        for staff in staff_members:
            print(f"ID: {staff['id']}, Name: {staff['staffName']}, Email: {staff['staffEmail']}")


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("user_type", default="student")
def create_user_command(username, password, user_type):
    user = create_user(username, password, user_type)
    if user:
        print(f'{user.username} ({user.user_type}) created!')
    else:
        print(f'User with username "{username}" already exists!')

# this command will be : flask user create bob bobpass

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





app.cli.add_command(user_cli) # add the group to the cli

# Student CLI commands
student_cli = AppGroup('student', help='Student object commands')


@student_cli.command("create", help="Creates a student")
@click.argument("username")
@click.argument("password")
@click.argument("studentname")
@click.argument("studentemail")
def create_student_command(username, password, studentname, studentemail):
    student, message = StudentController.create_student(username, password, studentname, studentemail)
    if student:
        print(f'Student {username} created successfully!')
    else:
        print(f'Error creating student: {message}')

@student_cli.command("list", help="Lists students in the database")
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
                # Choose emoji and label based on milestone
                if accolade_data['milestone'] == 10:
                    emoji = '🥉'
                elif accolade_data['milestone'] == 25:
                    emoji = '🥈'
                elif accolade_data['milestone'] == 50:
                    emoji = '🥇'
                else:
                    emoji = '🏆'
                print(f"{emoji} {accolade_data['name']} ({accolade_data['milestone']} hours)")
        else:
            print("No accolades earned yet.")
    else:
        print("Student not found")

app.cli.add_command(student_cli)

# Staff CLI commands  
staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("list", help="Lists all staff members")
def list_staff_command():
    staff_members = StaffController.get_staff_json()
    if not staff_members:
        print("No staff members found.")
    else:
        for staff in staff_members:
            print(f"ID: {staff['id']}, Name: {staff['staffName']}, Email: {staff['staffEmail']}")


@staff_cli.command("create", help="Creates a staff member")
@click.argument("username")
@click.argument("password")
@click.argument("staffname")
@click.argument("staffemail")
def create_staff_command(username, password, staffname, staffemail):
    staff, message = StaffController.create_staff(username, password, staffname, staffemail)
    if staff:
        print(f'Staff {username} created successfully!')
    else:
        print(f'Error creating staff: {message}')

@staff_cli.command("log-hours", help="Log hours for a student")
@click.argument("staff_username")
@click.argument("student_username")
@click.argument("hours", type=int)
@click.argument("description")
def log_hours_command(staff_username, student_username, hours, description):
    staff = StaffController.get_staff_username(staff_username)
    student = StudentController.get_student_username(student_username)
    
    if not staff:
        print("Staff member not found")
        return
    if not student:
        print("Student not found") 
        return
    
    log_entry, message = StaffController.log_hours(staff.id, student.id, hours, description)
    if log_entry:
        print(f"Logged {hours} hours for {student.studentName}: {description}")
        print(f"Log ID: {log_entry.logID}")
        print(f"isConfirmed: {getattr(log_entry, 'isConfirmed', None)}")
    else:
        print(f"Error: {message}")

@staff_cli.command("confirm-hours", help="Confirm hours for student")
@click.argument("staff_username")
@click.argument("log_id", type=int)
def confirm_hours_command(staff_username, log_id):
    staff = StaffController.get_staff_username(staff_username)
    if not staff:
        print("Staff member not found")
        return
        
    confirmed_log, message = StaffController.confirm_hours(staff.id, log_id)
    if confirmed_log:
        student = StudentController.get_student(confirmed_log.studentID)
        print(f"Confirmed {confirmed_log.hours} hours for {student.studentName}")
        print(f"Student's total hours: {student.totalHours}")
    else:
        print(f"Error: {message}")

app.cli.add_command(staff_cli)

# Student CLI commands
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
        print(f'Error creating student: {message}')

@student_cli.command("list", help="Lists students in the database")
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
                print(f"🏆 {accolade_data['name']} - {accolade_data['milestone']} hours")
        else:
            print("No accolades earned yet.")
    else:
        print("Student not found")

# Staff CLI commands  
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
        print(f'Error creating staff: {message}')

@staff_cli.command("log-hours", help="Log hours for a student")
@click.argument("staff_username")
@click.argument("student_username")
@click.argument("hours", type=int)
@click.argument("description")
def log_hours_command(staff_username, student_username, hours, description):
    staff = StaffController.get_staff_username(staff_username)
    student = StudentController.get_student_username(student_username)
    
    if not staff:
        print("Staff member not found")
        return
    if not student:
        print("Student not found") 
        return
        
    log_entry, message = StaffController.log_hours(staff.id, student.id, hours, description)
    if log_entry:
        print(f"Logged {hours} hours for {student.studentName}: {description}")
        print(f"Log ID: {log_entry.logID}")
    else:
        print(f"Error: {message}")

@staff_cli.command("confirm-hours", help="Confirm hours for student")
@click.argument("staff_username")
@click.argument("log_id", type=int)
def confirm_hours_command(staff_username, log_id):
    staff = StaffController.get_staff_username(staff_username)
    if not staff:
        print("Staff member not found")
        return
        
    confirmed_log, message = StaffController.confirm_hours(staff.id, log_id)
    if confirmed_log:
        student = StudentController.get_student(confirmed_log.studentID)
        print(f"Confirmed {confirmed_log.hours} hours for {student.studentName}")
        print(f"Student's total hours: {student.totalHours}")
    else:
        print(f"Error: {message}")

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