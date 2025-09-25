from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, user_type):
        self.username = username
        self.user_type = user_type
        self.set_password(password)

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'user_type': self.user_type,
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    studentName = db.Column(db.String(100), nullable=False)
    totalHours = db.Column(db.Integer, default=0)
    studentEmail = db.Column(db.String(100))
    
    # Fixed relationships with proper foreign_keys parameter
    loggedHours = db.relationship('LoggedHours', backref='student', lazy=True)
    accolades = db.relationship('Accolade', backref='student', lazy=True)

    def __init__(self, username, password, studentName, studentEmail):
        super().__init__(username, password, user_type='student')
        self.studentName = studentName
        self.studentEmail = studentEmail

    def get_json(self):
        data = super().get_json()
        data.update({
            'studentName': self.studentName,
            'studentEmail': self.studentEmail,
            'totalHours': self.totalHours,
            'loggedHours': [log.get_json() for log in self.loggedHours],
            'accolades': [accolade.get_json() for accolade in self.accolades]
        })
        return data

    def requestConfirmation(self, log):
        """Request confirmation for logged hours"""
        if log.studentID == self.id and not log.isConfirmed:
            request = ConfirmRequest(
                loggedHoursID=log.logID,
                studentID=self.id,
                requestDate=datetime.utcnow()
            )
            db.session.add(request)
            db.session.commit()
            return request
        return None

    def viewLeaderBoard(self):
        """View current leaderboard"""
        leaderboard = Leaderboard()
        return leaderboard.generateRankings()

    def viewAccolades(self):
        """View student's accolades"""
        return self.accolades

class Staff(User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    staffName = db.Column(db.String(100), nullable=False)
    staffEmail = db.Column(db.String(100))
    
    # Fixed relationship
    confirmedHours = db.relationship('LoggedHours', backref='confirming_staff', 
                                   foreign_keys='LoggedHours.staffID', lazy=True)

    def __init__(self, username, password, staffName, staffEmail):
        super().__init__(username, password, user_type='staff')
        self.staffName = staffName
        self.staffEmail = staffEmail

    def get_json(self):
        data = super().get_json()
        data.update({
            'staffName': self.staffName,
            'staffEmail': self.staffEmail,
            'hoursConfirmed': [log.get_json() for log in self.confirmedHours if log.isConfirmed]
        })
        return data

    def logHours(self, student, hours, description):
        """Log hours for a student"""
        log_entry = LoggedHours(
            studentID=student.id,
            staffID=self.id,
            hours=hours,
            description=description,
            logDate=datetime.utcnow(),
            isConfirmed=False
        )
        db.session.add(log_entry)
        db.session.commit()
        return log_entry

    def confirmHours(self, log):
        """Confirm logged hours"""
        if not log.isConfirmed:
            log.isConfirmed = True
            log.dateConfirmed = datetime.utcnow()
            
            # Update student's total hours
            student = Student.query.get(log.studentID)
            if student:
                confirmed_hours = LoggedHours.query.filter_by(
                    studentID=student.id, isConfirmed=True).all()
                student.totalHours = sum(hour.hours for hour in confirmed_hours)
                self.checkAccolades(student)
                db.session.commit()
                return log
        return None

    def checkAccolades(self, student):
        """Check and award accolades based on milestones"""
        milestones = [10, 25, 50]
        for milestone in milestones:
            if student.totalHours >= milestone:
                existing_accolade = Accolade.query.filter_by(
                    studentID=student.id, milestone=milestone).first()
                if not existing_accolade:
                    accolade = Accolade(
                        studentID=student.id,
                        milestone=milestone,
                        dateAwarded=datetime.utcnow()
                    )
                    db.session.add(accolade)

class LoggedHours(db.Model):
    __tablename__ = 'loggedHours'
    logID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))
    logDate = db.Column(db.DateTime, default=datetime.utcnow)
    isConfirmed = db.Column(db.Boolean, default=False)
    dateConfirmed = db.Column(db.DateTime)

    def get_json(self):
        return {
            'logID': self.logID,
            'studentID': self.studentID,
            'staffID': self.staffID,
            'hours': self.hours,
            'description': self.description,
            'logDate': self.logDate.isoformat() if self.logDate else None,
            'isConfirmed': self.isConfirmed,
            'dateConfirmed': self.dateConfirmed.isoformat() if self.dateConfirmed else None
        }

    def setStudentStatus(self, studentStatus):
        """Set confirmation status"""
        if studentStatus.lower() == 'confirmed':
            self.isConfirmed = True
            self.dateConfirmed = datetime.utcnow()
        else:
            self.isConfirmed = False
        db.session.commit()
        
    def getHours(self):
        """Get hours logged"""
        return self.hours   

class Accolade(db.Model):
    __tablename__ = 'accolade'
    accoladeID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    milestone = db.Column(db.Integer, nullable=False)
    dateAwarded = db.Column(db.DateTime, default=datetime.utcnow)

    def get_json(self):
        milestone_names = {10: "Bronze Service Award", 25: "Silver Service Award", 50: "Gold Service Award"}
        return {
            'accoladeID': self.accoladeID,
            'studentID': self.studentID,
            'milestone': self.milestone,
            'name': milestone_names.get(self.milestone, f"{self.milestone} Hour Award"),
            'dateAwarded': self.dateAwarded.isoformat() if self.dateAwarded else None
        }

    def assignedToStudent(self, student):
        """Assign accolade to student"""
        self.studentID = student.id
        db.session.commit()

    def getMilestone(self):
        """Get milestone hours"""
        return self.milestone
    
class ConfirmRequest(db.Model):
    __tablename__ = 'confirmRequest'
    requestID = db.Column(db.Integer, primary_key=True)
    loggedHoursID = db.Column(db.Integer, db.ForeignKey('loggedHours.logID'), nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    requestDate = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

    def get_json(self):
        return {
            'requestID': self.requestID,
            'loggedHoursID': self.loggedHoursID,
            'studentID': self.studentID,
            'requestDate': self.requestDate.isoformat() if self.requestDate else None,
            'status': self.status
        }

class Leaderboard:
    def __init__(self):
        self.studentRanks = []

    def generateRankings(self):
        """Generate student rankings based on confirmed hours"""
        students = Student.query.all()
        student_hours = []
        
        for student in students:
            total = db.session.query(db.func.sum(LoggedHours.hours)).filter_by(
                studentID=student.id, isConfirmed=True).scalar() or 0
            student.totalHours = total  # Update the student's total
            student_hours.append((student, total))
        
        # Sort by hours descending
        ranked_students = sorted(student_hours, key=lambda x: x[1], reverse=True)
        self.studentRanks = [student for student, hours in ranked_students]
        return self.studentRanks

    def topAchiever(self, n: int):
        """Get top N achievers"""
        if not self.studentRanks:
            self.generateRankings()
        return self.studentRanks[:n]

    def get_json(self):
        """Get leaderboard as JSON"""
        if not self.studentRanks:
            self.generateRankings()
        rankings = []
        for i, student in enumerate(self.studentRanks, 1):
            rankings.append({
                'rank': i,
                'studentID': student.id,
                'studentName': student.studentName,
                'totalHours': student.totalHours
            })
        return rankings