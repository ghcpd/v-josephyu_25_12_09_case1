from app import app
from models import init_db
import tempfile
import os


def setup_app():
    db_fd, db_path = tempfile.mkstemp(prefix='tf_', suffix='.db')
    os.close(db_fd)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DATABASE'] = db_path
    init_db(app)
    return app


def test_root_redirects():
    a = setup_app()
    client = a.test_client()
    rv = client.get('/')
    assert rv.status_code == 302


def test_profile_missing():
    a = setup_app()
    client = a.test_client()
    rv = client.get('/profile')
    assert rv.status_code == 404


def test_password_min_msg():
    a = setup_app()
    client = a.test_client()
    rv = client.post('/register', data={'username':'short','password':'123','email':'a@b.c'}, follow_redirects=True)
    assert b'Field must be between' in rv.data
