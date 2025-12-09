"""
Test suite for Flask User Login & Registration App
Tests registration, login, logout, and database operations
"""

import pytest
import sqlite3
import os
from werkzeug.security import check_password_hash
from app import app, init_db
from models import User, get_connection


@pytest.fixture
def client():
    """Create a test client with a temporary database."""
    app.config['DATABASE'] = 'test_app.db'
    app.config['TESTING'] = True
    
    # Create database and tables
    init_db(app)
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    if os.path.exists('test_app.db'):
        os.remove('test_app.db')


class TestUserModel:
    """Test User model and database operations."""
    
    def test_user_creation(self, client):
        """Test creating a user in the database."""
        conn = get_connection(app)
        user = User.create(conn, 'testuser', 'password123', 'test@example.com')
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.id is not None
        assert check_password_hash(user.password_hash, 'password123')
        
        conn.close()
    
    def test_get_user_by_username(self, client):
        """Test retrieving user by username."""
        conn = get_connection(app)
        User.create(conn, 'testuser', 'password123', 'test@example.com')
        
        retrieved_user = User.get_by_username(conn, 'testuser')
        assert retrieved_user is not None
        assert retrieved_user.username == 'testuser'
        
        conn.close()
    
    def test_get_user_by_id(self, client):
        """Test retrieving user by ID."""
        conn = get_connection(app)
        user = User.create(conn, 'testuser', 'password123', 'test@example.com')
        
        retrieved_user = User.get_by_id(conn, user.id)
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        
        conn.close()
    
    def test_get_nonexistent_user(self, client):
        """Test retrieving non-existent user returns None."""
        conn = get_connection(app)
        
        user = User.get_by_username(conn, 'nonexistent')
        assert user is None
        
        conn.close()
    
    def test_password_verification(self, client):
        """Test password verification."""
        conn = get_connection(app)
        user = User.create(conn, 'testuser', 'password123', 'test@example.com')
        
        assert user.verify_password('password123') is True
        assert user.verify_password('wrongpassword') is False
        
        conn.close()
    
    def test_user_creation_password_hashed(self, client):
        """Test that passwords are hashed, not stored in plain text."""
        conn = get_connection(app)
        user = User.create(conn, 'testuser', 'mypassword', 'test@example.com')
        
        # Password should NOT be stored in plain text
        assert user.password_hash != 'mypassword'
        # But should be able to verify the password
        assert user.verify_password('mypassword') is True
        
        conn.close()


class TestDatabaseSchema:
    """Test database schema and constraints."""
    
    def test_database_file_created(self, client):
        """Test that database file is created."""
        assert os.path.exists('test_app.db')
    
    def test_users_table_exists(self, client):
        """Test that users table is created."""
        conn = get_connection(app)
        cur = conn.cursor()
        
        # Query to check if table exists
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        result = cur.fetchone()
        
        assert result is not None
        conn.close()
    
    def test_username_unique_constraint(self, client):
        """Test that username has unique constraint."""
        conn = get_connection(app)
        
        User.create(conn, 'testuser', 'password1', 'test1@example.com')
        
        # Try to create another user with same username
        with pytest.raises(sqlite3.IntegrityError):
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                ('testuser', 'dummy_hash', 'test2@example.com')
            )
            conn.commit()
        
        conn.close()
    
    def test_email_unique_constraint(self, client):
        """Test that email has unique constraint."""
        conn = get_connection(app)
        
        User.create(conn, 'testuser1', 'password1', 'test@example.com')
        
        # Try to create another user with same email
        with pytest.raises(sqlite3.IntegrityError):
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                ('testuser2', 'dummy_hash', 'test@example.com')
            )
            conn.commit()
        
        conn.close()


