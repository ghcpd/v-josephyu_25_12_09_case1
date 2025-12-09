This folder contains guidance and artifacts related to the automated tests.

Automated tests (pytest) already exercise the main flows (create user, register, login, model behavior).

How tests operate:
- They run an isolated sqlite database (temporary) and exercise the Flask test client.
- Tests check: user creation, register+login flow, validation rules, and route existence.

Files of interest:
- `tests/test_app.py` — the main set of tests (already present in repo root `tests/`).

Manual API checks: because the forms use WTForms and CSRF protection is active by default, automated curl-based checks require CSRF handling. Use the test suite or a browser to check the live endpoints.
