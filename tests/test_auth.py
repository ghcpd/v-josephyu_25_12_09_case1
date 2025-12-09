import os
import tempfile
import sqlite3
import pytest
import importlib.util
import sys
from pathlib import Path

# Import app module by file path to avoid import issues with spaces in path
proj_root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('app', str(proj_root / 'app.py'))
app_module = importlib.util.module_from_spec(spec)
# Ensure project root is on sys.path for imports inside app.py
sys.path.insert(0, str(proj_root))
spec.loader.exec_module(app_module)
_app = app_module.app

from models import init_db, get_connection

DB_PATH = os.path.join(os.path.dirname(__file__), 'test_app.db')

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Ensure fresh database for tests
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    _app.config['DATABASE'] = DB_PATH
    _app.config['WTF_CSRF_ENABLED'] = False
    init_db(_app)
    yield
    try:
        os.remove(DB_PATH)
    except OSError:
        pass


def register(client, username, email, password):
    return client.post('/register', data={
        'username': username,
        'email': email,
        'password': password,
        'submit': 'Register'
    }, follow_redirects=True)


def login(client, username, password):
    return client.post('/login', data={
        'username': username,
        'password': password,
        'submit': 'Login'
    }, follow_redirects=True)


def test_register_and_login_flow():
    client = _app.test_client()
    rv = register(client, 'alice', 'alice@example.com', 'password123')
    assert b"You are logged in" in rv.data
    # Logout
    client.get('/logout', follow_redirects=True)
    # Login
    rv = login(client, 'alice', 'password123')
    assert b"You are logged in" in rv.data


def test_duplicate_username_shows_error():
    client = _app.test_client()
    rv = register(client, 'bob', 'bob@example.com', 'secret12')
    assert b"You are logged in" in rv.data
    client.get('/logout', follow_redirects=True)
    rv = register(client, 'bob', 'bob2@example.com', 'secret12')
    assert b"Username is already taken" in rv.data


def test_duplicate_email_shows_error():
    client = _app.test_client()
    rv = register(client, 'charlie', 'charlie@example.com', 'passtest')
    assert b"You are logged in" in rv.data
    client.get('/logout', follow_redirects=True)
    rv = register(client, 'charlie2', 'charlie@example.com', 'passtest')
    assert b"Email is already registered" in rv.data


def test_login_with_wrong_password_fails():
    client = _app.test_client()
    register(client, 'dave', 'dave@example.com', 'mypassword')
    client.get('/logout', follow_redirects=True)
    rv = login(client, 'dave', 'wrongpass')
    assert b"Invalid username or password" in rv.data


def test_dashboard_requires_login():
    client = _app.test_client()
    rv = client.get('/dashboard', follow_redirects=False)
    # Should redirect to login (302)
    assert rv.status_code == 302
    assert '/login' in rv.headers['Location']
