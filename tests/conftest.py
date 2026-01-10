import os
import sys
import tempfile
import pytest
# Ensure project root is on PYTHONPATH so imports like 'app' work when running pytest from tests/
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app as flask_app
from models import init_db

@pytest.fixture
def app():
    # Use a temporary database file for isolation
    db_fd, db_path = tempfile.mkstemp(prefix='test_', suffix='.db')
    os.close(db_fd)
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False  # disable CSRF for functional tests
    flask_app.config['DATABASE'] = db_path
    # Initialize fresh DB
    init_db(flask_app)

    yield flask_app

    # Teardown
    try:
        os.remove(db_path)
    except OSError:
        pass

@pytest.fixture
def client(app):
    return app.test_client()
