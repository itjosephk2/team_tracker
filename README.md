# Team Tracker
![Dashboard](./assets/dashboard/admin_dashboard.png)

**Live Application:** [Team Tracker](https://team-tracker-d6988ecc9291.herokuapp.com/)

Team Tracker is a full-stack web application designed to manage employee records, roles, and permissions efficiently. It provides **role-based access control (RBAC)**, enabling HR admins to manage employees while allowing managers and employees access to relevant data.

## Table of Contents

1. [Data Models](#data-models)
2. [User Experience (UX)](#user-experience-ux)
3. [Agile Methodology](#agile-methodology)
4. [Features](#features)
5. [Technologies Used](#technologies-used)
6. [Installation & Setup](#installation--setup)
7. [Testing](#testing)
8. [Troubleshooting Common Errors](#troubleshooting-common-errors)
9. [Deployment](#deployment)
10. [Known Issues & Future Improvements](#known-issues--future-improvements)
11. [Acknowledgments](#acknowledgments)

---

## Data Models

### **Person**

| Field Name    | Type                    | Notes                                                         |
| ------------- | ----------------------- | ------------------------------------------------------------- |
| id            | AutoField               | Primary Key (automatically added by Django)                   |
| first_name    | CharField(50)           | Employee’s first name                                         |
| last_name     | CharField(50)           | Employee’s last name                                          |
| email         | EmailField(unique=True) | Must be unique                                                |
| phone_number  | CharField(15)           | Optional contact number                                       |
| date_of_birth | DateField               | Required                                                      |
| active        | BooleanField            | Defaults to `False`; updated based on contract status         |
| manager       | ForeignKey('self')      | Nullable; represents the employee’s direct manager            |
| role          | CharField(choices)      | 'employee', 'manager', or 'hr_admin'                          |
| user          | OneToOneField(User)     | Nullable link to Django `User` for authentication             |
| history       | HistoricalRecords       | Enables tracking of model changes (via django-simple-history) |

### **Contract**

| Field Name       | Type                 | Notes                                                   |
| ---------------- | -------------------- | ------------------------------------------------------- |
| id               | AutoField            | Primary Key                                             |
| person           | ForeignKey(Person)   | Required; cascades on delete                            |
| job_title        | CharField(255)       | The title for the position associated with the contract |
| contract_start   | DateField            | Start date of the contract                              |
| contract_end     | DateField (nullable) | Can be left blank for ongoing contracts                 |
| hourly_rate      | FloatField           | Defaults to €12.45                                      |
| contracted_hours | FloatField           | Defaults to 40 hours/week                               |
| history          | HistoricalRecords    | Tracks historical changes to each contract              |

## User Experience (UX)

### **Project Goals**

-    **Efficient Employee Management:** Maintain accurate records of employees, contracts, and roles.
-    **Role-Based Permissions:** Ensure users only access relevant information.
-    **Secure Authentication:** Enforce login protection and access control.
-    **Responsive & User-Friendly Interface:** Accessible across different devices.

### **User Roles & Goals**

| Role     | Goals                                  |
| -------- | -------------------------------------- |
| HR Admin | Manage all employees and assign roles. |
| Manager  | View and manage team members.          |
| Employee | View personal details and contracts.   |

User Roles have been replaced to use djangos in built permission system. There is base of HR Admin, Manager, Employee for permissions but custom groups are creatable. Permissions are checked for as mixins with the class based views. If the user has a group with the required permiission they can access the functionality. Roled are used to restrict the sidenav of the dashboard.

![Permissions](./assets/groups/assign_permission.png)

---

## Agile Methodology

Team Tracker was developed using Agile methodology. The project followed iterative development cycles with continuous feedback and improvements. This can be seen in the project section of the repository where epics, user stories, priorities and assignment etc can be seen to be used in the process. 

### **User Stories**

Here is some example of user stories. The full list of user stories can be seen in the projects attached to this repository. 
1. As an HR Admin, I want to add employees so I can manage the workforce.
2. As an Hr Admin, I want to add contracts and attach them to employees.
3. As an HR Admin, I want to assign permissions to users so they can access the software.
4. As a Manager, I want to view my team members so I can track their details.
5. As a Manager, I want to add contracts and attach them to employees who are in my team.
6. As a Manager, I want to add contracts to the employee that I can manage the workforce.
7. As an Employee, I want to view my personal details so I can check my contract status.

### **Task Tracking**

-    **GitHub Projects was used for task tracking** ([View Here](https://github.com/itjosephk2/team_tracker/projects?query=is%3Aopen)).
-    Features were divided into milestones with clear goals.
-    User stories and sprint progress were documented within GitHub Projects.
-    Pull requests followed structured code reviews before merging.
-    Epics were brken downinto user stories

---

## Features

-    **User Authentication & Authorization**
     -    Secure login and logout functionality.
     -    Role-based permissions to control access.
-    **Employee Management**
     -    Create, update, and delete employee records.
     -    Assign managers to employees.
-    **Contract Management**
     -    Add employment contracts with job titles, start/end dates, and salary information.
-    **Role-Based Access Control (RBAC)**
     -    Assign permissions based on roles.
     -    Prevent unauthorized access to sensitive data.
-    **Dashboard Overview**
     -    Summary of employees and active contracts.
-    **Search & Filtering**
     -    Easily locate employees and contracts.

---

## Technologies Used

### **Languages & Frameworks**

-    **Backend:** Django (Python)
-    **Frontend:** Django Templates, HTML, CSS
-    **Database:** SQLite (for development), PostgreSQL (for production)
-    **Version Control:** Git & GitHub
-    **Deployment:** (To be added - Heroku, Railway, or other cloud platforms)

---

## Installation & Setup

### **Prerequisites**

Ensure you have the following installed:

-    Python 3.9+
-    pip
-    virtualenv

### **Setup Steps**

1. **Clone the Repository:**

     ```bash
     git clone https://github.com/itjosephk2/team_tracker.git
     cd team_tracker
     ```

2. **Create a Virtual Environment:**

     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use: venv\Scripts\activate
     ```

3. **Install Dependencies:**

     ```bash
     pip install -r requirements.txt
     ```

4. **Run Migrations:**

     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Create a Superuser (Admin Account):**

     ```bash
     python manage.py createsuperuser
     ```

6. **Run the Server:**

     ```bash
     python manage.py runserver
     ```

     Access the application at `http://127.0.0.1:8000/`

---

## Testing

-    **Unit Tests:** Located in `tests.py` files within each app.
-    **Run Tests:**
     ```bash
     python manage.py test
     ```
-    **Example Test Case:**

     ```python
     from django.test import TestCase
     from people_management.models import Person

     class PersonModelTest(TestCase):
         def test_create_person(self):
             person = Person.objects.create(first_name="John", last_name="Doe")
             self.assertEqual(person.first_name, "John")
     ```

-    **Manual Testing:**
     -    Verify login, role-based access, CRUD functionality.
     -    Test edge cases (invalid logins, unauthorized access attempts).

---

## Troubleshooting Common Errors

### **Database Errors During Testing**

**Error:** `django.db.utils.ProgrammingError: relation "security_permissiondefinition" does not exist`

**Solution:** Ensure migrations are properly applied before running tests:

```bash
python manage.py makemigrations security people_management
python manage.py migrate
```

If the error persists, try resetting the test database:

```bash
python manage.py flush
```

Then, rerun:

```bash
python manage.py test
```

## Deployment (Heroku)

1. **Create Heroku app:**

   Create a new Heroku app using the following command. If you don't provide a name, Heroku will generate one for you.

   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables:**

   You'll need to set the environment variables required for your app, such as the secret key, debug mode, allowed hosts, and database URL. You can do this using the `heroku config:set` command:

   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   heroku config:set DATABASE_URL=your-postgres-url
   ```

   * **SECRET\_KEY**: Generate a secret key using a random string. For example, run:

     ```python
     python -c "import random; print(''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)', k=50)))"
     ```

   * **DATABASE\_URL**: Heroku automatically sets this environment variable when you add the PostgreSQL add‑on. If you're using another database, set this URL manually.

3. **Disable collectstatic (if not using static files):**

   If your application does not serve static files (e.g., you're not using `django-storages` or another static‑files backend), disable Heroku’s automatic static file collection:

   ```bash
   heroku config:set DISABLE_COLLECTSTATIC=1
   ```

4. **Deploy to Heroku:**

   Push your local code to Heroku via Git:

   ```bash
   git push heroku main
   ```

   > Ensure you're pushing the correct branch (`main`, `master`, etc.).

5. **Run migrations:**

   After deployment, apply database migrations:

   ```bash
   heroku run python manage.py migrate
   ```

---

### Additional Notes

* **Collect Static Files**
  If you *are* using static files, run:

  ```bash
  heroku run python manage.py collectstatic
  ```

  or add the [`django-heroku`](https://github.com/heroku/django-heroku) package to automate settings.

* **Scaling Dynos**
  To scale your web dynos:

  ```bash
  heroku ps:scale web=1
  ```

* **Logs**
  View real‑time logs with:

  ```bash
  heroku logs --tail
  ```

---

## Known Issues & Future Improvements

-    **Add Automated Testing:** Improve test coverage.
-    **Enhance Frontend UI:** Make forms and dashboard more user-friendly.
-    **Implement Email Notifications:** Notify users about contract updates.

---

## Acknowledgments

-    Special thanks to **Django documentation** and **Stack Overflow** for troubleshooting support.
-    Project inspired by modern HR management tools.

---

**Project Repository:** [GitHub](https://github.com/itjosephk2/team_tracker)
