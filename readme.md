
# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

Initialize Database
# Empty database
flask init
flask initialize

# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```
#user commands:
# Create a user
```
flask user create <username> <password> <user_type>
```
# Example:
```
flask user create jake jakepass student
# Output:
# jake (student) created!
```
# List all users
```
flask user list string
```
# Output:
```
 Username: jake, Type: student
```

#student commands:
# Create a student
```
flask student create <username> <password> <studentName> <studentEmail>
```
# Example:
```
flask student create jake jakepass "Jake Johnson" jake@example.com
# Output:
# Student jake created successfully!
```

# List students
```
flask student list
```
# Output:
```
 ID: 1, Name: Jake Johnson, Hours: 0
```

# View leaderboard
```
flask student leaderboard
```
# Output:
```
 ===== STUDENT LEADERBOARD =====
1. Jake Johnson: 10 hours
 ===============================
```

# View accolades
```
flask student accolades <username>
```
# Example:
```
flask student accolades jake
 Output:
 === Jake Johnson's ACCOLADES ===
 Silver Service Award (25 hours)
```
staff Commands
# Create staff
```
flask staff create <username> <password> <staffName> <staffEmail>
```
# Example:
```
flask staff create admin adminpass "Alice Admin" admin@example.com
# Output:
# Staff admin created successfully!
```

# List staff
```
flask staff list
```
# Output:
```
 ID: 1, Name: Alice Admin, Email: admin@example.com
```

# Log hours for a student
```
flask staff log-hours <staff_username> <student_username> <hours> <description>
```
# Example:
```
flask staff log-hours admin jake 5 "Community cleanup"
# Output:
# Logged 5 hours for Jake Johnson: Community cleanup
# Log ID: 1
# isConfirmed: False
```

# Confirm student hours
```
flask staff confirm-hours <staff_username> <log_id>
```
# Example:
```
flask staff confirm-hours admin 1
# Output:
# Confirmed 5 hours for Jake Johnson
# Student's total hours: 15
```











