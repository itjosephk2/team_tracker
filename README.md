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

The design philosophy for this system was centered on **simplicity**, **clarity**, and **role-based dashboards**. The goal was to offer each user a tailored experience based on their role — whether HR Admin, Manager, or Employee — while maintaining consistency and scalability.

### 🧭 Design Goals

- **Dashboard-Centric Interface:**  
  The core navigation experience revolves around a dashboard with quick-access widgets. These widgets offer a snapshot of the most relevant data for the user’s role.

- **Two Types of Views:**
  1. **Dashboard Widgets** — white background with black outlines. Lightweight and dynamic.
  2. **Form Pages** — grey background with shadow. More static, focused on data input and updates.

This visual distinction supports intuitive navigation and helps users immediately understand the difference between overview vs. action.

---
### **User Roles & Goals**

| Role     | UX Focus                                 | Permissions Behavior                             |
|----------|-------------------------------------------|--------------------------------------------------|
| HR Admin | Manage all employees and assign roles     | Full access to all features via group permissions |
| Manager  | View and manage team members              | Limited to own team; no access to Security       |
| Employee | View personal details and contracts only  | Read-only interface                              |

The application uses a **hybrid access control model**:

- **Roles (`person.role`)** are stored in the database and used to control the **dashboard layout and sidebar navigation**.
- **Django Groups and Permissions** determine what actions users can perform (e.g., adding people, editing contracts).

This structure allows:
- A flexible UI tailored to each user's role
- Secure backend enforcement using Django’s built-in permission system
- Easy expansion of access logic without rewriting frontend views

### 👥 Role-Specific UX

Each role experiences a different version of the system:

- **HR Admin:**
  - Full access to People, Contracts, and Security
  - Can manage users and assign permission groups
  - Sees all employees and all contracts

- **Manager:**
  - Sees only their assigned employees (via `manager` field)
  - Can create/edit contracts for those employees
  - No access to user or group management

- **Employee:**
  - Can only see their own personal and contract data
  - Read-only experience, no ability to manage or update records

### 🔐 Permissions & Modular Access

- Permissions are assigned through **Groups** (e.g., `people.add_person`, `contracts.view_contract`)
- The system uses Django **permission mixins** in class-based views to check access
- Admins can configure new Groups to create custom permission sets
- If a user has the required permission, the associated action or page becomes accessible

### ✅ Summary

- `person.role` → controls what you **see**
- Django permissions → control what you **can do**

---

### 🔁 Data Flow Considerations

- **User creation is linked to People:**  
  You must create a `Person` record first before assigning a Django `User`. This ensures that each login account is tied to a known employee or manager.

- **Contract logic drives employee status:**
  - When a contract is added or ends, the system checks and updates the person’s `active` status.
  - This avoids manual status toggling and reduces admin overhead.
  - Multiple contracts can be assigned per person to support job transitions or multi-role staff.

---

### 📁 Sections Breakdown

To support user flow, the system is divided into clear sections:

| Section            | Purpose                                 | Role Required      |
|--------------------|------------------------------------------|--------------------|
| **Dashboard**       | View widgets with personal/team data     | All users          |
| **People Management** | Manage employee records                 | Manager, HR Admin  |
| **Contract Management** | Manage job contracts                 | Manager, HR Admin  |
| **Security**        | Create users, assign groups/permissions  | HR Admin only      |

---

### 🧠 Implementation Reasoning

- **Modularity:** Permissions and groups make it easy to expand or restrict functionality.
- **Responsibility Delegation:** Managers can manage their own teams, reducing admin workload.
- **Role Isolation:** Clear UX boundaries between what each role can see/do help prevent errors and improve user trust.
- **Visual Cues:** The contrast between widgets and forms makes navigation feel intuitive without needing training.

---

### 🖼️ Wireframes & Mockups

The following wireframes were created during the design process and influenced the implementation of both structure and visual hierarchy. You can see how they translate directly into the implemented dashboard, people list, forms, and navigation system.

**📌 All Employees**  
<img src="./assets/wireframes/All_Employees.jpg" alt="All Employees" width="600"/>

**📌 Audit Log**  
<img src="./assets/wireframes/Audit.jpg" alt="Audit Log" width="600"/>

**📌 Contract Details**  
<img src="./assets/wireframes/Contract_details.jpg" alt="Contract Details" width="600"/>

**📌 Update Contract**  
<img src="./assets/wireframes/contract_update.jpg" alt="Contract Update" width="600"/>

**📌 Contracts List**  
<img src="./assets/wireframes/Contracts.jpg" alt="Contracts" width="600"/>

**📌 Delete Confirmation**  
<img src="./assets/wireframes/Delete.jpg" alt="Delete" width="600"/>

