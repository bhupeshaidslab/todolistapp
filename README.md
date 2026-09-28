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

This project intentionally stays small. It does not include APIs, social login, or advanced enterprise features.

## Deploy on Render

### Option A — Blueprint (`render.yaml`)

1. Push this repo to GitHub.
2. In [Render](https://render.com): **New** → **Blueprint** → connect the repo.
3. Render creates a **Web Service** and **PostgreSQL** database and wires `DATABASE_URL` automatically.
4. After deploy, open your `*.onrender.com` URL and register a user.

### Option B — Manual web service

1. **New** → **PostgreSQL** (free). Copy the **Internal Database URL**.
2. **New** → **Web Service** → connect the same GitHub repo.
3. Settings:

| Setting | Value |
|--------|--------|
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |
| **Python version** | `3.12.8` (Environment → `PYTHON_VERSION`) |

4. **Environment variables**:

| Key | Value |
|-----|--------|
| `DEBUG` | `false` |
| `SECRET_KEY` | long random string (Generate in Render) |
| `DATABASE_URL` | Internal Database URL from step 1 |
| `ALLOWED_HOSTS` | `your-service.onrender.com,.onrender.com` |

Render also sets `RENDER_EXTERNAL_HOSTNAME` for CSRF automatically.

5. Deploy. Migrations run during `./build.sh`.

### After deploy

```bash
# Optional: create admin user (Render Shell on the web service)
python manage.py createsuperuser
```

Static files are served via **WhiteNoise** (`collectstatic` runs in `build.sh`).
