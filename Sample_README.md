# Flask User Login & Registration App

This project is a simple Flask-based user registration and login example. It includes:

- User registration, login, and logout
- A login-protected dashboard page at `/dashboard`
- A local SQLite database file `app.db`
- Session management via Flask-Login

This README is written against the actual code (`app.py`, `auth.py`, `models.py`) and fixes all known issues described in `sample_defects.txt` and `true_defect.md`.

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
└─ README_new.md        # This documentation
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
``+

### 3.3 Start the App

```powershell
python app.py
```

Default behavior:

- Binds to `http://127.0.0.1:5000/`
- Command-line flags `--host` / `--port` are **not** parsed by `app.py`; they will be ignored if provided

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
- The environment variable name `FLASK_SECRET` mentioned in the old README is **not** used.
- In production, you should use a strong, random secret and avoid hardcoding it in the source (for example, load from an environment variable and assign to `SECRET_KEY`).

### 4.2 Database

The project uses a SQLite database configured in `app.py`:

```python
app.config['DATABASE'] = 'app.db'
```

- Database file name: `app.db`
- Location: project root (same directory as `app.py`)
- The old path `data/database.sqlite3` is no longer used.
- `init_db(app)` will create the database and tables on startup if they do not exist.

### 4.3 Sessions & Login

- Uses `Flask-Login` to manage user login state.
- Login view name: `auth.login`, mapped to `/login`.
- Sessions rely on Flask's default signed cookie mechanism.
- **No Redis or external session store is used**; any mention of Redis in old docs is incorrect.

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

> Notes:
>
> - There is **no** `/signup`, `/signin`, or `/profile` route in the current code.
> - There are **no** `/api/*` JSON endpoints implemented.

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
  - Required
  - Must be a valid email format
  - Typically unique in the database (to prevent duplicate accounts)
- `password`
  - Required
  - Minimum length **6** (the old README's value of 3 is outdated)
  - Stored as a hash (e.g., via Werkzeug utilities)

> Notes:
>
> - The `confirm_password` field mentioned in the old README is **not** present in the current implementation.
> - Email **is required**; the old statement that "Email is optional" is incorrect.

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

## 8. Example Flow: Register and Login

1. Start the app:
   ```powershell
   python app.py
   ```
2. Open `http://127.0.0.1:5000/register` in your browser.
3. Fill out the form:
   - Username (3–32 characters)
   - Valid, unused email address
   - Password (at least 6 characters)
4. Submit the registration form. On success, you should be redirected to `/dashboard`.
5. Use the logout link (points to `/logout`).
6. Visit `/login`, enter the same username and password, and you should again be redirected to `/dashboard` after logging in.

---

## 9. Differences from the Old README

To avoid confusion, this section explicitly lists items from the old README that are **no longer correct** and how they are fixed here.

1. **CLI flags `--host` / `--port`**
   - Old docs: `python app.py --host=0.0.0.0 --port=8080`
   - Reality: `app.py` does not parse CLI arguments and always runs on `127.0.0.1:5000` by default.
   - This README: recommends just running `python app.py` and visiting `http://127.0.0.1:5000/`.

2. **Route names**
   - Old docs: `/signup`, `/signin`, `/profile`
   - Reality: `/register`, `/login`, `/dashboard`
   - This README: uses only the actual routes and lists them in Section 5.

3. **JSON API endpoints**
   - Old docs: `POST /api/register`, `POST /api/login` with JSON bodies using `user` / `pass` / `mail`.
   - Reality: there are no `/api/*` endpoints; the app uses HTML forms with fields `username` / `password` / `email`.
   - This README: clarifies that there is currently no JSON API.

4. **Field requirements**
   - Old docs:
     - Email optional
     - Minimum password length 3
   - Reality:
     - Email required, typically `NOT NULL` and `UNIQUE` in the database.
     - Minimum password length **6**.
   - This README: documents the current field validation rules in Section 6.

5. **Database and session storage**
   - Old docs:
     - Database path: `data/database.sqlite3`
     - Sessions stored in Redis
   - Reality:
     - Database file: `app.db` in the project root.
     - Sessions: Flask's default cookie-based sessions; no Redis dependency.
   - This README: explains the actual configuration in Section 4.

6. **Secret / CSRF configuration**
   - Old docs: suggest using env var `FLASK_SECRET` for Secret/CSRF.
   - Reality:
     - The app uses `app.config['SECRET_KEY']`.
     - It does not read `FLASK_SECRET`.
   - This README: documents `SECRET_KEY` and suggests using an environment variable in production if you extend the code.

---

## 10. Possible Future Extensions

If you plan to build on top of this project, consider:

- Adding a password confirmation field (`confirm_password`).
- Implementing email verification (sending confirmation emails).
- Adding JSON APIs (e.g., `/api/register`, `/api/login`) and wiring them to a frontend client.
- Migrating from SQLite to a more robust database (PostgreSQL / MySQL, etc.).
- Loading sensitive configuration (such as `SECRET_KEY`, database URL) from environment variables.

These features are **not implemented** in the current code. If you add them, make sure to update this README accordingly.
