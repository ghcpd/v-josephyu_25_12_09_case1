# Corrected README — Flask User Login & Registration App

This document corrects and clarifies the original README so that commands run as documented.

Prerequisites
- Python 3.10+
- pip
- Recommended: virtual environment

Quick start (Windows PowerShell)

1) Create a virtual environment and install deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Start the app

Because the app entrypoint (app.py) uses app.run() directly, passing `--host`/`--port` to `python app.py` will be ignored. Use the flask CLI (recommended) to control host/port, or set environment variables.

Recommended command (works cross-platform):

Windows PowerShell
```powershell
$env:FLASK_APP = 'app.py'
$env:FLASK_ENV = 'development'
flask run --host=0.0.0.0 --port=8080
```

Linux / macOS / Bash
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8080
```

After start, the app will be reachable at the host/port you specified (e.g. `http://127.0.0.1:8080/`).

Notes on configuration
- SECRET_KEY: `app.config['SECRET_KEY']` is used for sessions and CSRF.
- Database: By default the project uses `app.config['DATABASE'] = 'app.db'` located at the project root — not `data/database.sqlite3`.
- Session backend: The project uses Flask's default session mechanism (client-side cookie with secure signing). There is no Redis backend configured in this codebase.

Routes
- GET / — root; redirects to `/dashboard` if authenticated, otherwise to `/login`.
- GET /register — form to register a new user
- POST /register — create user (username and email must be unique)
- GET /login — form to login
- POST /login — authenticate
- GET /logout — log out current user
- GET /dashboard — protected page (requires login)

Form validation
- The registration form requires `email` and enforces a minimum password length of 6 characters. This differs from earlier text that indicated email optional and password length 3.

Testing
- Run tests with:

Windows PowerShell
```powershell
.\.venv\Scripts\Activate.ps1
.venv\Scripts\pytest -q
```

Bash
```bash
source .venv/bin/activate
.venv/bin/pytest -q
```

If you want to adapt the code to accept command-line host/port flags or to change the database location, edit app.py accordingly.
