from App.models import User, Student, Staff, LoggedHours, Accolade, ConfirmRequest, Leaderboard
from App.database import db
from datetime import datetime

def create_user(username, password, user_type):
    if get_user_by_username(username):
        return None
    newuser = User(username=username, password=password, user_type=user_type)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    return [user.get_json() for user in users]

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.commit()
        return user
    return None

class StudentController:
    @staticmethod
    def create_student(username, password, studentName, studentEmail):
        try:
            existing_user = get_user_by_username(username)
            if existing_user:
                return None, "Username already exists"
            
            student = Student(
                username=username,
                password=password,
                studentName=studentName,
                studentEmail=studentEmail
            )
            db.session.add(student)
            db.session.commit()
            return student, "Successfully created student account"
        except Exception as e:
            db.session.rollback()
            return None, f"Cannot create student account: {str(e)}"

    @staticmethod
    def get_student(studentId):
        return Student.query.get(studentId)

    @staticmethod
    def get_student_username(username):
        return Student.query.filter_by(username=username).first()

    @staticmethod
    def get_all_students():
        return Student.query.all()

    @staticmethod
    def get_students_json():
        students = StudentController.get_all_students()
        if not students:
            return []
        return [student.get_json() for student in students]

    @staticmethod
    def request_confirmation(studentId, loggedHoursId):
        try:
            student = StudentController.get_student(studentId)
            loggedHours = LoggedHours.query.get(loggedHoursId)

            if not student:
                return None, "Student not found"
            if not loggedHours:
                return None, "Logged hours entry not found"
            if loggedHours.studentID != student.id:
                return None, "Logged hours entry does not belong to student"

            request = student.requestConfirmation(loggedHours)
            if request:
                return request, "Confirmation request submitted successfully"
            return None, "Cannot submit confirmation request"
        except Exception as e:
            return None, f"Error requesting confirmation: {str(e)}"

    @staticmethod
    def view_accolades(studentId):
        student = StudentController.get_student(studentId)
        if student:
            return student.viewAccolades(), "Retrieved student's accolades successfully"
        return [], "Student not found"

def view_leaderboard():
    """View current leaderboard"""
    try:
        leaderboard = Leaderboard()
        rankings = leaderboard.generateRankings()
        return rankings, "Retrieved leaderboard successfully"
    except Exception as e:
        return [], f"Error generating leaderboard: {str(e)}"

class StaffController:
    @staticmethod
    def create_staff(username, password, staffName, staffEmail):
        try:
            existing_user = get_user_by_username(username)
            if existing_user:
                return None, "Username already exists"
            
            staff = Staff(
                username=username,
                password=password,
                staffName=staffName,
                staffEmail=staffEmail
            )
            db.session.add(staff)
            db.session.commit()
            return staff, "Successfully created staff account"
        except Exception as e:
            db.session.rollback()
            return None, f"Cannot create staff account: {str(e)}"

    @staticmethod
    def get_staff(staffId):
        return Staff.query.get(staffId)

    @staticmethod
    def get_staff_username(username):
        return Staff.query.filter_by(username=username).first()

    @staticmethod
    def get_all_staff():
        return Staff.query.all()

    @staticmethod
    def get_staff_json():
        staff_members = StaffController.get_all_staff()
        if not staff_members:
            return []
        return [staff.get_json() for staff in staff_members]

    @staticmethod
    def log_hours(staffId, studentId, hours, description):
        try:
            staff = StaffController.get_staff(staffId)
            student = StudentController.get_student(studentId)
            
            if not staff:
                return None, "Staff not found"
            if not student:
                return None, "Student not found"
            if hours <= 0:
                return None, "Hours must be greater than zero"
            
            log_entry = staff.logHours(student, hours, description)
            return log_entry, "Logged hours successfully"
        except Exception as e:
            return None, f"Error logging hours: {str(e)}"

    @staticmethod
    def confirm_hours(staffId, loggedHoursId):
        try:
            staff = StaffController.get_staff(staffId)
            loggedHours = LoggedHours.query.get(loggedHoursId)
            
            if not staff:
                return None, "Staff not found"
            if not loggedHours:
                return None, "Logged hours entry not found"
            if loggedHours.isConfirmed:
                return None, "Hours already confirmed"
            
            confirmed_log = staff.confirmHours(loggedHours)
            if confirmed_log:
                return confirmed_log, "Hours confirmed successfully"
            return None, "Failed to confirm hours"
        except Exception as e:
            return None, f"Error confirming hours: {str(e)}"