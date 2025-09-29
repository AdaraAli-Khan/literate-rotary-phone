
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







```

CLI COMMANDS - USER
```
-create a user: $ flask user create <username> <password> <user_type>
e.g
flask user create jake jakepass student
output: jake (student) created!

-list all users :$flask user list string
output: Username: jake, Type: student


```
CLI COMMANDS -STUDENT
```
-create a student : $flask student create <username> <password> <studentName> <studentEmail>
e.g flask student create jake jakepass "Jake Johnson" jake@example.com
output-Student jake created successfully!


-list all students: $flask student list
e.g ID: 1, Name: Jake Johnson, Hours: 0

-view leaderboard: $flask student leaderboard
e.gflask student leaderboard
output-===== STUDENT LEADERBOARD =====
            1. Jake Johnson: 10 hours
        ===============================

-view accolades: $flask student accolades <username>
e.g flask student accolades jake
output-  === Jake Johnson's ACCOLADES ===
          Silver Service Award (25 hours)


```
CLI COMMANDS- STAFF
```
-create staff :$flask staff create <username> <password> <staffName> <staffEmail>
e.g flask staff create admin adminpass "Alice Admin" admin@example.com
output- Staff admin created successfully!


-list all staff: $flask staff list
output-ID: 1, Name: Alice Admin, Email: admin@example.com

-log all hours for student: $flask staff log-hours <staff_username> <student_username> <hours> <description>
e.g flask staff log-hours admin jake 5 "Community cleanup"
output-Logged 5 hours for Jake Johnson: Community cleanup
        Log ID: 1
        isConfirmed: False

-confirm logged hours: $flask staff confirm-hours <staff_username> <log_id>
e.g flask staff confirm-hours admin 1
output:Confirmed 5 hours for Jake Johnson
       Student's total hours: 15

```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
