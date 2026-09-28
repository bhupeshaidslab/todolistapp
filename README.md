# TaskFlow

Small Todo app built for Ubuntu using:

- HTML
- CSS
- JavaScript
- Python / Django
- PostgreSQL

## Features

- Register
- Login / Logout
- Add task
- Edit task
- Delete task
- Mark task complete / incomplete
- Each user only sees their own tasks
- Responsive UI

## Ubuntu setup

### 1. Install system packages

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip postgresql postgresql-contrib
```

### 2. Create PostgreSQL database

```bash
sudo -u postgres psql
```

Then run:

```sql
CREATE DATABASE todo_db;
CREATE USER todo_user WITH PASSWORD 'todo_password';
GRANT ALL PRIVILEGES ON DATABASE todo_db TO todo_user;
\c todo_db
GRANT ALL ON SCHEMA public TO todo_user;
\q
```

### 3. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python packages

```bash
pip install -r requirements.txt
```

### 5. Configure environment

```bash
cp .env.example .env
```

Edit `.env` if your PostgreSQL credentials are different.

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Run

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Admin

Optional:

```bash
python manage.py createsuperuser
```

Then visit:

```text
http://127.0.0.1:8000/admin/
```

## Notes

This project intentionally stays small. It does not include categories, reminders, APIs, dark mode, social login, or advanced filtering.
