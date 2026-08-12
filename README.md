# TaskFlow – Personal To-Do Task Manager

TaskFlow is a beginner-friendly full-stack task management application built with Flask, SQLite, SQLAlchemy, and Flask-Login.

## Features

- User registration and login
- Secure password hashing
- Personal task isolation
- Add, edit, delete and complete tasks
- Pending, In Progress and Completed statuses
- Low, Medium and High priorities
- College, Personal, Work and Other categories
- Due dates and automatic overdue detection
- Search, filtering and sorting
- Dashboard statistics
- Completion percentage
- User profile
- Responsive design
- Light/dark theme with localStorage
- REST-style JSON endpoints for task operations

## Technologies

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- HTML5
- CSS3
- JavaScript

## Project Structure

```text
taskflow/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── task.py
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   └── tasks.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── tasks.html
│   └── edit_task.html
├── static/
│   ├── css/style.css
│   └── js/script.js
└── instance/
    └── taskflow.db
```

## Installation

### 1. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

The database and `instance` directory are created automatically.

Open:

http://127.0.0.1:5000

## Database

SQLite is used by default. The database file is:

```text
instance/taskflow.db
```

Tables are automatically created when the application starts.

## API Endpoints

- `POST /register`
- `POST /login`
- `GET /logout`
- `GET /dashboard`
- `GET /profile`
- `GET /tasks`
- `POST /tasks`
- `PUT /tasks/<id>`
- `DELETE /tasks/<id>`
- `PATCH /tasks/<id>/status`

## Testing

1. Register a new user.
2. Log in.
3. Create tasks with different priorities and categories.
4. Test editing and deleting.
5. Change task status.
6. Create an old due date to test overdue detection.
7. Try filters and search.
8. Log out and verify protected pages require authentication.
9. Create a second account and verify users cannot see each other's tasks.
10. Test the theme toggle.

## Screenshots

Add screenshots here after running the application.

## Future Improvements

- Email reminders
- Password reset
- Calendar view
- Drag-and-drop task ordering
- Recurring tasks
- Export tasks to CSV/PDF
- Cloud deployment
- CSRF protection with Flask-WTF
- Automated unit and integration tests