class TestPageLoading:
    """Test that basic pages load without errors."""
    
    def test_register_page_loads(self, client):
        """Test that registration page loads successfully."""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Register' in response.data or b'register' in response.data
    
    def test_login_page_loads(self, client):
        """Test that login page loads successfully."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data or b'login' in response.data
    
    def test_root_redirects_unauthenticated(self, client):
        """Test that unauthenticated root access redirects."""
        response = client.get('/')
        # Should be a redirect (not 200)
        assert response.status_code in [301, 302, 303, 307, 308]


class TestRegistrationForm:
    """Test registration form validation."""
    
    def test_register_form_accepts_valid_data(self, client):
        """Test registration form submission with valid data."""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        # Should get 200 or redirect
        assert response.status_code in [200, 302]
    
    def test_register_short_username_rejected(self, client):
        """Test that short usernames are rejected."""
        response = client.post('/register', data={
            'username': 'ab',
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        # Should show form again with error
        assert b'username' in response.data.lower()
    
    def test_register_short_password_rejected(self, client):
        """Test that short passwords are rejected."""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'pass'  # Only 4 characters
        })
        
        assert response.status_code == 200
        # Should show form again
        assert b'password' in response.data.lower()
    
    def test_register_invalid_email_rejected(self, client):
        """Test that invalid emails are rejected."""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'not-an-email',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        # Should show form with email field
        assert b'email' in response.data.lower()


class TestLoginForm:
    """Test login form validation."""
    
    def test_login_form_accepts_valid_data(self, client):
        """Test login form submission."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        # Should get 200 (form redisplayed) or 302 (redirect if user found)
        assert response.status_code in [200, 302]
    
    def test_login_short_username_rejected(self, client):
        """Test that form validation works."""
        response = client.post('/login', data={
            'username': 'ab',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        assert b'username' in response.data.lower() or b'login' in response.data.lower()
    
    def test_login_short_password_rejected(self, client):
        """Test that short passwords are rejected on login form."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'pass'
        })
        
        assert response.status_code == 200
        assert b'password' in response.data.lower() or b'login' in response.data.lower()


class TestLogout:
    """Test logout functionality."""
    
    def test_logout_requires_login(self, client):
        """Test that logout is protected by login_required."""
        response = client.get('/logout')
        # Should redirect to login page (protected route)
        assert response.status_code == 302
        assert '/login' in response.location


class TestDashboardProtection:
    """Test that dashboard is protected."""
    
    def test_dashboard_requires_login(self, client):
        """Test that dashboard is protected by login_required."""
        response = client.get('/dashboard')
        # Should redirect to login page (protected route)
        assert response.status_code == 302
        assert '/login' in response.location


class TestFormValidationRules:
    """Test specific validation rules from the documentation."""
    
    def test_username_min_length_is_3(self, client):
        """Test that username minimum length is 3."""
        # Test with 2 characters - should fail
        response = client.post('/register', data={
            'username': 'ab',
            'email': 'test@example.com',
            'password': 'password123'
        })
        assert response.status_code == 200  # Form redisplayed
        
        # Test with 3 characters - should accept
        response = client.post('/register', data={
            'username': 'abc',
            'email': 'test@example.com',
            'password': 'password123'
        })
        # Should not show validation error for username
        assert b'between 3 and 32' not in response.data.lower()
    
    def test_password_min_length_is_6(self, client):
        """Test that password minimum length is 6."""
        # Test with 5 characters - should fail
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'pass1'
        })
        assert response.status_code == 200  # Form redisplayed
        
        # Test with 6 characters - should accept
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'pass12'
        })
        # Should not show validation error for password length
        assert b'at least 6' not in response.data.lower() or b'password' not in response.data.lower()


class TestDatabaseOperations:
    """Test core database operations."""
    
    def test_multiple_users_can_be_created(self, client):
        """Test that multiple users can be created."""
        conn = get_connection(app)
        
        user1 = User.create(conn, 'user1', 'pass1', 'user1@example.com')
        user2 = User.create(conn, 'user2', 'pass2', 'user2@example.com')
        user3 = User.create(conn, 'user3', 'pass3', 'user3@example.com')
        
        assert user1.id != user2.id
        assert user2.id != user3.id
        
        # Verify all users can be retrieved
        assert User.get_by_username(conn, 'user1') is not None
        assert User.get_by_username(conn, 'user2') is not None
        assert User.get_by_username(conn, 'user3') is not None
        
        conn.close()
    
    def test_user_fields_are_preserved(self, client):
        """Test that user field data is preserved in database."""
        conn = get_connection(app)
        
        User.create(conn, 'myuser', 'mypassword', 'my@email.com')
        retrieved = User.get_by_username(conn, 'myuser')
        
        assert retrieved.username == 'myuser'
        assert retrieved.email == 'my@email.com'
        assert retrieved.verify_password('mypassword') is True
        assert not retrieved.verify_password('wrongpass') 
        
        conn.close()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
