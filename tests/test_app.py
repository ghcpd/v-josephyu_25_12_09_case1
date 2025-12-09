import os
import tempfile

import pytest
import sys
import os

# Ensure project root is on sys.path so tests can import app, models
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app, init_db
from models import get_connection, User


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary sqlite file for tests
    db_file = str(tmp_path / 'test_db.sqlite3')
    app.config['DATABASE'] = db_file
    app.config['WTF_CSRF_ENABLED'] = False
    init_db(app)
    with app.test_client() as c:
        yield c


def test_model_create_and_retrieve(tmp_path):
    db_file = str(tmp_path / 'test_db.sqlite3')
    app.config['DATABASE'] = db_file
    init_db(app)
    conn = get_connection(app)
    u = User.create(conn, 'alice', 'secret123', 'alice@example.com')
    assert u.id is not None

    fetched = User.get_by_username(conn, 'alice')
    assert fetched is not None
    assert fetched.username == 'alice'
    assert fetched.verify_password('secret123')
    conn.close()


def test_register_and_login_flow(client):
    # Register
    resp = client.post('/register', data={
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'password123'
    }, follow_redirects=False)

    # On success the code redirects to /dashboard
    assert resp.status_code in (302, 303)

    # Login using the same credentials
    resp2 = client.post('/login', data={
        'username': 'bob',
        'password': 'password123'
    }, follow_redirects=True)

    # After login, dashboard should be accessible and show username
    assert resp2.status_code == 200
    assert b'You are logged in.' in resp2.data
    assert b'bob' in resp2.data


def test_register_password_too_short(client):
    # password length in code requires min 6; README says 3
    resp = client.post('/register', data={
        'username': 'shortpass',
        'email': 'short@example.com',
        'password': 'abc'
    }, follow_redirects=True)
    # Should not accept the short password — form should reject
    assert b'Field must be between 6 and 128 characters long.' in resp.data


def test_register_missing_email(client):
    # email field in form is required in code though README says optional
    resp = client.post('/register', data={
        'username': 'noemail',
        'email': '',
        'password': 'password123'
    }, follow_redirects=True)
    assert b'This field is required' in resp.data


def test_profile_route_missing(client):
    r = client.get('/profile')
    assert r.status_code == 404
