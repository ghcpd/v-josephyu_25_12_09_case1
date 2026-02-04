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
└─ README.md            # This documentation
```

---

## 3. Installation & Run

The following commands assume Windows PowerShell. First, change to the project directory

### 3.1 Create and Activate Virtual Environment (Windows PowerShell)

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

**Note:** If you encounter an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3.1b Create and Activate Virtual Environment (Linux/macOS Bash)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 3.2 Install Dependencies

Preferred: use `requirements.txt`:

```powershell
pip install -r requirements.txt
```

This installs all required packages including Flask, Flask-Login, Flask-WTF, WTForms, and email-validator.

For reference, the required packages are:
- `Flask==3.0.0`
- `Flask-Login==0.6.3`
- `Flask-WTF==1.2.1`
- `WTForms==3.1.2`
- `Werkzeug==3.0.1`
- `email_validator==2.2.0`
- `pytest` (for testing)

### 3.3 Start the App

To start the Flask development server with default settings:

```powershell
python app.py
```

The app will run on `http://127.0.0.1:5000` by default.

**Debug Mode:** The app runs with `debug=True`, which enables:
- Auto-reload on code changes
- Interactive debugger on errors
- Development server mode

**Note on Command-line Arguments:** The current implementation does not support `--host` and `--port` 
command-line arguments. To change the host and port, modify the `app.run()` call in `app.py` or 
set environment variables.

**Important:** Do NOT use the development server in production. For production deployment, 
use a WSGI server such as Gunicorn, uWSGI, or Waitress.

Open in your browser:

- Root (auto-redirect): `http://127.0.0.1:5000/`
- Login page: `http://127.0.0.1:5000/login`
- Register page: `http://127.0.0.1:5000/register`
- Dashboard (requires login): `http://127.0.0.1:5000/dashboard`

---

## 4. Configuration

All critical configuration lives in `app.py`.

### 4.1 Secret Key

Used for sessions and CSRF protection:

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-with-a-strong-secret-key'
```

**For Production:** Use an environment variable:

```python
import os
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'replace-with-a-strong-secret-key')
```

Then set the environment variable before running:
```powershell
$env:FLASK_SECRET = 'your-strong-random-secret-key'
python app.py
```

### 4.2 Database

The project uses a SQLite database configured in `app.py`:

```python
app.config['DATABASE'] = 'app.db'
```

- Database file name: `app.db`
- Location: Root directory of the project
- `init_db(app)` creates the database and tables on startup if they do not exist
- The database includes a `users` table with columns: `id`, `username`, `password_hash`, `email`

### 4.3 Sessions & Login

- Uses `Flask-Login` to manage user login state
- Login view name: `auth.login`, mapped to `/login`
- Sessions are stored using Flask's default session mechanism (signed cookies)
- No additional session backend configuration is required
- Session data is secured using the `SECRET_KEY` configuration

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

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Root, redirects based on login state |
| GET | `/login` | Display login form |
| POST | `/login` | Process login submission |
| GET | `/register` | Display registration form |
| POST | `/register` | Process registration; redirects to `/dashboard` on success |
| GET | `/logout` | Log out current user; redirects to `/login` |
| GET | `/dashboard` | Authenticated dashboard view (protected by `@login_required`) |

---

## 6. Forms and Validation Rules

The exact implementations live in `auth.py` and `models.py`. The following summarizes the expected behavior based on the current code.

### 6.1 Registration (`/register`)

Fields and validation:

- `username`
  - Required
  - 3–32 characters (enforced by `Length(min=3, max=32)`)
  - Must be unique (checked against existing users in database)
  
- `email`
  - Required
  - Must be a valid email format (validated by `email_validator`)
  - Must be unique in the database (prevents duplicate accounts)
  
- `password`
  - Required
  - Minimum length **6** characters (enforced by `Length(min=6, max=128)`)
  - Stored as a hash using Werkzeug's `generate_password_hash()`

**Success Behavior:** On successful registration:
- User is created in database
- User is logged in automatically
- User is redirected to `/dashboard`

**Failure Behavior:** If validation fails:
- Form errors are displayed
- User is not created
- User remains on `/register` page

### 6.2 Login (`/login`)

Fields and validation:

- `username`
  - Required
  - 3–32 characters minimum (enforced by `Length(min=3, max=32)`)
  
- `password`
  - Required
  - 6–128 characters (enforced by `Length(min=6, max=128)`)

**Validation Logic:**

1. User submits login form with username and password
2. System looks up the user by username in the database
3. If user exists, system verifies the provided password against the stored hash
4. On success: user is logged in via `Flask-Login` and redirected to `/dashboard`
5. On failure: flash message "Invalid username or password" is displayed
6. User remains on `/login` page to retry

---

## 7. Data Model & Persistence

`models.py` is responsible for:

- Creating connections to the SQLite database (using `app.config['DATABASE']`)
- Defining the `User` model with fields: `id`, `username`, `email`, `password_hash`
- Providing user operations such as:
  - `User.create(conn, username, password, email)` - Creates a new user
  - `User.get_by_id(conn, user_id)` - Retrieves user by ID
  - `User.get_by_username(conn, username)` - Retrieves user by username
  - `User.verify_password(password)` - Validates password against hash

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

## 8. Testing

### 8.1 Running Tests

To run the test suite:

**Windows PowerShell:**
```powershell
# Activate virtual environment first
.\.venv\Scripts\Activate.ps1

# Run tests with pytest
pytest -v
```

**Linux/macOS Bash:**
```bash
# Activate virtual environment first
source .venv/bin/activate

# Run tests with pytest
pytest -v
```

### 8.2 Test Coverage

The test suite (`tests/test_*.py` files) includes:

- **test_registration.py**: Tests user registration with valid and invalid inputs
- **test_login.py**: Tests login functionality and validation
- **test_models.py**: Tests database models and user operations
- **test_auth_forms.py**: Tests form validation

All tests should pass successfully.

---

## 9. Troubleshooting

### Virtual Environment Not Activating

**Error:** `Activate.ps1 cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

### ModuleNotFoundError After Installation

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:** Ensure you have activated the virtual environment:
```powershell
.\.venv\Scripts\Activate.ps1
```

Then verify dependencies are installed:
```powershell
pip install -r requirements.txt
```

### Database Issues

**Issue:** Database is locked or corrupted

**Solution:** Delete the `app.db` file and restart the app:
```powershell
Remove-Item app.db
python app.py
```

The database will be recreated automatically with the proper schema.

### Port Already in Use

**Error:** `Address already in use`

**Solution:** Another process is using port 5000. Either:
1. Close the other application using port 5000
2. Modify `app.py` to use a different port:
   ```python
   if __name__ == '__main__':
       app.run(debug=True, port=5001)  # Use port 5001 instead
   ```

---

## 10. Deployment

For production deployment:

1. Set a strong `FLASK_SECRET` environment variable
2. Use a production WSGI server (Gunicorn, uWSGI, Waitress, etc.)
3. Use HTTPS/SSL certificates
4. Set `debug=False`
5. Use a production-grade database (PostgreSQL, MySQL) instead of SQLite
6. Configure proper error logging and monitoring

Example with Gunicorn:

```powershell
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

---

## 11. Version History

- **v1.0** (December 9, 2025): Initial release with corrected documentation
  - Fixed virtual environment activation path
  - Removed unsupported command-line arguments
  - Corrected database location documentation
  - Fixed password minimum length (6, not 3)
  - Clarified session management (no Redis required)
  - Added missing FLASK_SECRET environment variable support documentation
  - Added email_validator to quick install list

---

## 12. License

This project is provided as-is for educational and demonstration purposes.
