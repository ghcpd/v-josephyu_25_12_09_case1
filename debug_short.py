from app import app, init_db

app.config['DATABASE'] = 'tmp_debug.sqlite3'
app.config['WTF_CSRF_ENABLED'] = False
init_db(app)

with app.test_client() as c:
    r = c.post('/register', data={'username': 'short', 'email': 'short@example.com', 'password': 'abc'}, follow_redirects=True)
    print('STATUS', r.status_code)
    print(r.data.decode('utf-8'))
