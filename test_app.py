import pytest
from app import app, init_db
from models import get_connection, User
import tempfile
import os

@pytest.fixture
def client():
    # Create a temporary database
    db_fd, db_path = tempfile.mkstemp()
    app.config['DATABASE'] = db_path
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test'

    with app.test_client() as client:
        with app.app_context():
            init_db(app)
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_root_redirects_to_login(client):
    rv = client.get('/')
    assert rv.status_code == 302
    assert '/login' in rv.headers['Location']

def test_register_page(client):
    rv = client.get('/register')
    assert rv.status_code == 200
    assert b'Register' in rv.data

def test_login_page(client):
    rv = client.get('/login')
    assert rv.status_code == 200
    assert b'Login' in rv.data

def test_register_user(client):
    rv = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert b'welcome' in rv.data.lower()

def test_login_user(client):
    # First register
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    # Then login
    rv = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert b'welcome' in rv.data.lower()

def test_dashboard_requires_login(client):
    rv = client.get('/dashboard')
    assert rv.status_code == 302
    assert '/login' in rv.headers['Location']

def test_logout(client):
    # Register and login
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    })
    # Logout
    rv = client.get('/logout', follow_redirects=True)
    assert rv.status_code == 200
    assert b'login' in rv.data.lower()