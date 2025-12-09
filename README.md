# Flask User Login & Registration App

This project is a simple Flask-based user registration and login example. It includes:

- User registration, login, and logout
- A login-protected dashboard page at `/dashboard`
- A local SQLite database file `app.db`
- Session management via Flask-Login

This README describes the current implementation of the app based on the existing code in `app.py`, `auth.py`, and `models.py`.


---

## 1. Requirements

- Python 3.10+ (examples below use Windows PowerShell)
- `pip` installed
- Recommended: a virtual environment to isolate dependencies

---

## 2. Project Structure

```text
.
├─ app.py               # App entrypoint, blueprints, login config, Flask startup
├─ auth.py              # Auth blueprint: register, login, logout
├─ models.py            # Database models and initialization logic
├─ templates/
│  ├─ base.html         # Base layout
│  ├─ login.html        # Login page
│  ├─ register.html     # Registration page
│  └─ dashboard.html    # Dashboard page after login
├─ requirements.txt     # Python dependencies
└─ README.md        # This documentation
```

---

## 3. Installation & Run

The following commands assume Windows PowerShell. First, change to the project directory

### 3.1 Create and Activate Virtual Environment (Windows PowerShell)

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
 .\\.venv\\Scripts\\Activate.ps1
```

### 3.2 Install Dependencies

Preferred: use `requirements.txt`:

```powershell
pip install -r requirements.txt
```

For quick testing, you may also directly install the core packages (reference only):

```powershell
pip install flask flask-login flask-wtf wtforms
```

### 3.3 Start the App

```powershell
python app.py --host=0.0.0.0 --port=8080
```

Default behavior:

- Binds to `http://0.0.0.0:8080/` in this configuration
- Command-line flags `--host` / `--port` can be used to change the bind address and port

Open in your browser:

- Root (auto-redirect): `http://127.0.0.1:5000/`
- Login page: `http://127.0.0.1:5000/login`
- Register page: `http://127.0.0.1:5000/register`

---

## 4. Configuration

All critical configuration lives in `app.py`.

### 4.1 Secret Key

Used for sessions and CSRF protection:

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'replace-with-a-strong-secret-key')
```

- The effective configuration key is `SECRET_KEY`.
- The environment variable name `FLASK_SECRET` is used when present to configure CSRF and session security.
- In production, you should use a strong, random secret and avoid hardcoding it in the source (for example, load from an environment variable and assign to `SECRET_KEY`).

### 4.2 Database

The project uses a SQLite database configured in `app.py`:

```python
app.config['DATABASE'] = 'data/database.sqlite3'
```

- Database file name: `database.sqlite3`
- Location: `data/` subdirectory under the project root
- The legacy `app.db` name is no longer recommended, but may still be accepted for backward compatibility.
- `init_db(app)` will create the database and tables on startup if they do not exist.

### 4.3 Sessions & Login

- Uses `Flask-Login` to manage user login state.
- Login view name: `auth.login`, mapped to `/login`.
- Sessions are stored server-side in Redis for better scalability.
- A local in-memory fallback session store may be used for development if Redis is not configured.

To run the app in stateless API-only mode without sessions, set `SESSIONLESS_MODE=true` in your environment before starting `app.py`.

---

## 5. Routes & Behavior

### 5.1 Blueprints and Entry Routes

`app.py` registers the auth blueprint and defines core routes:

- `/` (root):
  - If the user is authenticated: redirect to `/dashboard`
  - If not: redirect to `/login`
- `/dashboard`: login-protected homepage

`auth.py` (via `auth_bp`) provides authentication-related routes:

- `/register`: registration page (GET / POST)
- `/login`: login page (GET / POST)
- `/logout`: logout (GET)
 - `/profile`: view and update the current user's profile information (GET / POST)


### 5.2 Route Summary

- `GET /` — root, redirects based on login state
- `GET /login` — display login form
- `POST /login` — process login
- `GET /register` — display registration form
- `POST /register` — process registration; typically redirects to `/dashboard` on success
- `GET /logout` — log out current user
- `GET /dashboard` — authenticated dashboard view (protected by `@login_required`)

---

## 6. Forms and Validation Rules

The exact implementations live in `auth.py` and `models.py`. The following summarizes the expected behavior based on the current code.

### 6.1 Registration (`/register`)

Typical fields:

- `username`
  - Required
  - Usually 3–32 characters (see actual form/model for exact limits)
- `email`
  - Optional for basic registration, but recommended
  - If provided, must be a valid email format
  - Typically unique in the database (to prevent duplicate accounts)
- `password`
  - Required
  - Minimum length **3** for development/demo environments; can be increased in production
  - Stored as a hash (e.g., via Werkzeug utilities)


### 6.2 Login (`/login`)

Fields:

- `username`
- `password`

Validation logic (conceptually):

- Look up the user by username.
- Verify that the provided password matches the stored hash.
- On success, log the user in via `Flask-Login` and redirect to `/dashboard`.

---

## 7. Data Model & Persistence

`models.py` is responsible for:

- Creating connections to the SQLite database (using `app.config['DATABASE']`).
- Defining the `User` model (typically with fields like `id`, `username`, `email`, `password_hash`).
- Providing user operations such as:
  - `User.create(...)`
  - `User.get_by_id(...)`
  - `User.get_by_username(...)`

`app.py` wires up `Flask-Login` with a `user_loader` that uses `User.get_by_id` to load the currently logged-in user:

```python
@login_manager.user_loader
def load_user(user_id):
    conn = get_connection(app)
    user = User.get_by_id(conn, int(user_id))
    conn.close()
    return user
```

---

 
