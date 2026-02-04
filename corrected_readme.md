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
python app.py
```

Default behavior:

- Binds to `http://127.0.0.1:5000/` in development mode
- Command-line flags are not supported; modify code for custom host/port

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
app.config['SECRET_KEY'] = 'replace-with-a-strong-secret-key'
```

- The effective configuration key is `SECRET_KEY`.
- The secret is currently hardcoded; in production, replace with a strong, random secret.

### 4.2 Database

The project uses a SQLite database configured in `app.py`:

```python
app.config['DATABASE'] = 'app.db'
```

- Database file name: `app.db`
- Location: root of the project
- `init_db(app)` will create the database and tables on startup if they do not exist.

### 4.3 Sessions & Login

- Uses `Flask-Login` to manage user login state with default client-side sessions.
- Login view name: `auth.login`, mapped to `/login`.

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

### 5.2 Route Summary

- `GET /` — root, redirects based on login state
- `GET /login` — display login form
- `POST /login` — process login
- `GET /register` — display registration form
- `POST /register` — process registration; redirects to `/dashboard` on success
- `GET /logout` — log out current user
- `GET /dashboard` — authenticated dashboard view (protected by `@login_required`)

---

## 6. Forms and Validation Rules

The exact implementations live in `auth.py` and `models.py`. The following summarizes the expected behavior based on the current code.

### 6.1 Registration (`/register`)

Typical fields:

- `username`
  - Required
  - 3–32 characters
- `email`
  - Required
  - Must be a valid email format
  - Unique in the database
- `password`
  - Required
  - Minimum length 6

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
- Defining the `User` model (with fields like `id`, `username`, `email`, `password_hash`).
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
```</content>
<parameter name="filePath">d:\mins_project\model_test\Documentation & knowledge\1209\grok-fast\corrected_readme.md