**📌 Edit Person**  
<img src="./assets/wireframes/Edit_person.jpg" alt="Edit Person" width="600"/>

**📌 Groups Management**  
<img src="./assets/wireframes/Groups.jpg" alt="Groups" width="600"/>

**📌 Login**  
<img src="./assets/wireframes/Login.jpg" alt="Login" width="600"/>

**📌 Dashboard (Main)**  
<img src="./assets/wireframes/Main.jpg" alt="Main Dashboard" width="600"/>

**📌 New Contract**  
<img src="./assets/wireframes/New_contract.jpg" alt="New Contract" width="600"/>

**📌 New Person**  
<img src="./assets/wireframes/New_person.jpg" alt="New Person" width="600"/>

**📌 View Person**  
<img src="./assets/wireframes/View_person.jpg" alt="View Person" width="600"/>


```




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

### 🔐 User Authentication

The application uses Django's built-in authentication system to manage secure login. Users must sign in to access any functionality. 

#### 🔑 Sign-In Page

The sign-in page is simple and functional. Users log in with credentials provided via email when their account is created.

![Screenshot: Login Page](./assets/auth/login_page.png)

#### 🛠️ Feature Roadmap

Currently, there is no "Forgot Password" feature implemented. A password recovery system is a feature I would add in future iterations to improve user experience.

#### 🧠 Design Choice: No Public User Registration

Public self-registration is intentionally **not** supported. This is a deliberate design choice because:

- The system is intended to be used within organizations.
- New users must be linked to a pre-existing Person object, which cannot be guaranteed via open registration.
- Creating users manually ensures proper permissions and relationships (e.g., manager assignments).

Users are created via the **Security → Users → Create User** interface.  
👉 [See: Creating a User](#-creating-a-user-and-sending-login-credentials)

#### 🏗️ Future Support: Multi-Tenancy

A feature I would like to implement in the future is **multi-tenancy**, which would allow different clients to sign up and receive isolated environments (separate databases or schemas for each client). This would enable secure and scalable use of public sign-up without risking data overlap or security breaches.

I've researched the [`django-tenants`](https://github.com/django-tenants/django-tenants) package, which supports schema-based tenant isolation for PostgreSQL. While I didn't have time to implement this during the current build, I understand the pattern and it is on the roadmap for scaling the application to support self-service client onboarding.

---

## 🧩 Dashboard

The **Dashboard** serves as the homepage of the application and provides a quick overview tailored to the logged-in user’s role.

### 👤 What the Dashboard Displays

- **Your Details:** Basic information about the logged-in user.
- **Your Contract Information:** If the user is linked to a contract, it will be displayed here.
- **Employees & Contracts Widgets:**
  - **Admin Users:** See all employees and contracts.
  - **Manager Users:** See only employees assigned to them (i.e., where they are listed as the manager).
  - **Employee Users:** Only see their own information.

Each section of the dashboard links to relevant features like viewing, editing, or deleting records, using the same interface structure as the main “View” pages. These widgets are designed for quick access but mirror the full functionality of their respective views.

**📸 Screenshot:**  
![Dashboard](./assets/dashboard/admin_dashboard.png)

---

### 📱 Responsive Design & Navigation

- The **sidebar** contains the main navigation and is **collapsible**.
- The **top navigation bar** includes logout functionality and remains present on all pages.
- On smaller screens, the sidebar is intended to collapse and be toggled via a menu icon.
  > ⚠️ *Currently, on some smaller screens, the sidebar menu does not respond when toggled. This is a known issue and will be addressed in future updates.*

---

### 🔮 Future Plans

- **Modular Dashboard Layout:**
  - Admins will be able to configure which widgets appear for each user role.
  - Users may eventually be able to personalize their own dashboard (e.g., show/hide certain widgets).
- **More Widgets as Features Expand:**
  - As features such as payroll, time tracking, and performance reviews are added, additional widgets will be introduced.
- **Improved Visual Design:**
  - Further emphasis will be placed on distinguishing between widgets and full-page forms through consistent use of styling (e.g., background color, borders, and layout positioning).

## 👥 People Management Feature

This section outlines how to manage people in the system. You will need the appropriate **people permissions** assigned to your user to access these features.

### 📋 View All People

- Navigate to **People Management > View People** in the sidebar.
- You'll see a list of all people in the system, showing names, emails, roles, and contract status.
- You can filter by:
  - **Active** or **Inactive**
  - **Role type** (if implemented in filtering)
- Each row includes options to **view**, **edit**, or **delete** that person.

**📸 Screenshot:**  
![View All People](./assets/people_management/people/person_list.png)

### 🔍 View Individual Person

- Click **View** next to a person in the list.
- Displays full details, including name, contact info, role, assigned manager, and any associated contracts.

**📸 Screenshot:**  
![View Individual Person](./assets/people_management/people/person_details.png)

### ✏️ Edit Person

- Click **Edit** next to a person.
- Update fields such as:
  - First name, last name
  - Email
  - Phone number
  - Date of birth
  - Assigned manager
  - Role

**📸 Screenshot:**  
![Edit Person](./assets/people_management/people/person_update.png)

### ➕ Create Person

- Go to **People Management > Create Person**
- Fill in the form with:
  - Basic details (first name, last name, etc.)
  - Select a manager (optional)
  - Set the person’s role (Employee, Manager, or HR Admin)
- Click **Save** to create the person record.

**📸 Screenshot:**  
![Create Person](./assets/people_management/people/person_create.png)

### ❌ Delete Person

- Click **Delete** next to a person entry.
- Deleting a person may affect contracts to be void and user accounts may still work.
- To offboard a person please end a contract then when they no longer need access to the system their account can be removed.

**📸 Screenshot:**  
![Delete Person](./assets/people_management/people/person_delete.png)

---

## 📄 Contracts Management Feature

This section explains how to manage contracts in the system. You must have appropriate **contract permissions** to access these options.

### 📋 View All Contracts

- Navigate to **Contract Management > View Contracts**.
- Displays a list of all contracts in the system.
- Columns typically include:
  - Person name
  - Job title
  - Start and end dates
  - Hourly rate
  - Contracted hours
- You can **filter** contracts by the person they’re assigned to.

**📸 Screenshot:**  
![View All Contracts](./assets/people_management/contracts/contract_list.png)

### 🔍 View Individual Contract

- Click **View** next to a contract in the list.
- Shows full details of the contract including:
  - Person assigned
  - Job title
  - Start and end dates
  - Hourly rate
  - Contracted hours

**📸 Screenshot:**  
![View Individual Contract](./assets/people_management/contracts/contract_view.png)

### ✏️ Edit Contract

- Click **Edit** next to a contract in the list.
- Fields that can be updated:
  - Assigned person (dropdown of existing people)
  - Job title (text input)
  - Contract start and end dates
  - Hourly rate (decimal)
  - Contracted hours per week

**📸 Screenshot:**  
![Update Contract](./assets/people_management/contracts/contract_update.png)

### ➕ Create Contract

- Go to **Contract Management > Create Contract**
- Required fields:
  - **Person**: Dropdown of existing people (a person may have multiple contracts).
  - **Job Title**: Free-text job title.
  - **Contract Start Date**: Required. This activates the person if it’s their only contract.
  - **Contract End Date**: Optional. When reached, it will deactivate the person if no active contracts remain.
  - **Hourly Rate**: Decimal input (e.g. 12.45).
  - **Contracted Hours**: Number of hours per week (e.g. 40.0).
- Click **Save** to create the contract.

**📸 Screenshot:**  
![Create a Contract](./assets/people_management/contracts/contract_create.png)

### ❌ Delete Contract

- Click **Delete** next to a contract entry.
- Deleting a contract may affect the employee's active status if it was their only active contract.

**📸 Screenshot:**  
![Delete a Contract](./assets/people_management/contracts/contract_delete.png)

---

## 🔐 User Management Feature

The **User Management** section allows administrators to manage authentication accounts for people in the system. Access to this section requires the relevant **user permissions**.

### 👁️ View Users

- Navigate to **Security > Users**.
- This page displays all registered Django users.
- Each entry shows:
  - **Username**
  - **Linked Person** (the person profile it is associated with)
  - **Email Address** (used for login and system emails)
- You can also use the “Add New User” button at the bottom of the page.

**📸 Screenshot:**  
![View All Users](./assets/security/users/user_list.png)

### 🔍 View Individual User

- Click **View** next to a User in the list.
- Shows full details of the User including:
  - First Name
  - Last Name
  - Email
  - User Name
  - Active Status

**📸 Screenshot:**  
![View Individual Contract](./assets/security/users/user_view.png)

### ✏️ Edit User

- Click **Edit** beside a user entry.
- You can update:
  - **Username** (used to log in)
  - **Email Address** (used for correspondence and login)
  - **Permission Groups** (assign one or more permission groups such as Manager, HR Admin, or Employee)
- Note: You cannot change the password from this screen.
- Changing the assigned group will change the user's access levels throughout the application.

**📸 Screenshot:**  
![Edit User](./assets/security/users/user_edit.png)

### ➕ Create User

- Go to **User > Create Contract**
- Required fields:
  - **Username**: Create a Username for the employee.
  - **Email Address**: Ensure Email Adress is the same as the persons Email will sync afterwards.
  - **Select Employee**: Dropdown appears to select an person from a list of people not yet synced with user accounts.
  - **Assign Permission Group**: Give the employee a permission group which will allow them to see an or action on crud functionality.

- Click **Save** to create the user.

**📸 Screenshot:**  
![Create a User](./assets/security/users/user_create.png)

### 🗑️ Delete User

- Click **Delete** beside a user entry.
- This will remove the user's account and revoke their system access.
- The linked person profile will remain intact but will no longer be tied to a login.

**📸 Screenshot:**  
![Delete User](./assets/security/users/user_delete.png)

---

## 👥 Groups & Permissions Management

The **Groups** section allows you to manage permission groupings that control what each user can see and do in the system. Users must belong to a group to access key functionality.

### 👁️ View Groups

- Navigate to **Security > Groups**.
- This page lists all existing permission groups.
- Each group shows its name and assigned permissions.
- From this screen, you can:
  - Click **Edit** to modify group permissions
  - Click **Delete** to remove the group
  - Click **Add New Group** to create a new one

**📸 Screenshot:**  
![View All Groups](./assets/security/groups/groups_view.png)

### 🔍 View Individual Group

- Click **View** next to a Group in the list.
- Shows full details of the Group including:
  - The name of the Group
  - All permissions assigned to the group

**📸 Screenshot:**  
![View Individual Contract](./assets/security/users/user_view.png)

### ✏️ Edit Group

- Click **Edit** on any group to change its permissions.
- Toggle on/off individual permissions to update what this group can do.
- Save changes to apply them immediately to all users assigned to the group.

**📸 Screenshot:**  
![Edit Group](./assets/security/groups/group_update.png)

### ➕ Create Group

- Click **Create Group** from the sidebar or use the “Add New Group” button.
- To create a group:
  - Provide a **Group Name**
  - Toggle on all the **permissions** you want the group to have
- Once submitted, the group becomes selectable when creating or editing a user.

**📸 Screenshot:**  
![Create Group](./assets/security/groups/group_create.png)


### 🗑️ Delete Group

- Click **Delete** on any group to remove it from the system.
- ⚠️ **Warning:** Deleting critical groups (e.g. Admin) can break access to the security section or dashboard functionality.
- If an admin group is deleted and no one has security permissions, the system may require **manual intervention** to restore access.

**📸 Screenshot:**  
![Delete Group](./assets/security/groups/group_delete.png)

### 💡 Notes on Group Usage

- Each **user can currently be assigned only one group**.
- If a user needs a combination of permissions from multiple groups, create a **custom group** containing the required permissions.
- Groups serve as containers for permissions — they do not hold business logic but control view access and functional availability.

### 🛠️ Future Improvements

1. **Multiple Group Assignments:**  
   Support assigning more than one group per user, allowing more flexible permission combinations.

2. **Undeletable Groups:**  
   Core groups like “Admin” could be made undeletable to prevent accidental lockout from security-critical functions.

3. **Permission Search & Filters:**  
   Add a **search bar** and **filter options** to the permission toggles list when creating/editing a group to improve usability.

4. **Fail-Safe Admin Recovery:**  
   Implement a built-in recovery flow or fallback user to regain admin access if all security permissions are lost.

---

### 📩 Creating a User and Sending Login Credentials

The application allows HR Admins or users with the correct permission to create new employees and send them login credentials via email.

### 🔐 Prerequisite:
You must have the **`security.add_user`** permission (or be in a group that includes it) to access the “Users” section.

### 👣 Steps to Create a User

1. **Open the sidebar navigation.**
2. Go to **People > Create Person**.
3. Fill in the employee's details.
   - Use a valid **email address**. This will be used to send login credentials.
4. Submit the form.

### 👥 Link a Django User Account

1. In the sidebar, go to **Security > Users**.
2. Click **Add User**.
3. Fill in the following:
   - **Username:** Any name you want.
   - **Email:** Use the *same email* as the Person entry (for clarity — technically it will sync anyway).
   - **Select Employee:** Only employees without a user account will appear here.
   - **Assign Group(s):** Choose one or more permission groups (e.g., `hr_admin`, `manager`, `employee`, or any custom group).
4. Click **Save**.

### 📧 What Happens Next

- An email is automatically sent to the user (SMTP is pre-configured).
- The email includes:
  - Their **username**
  - Their **password**
- The user can now log in at `/accounts/login/`.

---

## Technologies Used

### **Languages & Frameworks**

-    **Backend:** Django (Python)
-    **Frontend:** Django Templates, HTML, CSS
-    **Database:** SQLite (for development), PostgreSQL (for production)
-    **Version Control:** Git & GitHub
-    **Deployment:** (To be added - Heroku, Railway, or other cloud platforms)

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
