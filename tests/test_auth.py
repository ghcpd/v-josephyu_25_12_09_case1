def test_db_path_default(app):
    # The application currently uses 'app.db' by default (README expects data/ path)
    assert app.config['DATABASE'].endswith('.db')


def test_root_redirects_to_login(client):
    rv = client.get('/')
    assert rv.status_code == 302
    assert '/login' in rv.headers['Location']


def test_register_requires_email(client):
    # Post without email - the RegisterForm currently requires email
    rv = client.post('/register', data={'username': 'testuser', 'password': 'secret12', 'email': ''}, follow_redirects=True)
    assert b'This field is required.' in rv.data


def test_password_min_length_enforced(client):
    # Password length validator is set to min=6 in the form
    rv = client.post('/register', data={'username': 'shortpw', 'password': '123', 'email': 'a@example.com'}, follow_redirects=True)
    # WTForms Length validator renders: "Field must be between 6 and 128 characters long."
    assert b'Field must be between 6 and 128 characters long.' in rv.data


def test_profile_route_missing(client):
    # README documents a /profile route, which does not exist in the app
    rv = client.get('/profile')
    assert rv.status_code == 404


def test_register_then_login(client):
    # Happy path: register with valid data, then login and access dashboard
    register = client.post('/register', data={'username': 'jdoe', 'password': 'password123', 'email': 'jdoe@example.com'}, follow_redirects=True)
    # The dashboard template uses 'You are logged in.' and shows username
    assert b'You are logged in.' in register.data

    login = client.post('/login', data={'username': 'jdoe', 'password': 'password123'}, follow_redirects=True)
    assert b'You are logged in.' in login.data
