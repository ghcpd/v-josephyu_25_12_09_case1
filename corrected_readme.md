# Flask User Login & Registration App (corrected)

This corrected documentation reflects the *actual* behavior of the project code (after small fixes to make CLI flags and environment configuration work as expected).

Important: this is the authoritative README for running and testing this repository.

---

## Requirements

- Python 3.10+
- pip
- A virtual environment is recommended

---

## Project layout

The repository includes:

```
.\
├─ app.py               # App entrypoint, blueprints, login config, and app startup
├─ auth.py              # Auth blueprint and form logic
├─ models.py            # Database models and initialization logic
├─ templates/           # HTML templates
├─ requirements.txt     # Pinned Python dependencies
├─ tests/               # pytest test suite
└─ README.md            # Original documentation (this file is corrected_readme.md)
```

---

## 1. Setup (PowerShell / Bash)

Create and activate a virtual environment and install dependencies.

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Bash / macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Running the App

This app now supports reading configuration from environment variables and accepts --host and --port flags at runtime.

Configuration points
- SECRET_KEY: read from the environment variable `FLASK_SECRET` when present; otherwise a fallback hardcoded value is used (development only).
- DATABASE: path to the sqlite file. Default: `data/database.sqlite3`. You can set the DATABASE environment variable to override.

Start the app (PowerShell example):

```powershell
# use the CLI flags --host and --port
python app.py --host=0.0.0.0 --port=8080

# or use defaults (127.0.0.1:5000)
python app.py
```

Environment example (Windows PowerShell):

```powershell
$env:FLASK_SECRET = 'a-long-random-secret'
$env:DATABASE = 'data/database.sqlite3'
python app.py --host=0.0.0.0 --port=8080
```

Open in browser:

- Root: http://127.0.0.1:5000/ (or the host:port you provided)
- Login page: http://127.0.0.1:5000/login
- Register page: http://127.0.0.1:5000/register

---

## 3. Routes (actual implemented)

- GET / — root: redirects to `/dashboard` if authenticated or `/login` when not
- GET /login — show login form
- POST /login — process login
- GET /register — show registration form
- POST /register — process register
- GET /logout — log out user
- GET /dashboard — login_required dashboard

Note: There is no `/profile` route in the current implementation.

---

## 4. Validation and Forms

- Registration: `username` (required), `email` (required), `password` (required)
- Password minimum length is 6 characters (WTForms validators in `auth.py`)

If you need different constraints (e.g., make email optional or reduce min password length) change `auth.py` and the DB schema accordingly.

---

## 5. Database & persistence

- Default file: `data/database.sqlite3` (created on first run)
- You can override by setting the `DATABASE` environment variable.

Notes on migrations: `models.init_db` will attempt to add an `email` column if missing but this is a simple migration and may leave NULL values in older rows — proceed carefully in production.

---

## 6. Tests

Run the pytest test-suite:

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pytest -q
```

Bash:

```bash
source .venv/bin/activate
pytest -q
```

All tests should pass after following the setup steps.

---

If you want to change behavior (for example enabling Redis sessions), you'll need to modify `app.py` to register a server-side session store and add configuration points accordingly.
