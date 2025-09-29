This project is a Flask web application built using the MVC (Model–View–Controller) architecture.
It provides a platform for students and staff to interact in a structured way:
Students can track their volunteer or service hours, appear on leaderboards, and earn accolades/awards.
Staff can manage student accounts, log community service hours, and confirm hours submitted.
The system includes CLI commands for quick database management, user creation, logging hours, and viewing reports.

# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

1. Installing Dependencies
```bash
$ pip install -r requirements.txt
```

2.Initialize Database
# Empty database
flask init
flask initialize

# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```
#user commands:
3. Create a user
```
flask user create <username> <password> <user_type>
```
# Example:
```
flask user create jake jakepass student
# Output:
# jake (student) created!
```
4. List all users
```
flask user list string
```
# Output:
```
 Username: jake, Type: student
```

#student commands:
5. Create a student
```
flask student create <username> <password> <studentName> <studentEmail>
```
# Example:
```
flask student create mike mikepass "mike ali" mike@example.com
# Output:
# Student mike created successfully!
```

6. List students
```
flask student list
```
# Output:
```
 ID: 1, Name: mike ali, Hours: 0
```

7. View leaderboard
```
flask student leaderboard
```
# Output:
```
 ===== STUDENT LEADERBOARD =====
1. mike ali : 0 hours
 ===============================
```

8.View accolades
```
flask student accolades <username>
```
# Example:
```
flask student accolades mike
 Output:
 === Mike Johnson's ACCOLADES ===
No accolades earned yet.
```
staff Commands
9.Create staff
```
flask staff create <username> <password> <staffName> <staffEmail>
```
# Example:
```
flask staff create admin adminpass "Alice Admin" admin@example.com
# Output:
# Staff admin created successfully!
```

10. List staff
```
flask staff list
```
# Output:
```
 ID: 4, Name: Alice Admin, Email: admin@example.com
```
11. Log hours for a student
```
flask staff log-hours <staff_username> <student_username> <hours> <description>
```
# Example:
```
flask staff log-hours admin mike 5 "Community cleanup"
# Output:
# Logged 5 hours for Mike Ali: Community cleanup
# Log ID: 1
# isConfirmed: False
```

12.Confirm student hours
```
flask staff confirm-hours <staff_username> <log_id>
```
# Example:
```
flask staff confirm-hours admin 1
# Output:
# Confirmed 5 hours for Mike Ali
# Student's total hours: 15
```
#testing
```
$ pytest

$ pytest -s App/tests/test_app.py

$pytest App/tests/test_app.py

$pytest -k test_student_accolades

flask test user
```









