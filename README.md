Team Tracker

Team Tracker is a full-stack web application designed to manage employee records, roles, and permissions efficiently. It provides role-based access control (RBAC), enabling HR admins to manage employees while allowing managers and employees access to relevant data.

Table of Contents

User Experience (UX)

Agile Methodology

Features

Technologies Used

Installation & Setup

Testing

Deployment

Known Issues & Future Improvements

Acknowledgments

User Experience (UX)

Project Goals

Efficient Employee Management: Maintain accurate records of employees, contracts, and roles.

Role-Based Permissions: Ensure users only access relevant information.

Secure Authentication: Enforce login protection and access control.

Responsive & User-Friendly Interface: Accessible across different devices.

User Roles & Goals

Role

Goals

HR Admin

Manage all employees and assign roles.

Manager

View and manage team members.

Employee

View personal details and contracts.

Agile Methodology

Team Tracker was developed using Agile methodology. The project followed iterative development cycles with continuous feedback and improvements.

User Stories

As an HR Admin, I want to add employees so I can manage the workforce.

As an HR Admin, I want to assign roles so employees have correct access.

As a Manager, I want to view my team members so I can track their details.

As an Employee, I want to view my personal details so I can check my contract status.

As an HR Admin, I want to restrict permissions so sensitive data is protected.

Task Tracking

GitHub Projects was used for task tracking (View Here).

Features were divided into milestones with clear goals.

User stories and sprint progress were documented within GitHub Projects.

Pull requests followed structured code reviews before merging.

Features

User Authentication & Authorization

Secure login and logout functionality.

Role-based permissions to control access.

Employee Management

Create, update, and delete employee records.

Assign managers to employees.

Contract Management

Add employment contracts with job titles, start/end dates, and salary information.

Role-Based Access Control (RBAC)

Assign permissions based on roles.

Prevent unauthorized access to sensitive data.

Dashboard Overview

Summary of employees and active contracts.

Search & Filtering

Easily locate employees and contracts.

Technologies Used

Languages & Frameworks

Backend: Django (Python)

Frontend: Django Templates, HTML, CSS

Database: SQLite (for development), PostgreSQL (for production)

Version Control: Git & GitHub

Deployment: (To be added - Heroku, Railway, or other cloud platforms)

Installation & Setup

Prerequisites

Ensure you have the following installed:

Python 3.9+

pip

virtualenv

Setup Steps

Clone the Repository:

git clone https://github.com/itjosephk2/team_tracker.git
cd team_tracker

Create a Virtual Environment:

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt

Run Migrations:

python manage.py migrate

Create a Superuser (Admin Account):

python manage.py createsuperuser

Run the Server:

python manage.py runserver

Access the application at http://127.0.0.1:8000/

Testing

Unit Tests: Located in tests.py files within each app.

Run Tests:

python manage.py test

Example Test Case:

from django.test import TestCase
from people_management.models import Person

class PersonModelTest(TestCase):
    def test_create_person(self):
        person = Person.objects.create(first_name="John", last_name="Doe")
        self.assertEqual(person.first_name, "John")

Manual Testing:

Verify login, role-based access, CRUD functionality.

Test edge cases (invalid logins, unauthorized access attempts).

Deployment

(Once deployment is complete, add specific details here.)

Deployment Steps

Deploy the application using Heroku/Railway.

Set up environment variables for security (DEBUG=False).

Configure database settings for PostgreSQL.

Known Issues & Future Improvements

Add Automated Testing: Improve test coverage.

Enhance Frontend UI: Make forms and dashboard more user-friendly.

Implement Email Notifications: Notify users about contract updates.

Acknowledgments

Special thanks to Django documentation and Stack Overflow for troubleshooting support.

Project inspired by modern HR management tools.

Project Repository: GitHub
