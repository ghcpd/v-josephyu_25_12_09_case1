# Flask User Login & Registration App (Corrected)

This corrected README documents the behavior of the current implementation and provides commands that work as-is.

## 1. Requirements
- Python 3.10+
- `pip` installed
- Recommended: a virtual environment to isolate dependencies

## 2. Project Structure
(unchanged)

## 3. Installation & Run (Windows PowerShell examples)

### 3.1 Create and Activate Virtual Environment (Windows PowerShell)

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
 .\.venv\Scripts\Activate.ps1
```

### 3.2 Install Dependencies

Preferred: use `requirements.txt`:

```powershell
pip install -r requirements.txt
```

### 3.3 Start the App

The current implementation calls `app.run(debug=True)` when executed directly. By default it binds to `127.0.0.1:5000`.

To use a custom host/port, either call `app.run(host='0.0.0.0', port=8080)` in code or use the `flask` CLI:

```powershell
# Set FLASK_APP and run
$env:FLASK_APP = 'app.py'
flask run --host=0.0.0.0 --port=8080
```

Open in your browser:
- Root (auto-redirect): `http://127.0.0.1:5000/`
- Login page: `http://127.0.0.1:5000/login`
- Register page: `http://127.0.0.1:5000/register`

## 4. Configuration

### 4.1 Secret Key
The current app sets `app.config['SECRET_KEY']` to a static placeholder value. For production, set the secret from an environment variable and avoid hardcoding it.

Example (recommended):
```python
import os
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'replace-with-a-strong-secret-key')
```

### 4.2 Database
The project currently uses a SQLite database file `app.db` at the project root by default. You can override this by setting `app.config['DATABASE']`.

### 4.3 Sessions & Login
The current implementation uses Flask-Login and standard Flask session cookies. There is no Redis session backend or SESSIONLESS_MODE implemented.

## 5. Routes & Behavior
(Updated summary matching implementation)
- `/` (root): Redirects to `/dashboard` when authenticated, otherwise to `/login`.
- `/dashboard`: login-protected homepage
- `/register`: registration page (GET / POST). Email is required by the current implementation.
- `/login`: login page (GET / POST)
- `/logout`: logout

Note: There is no `/profile` route in the current code.

## 6. Forms and Validation Rules

### 6.1 Registration (`/register`)
Current validators:
- `username`: required, 3–32 characters
- `email`: required, must be valid email format
- `password`: required, minimum length 6 (development setting)

### 6.2 Login (`/login`)
- `username`, `password`: standard validators (password min length 6 enforced by the form)

## 7. Data Model & Persistence
(unchanged, but note email column exists and is required by the schema)

---

## Testing
A test suite using pytest is included under `tests/` (and a short smoke test under `test_files/`). Run the tests with:

```powershell
# Activate the virtualenv and run pytest
.\.venv\Scripts\Activate.ps1
pytest -q
```

Or on Unix:
```bash
source .venv/bin/activate
pytest -q
```

---

If you prefer the README to describe a different (corrected) intended behavior (for example, make email optional and set min password length to 3), change the implementation accordingly or open a PR with those code changes.
