# Spec: Login and Logout

## Overview
This step adds session-based authentication to Spendly. Users can log in with their email and password, which are verified against the hashed password stored in the database. A successful login stores the user's ID in the Flask session, granting access to protected routes. Logout clears the session and redirects to the landing page. This step also stubs the session guard pattern that subsequent steps will use to protect routes.

## Depends on
- Step 01: Database Setup — `get_db()`, `users` table, `get_user_by_email()`
- Step 02: Registration — users exist in the database with hashed passwords

## Routes
- `POST /login` — validates credentials, sets session, redirects to `/profile` — public
- `GET /logout` — clears session, redirects to `/` — public (safe to call even if not logged in)

## Database changes
No database changes. `get_user_by_email(email)` already exists in `database/db.py`.

## Templates
- **Modify:** `templates/login.html` — ensure form POSTs to `url_for('login')`, shows flashed error messages, repopulates email field on failure

## Files to change
- `app.py` — add `POST /login` handler; implement `GET /logout` stub
- `templates/login.html` — wire up form action, flash message display, email repopulation

## Files to create
No new files.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available via the existing `werkzeug` install.

## Rules for implementation
- No SQLAlchemy or ORMs — raw SQLite via `get_db()` only
- Parameterised queries only — no f-strings in SQL
- Password verified with `werkzeug.security.check_password_hash`
- Session key must be `user_id` (integer) — e.g. `session['user_id'] = user['id']`
- Use `flask.session` — do not use cookies directly
- Flash messages via `flask.flash()` — category `"error"` for failures
- Use `abort()` for HTTP errors — never return bare strings
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Logout must call `session.clear()` — not `session.pop()`
- After login, redirect to `/profile` (stub is fine — it returns 200)
- After logout, redirect to `/`

## Definition of done
- [ ] Submitting the login form with a valid email and correct password redirects to `/profile`
- [ ] Submitting with a valid email but wrong password re-renders the login page with a flash error message
- [ ] Submitting with an unknown email re-renders the login page with a flash error message (same generic message — do not reveal whether email exists)
- [ ] After a failed login, the email field is repopulated with the submitted value
- [ ] Visiting `GET /logout` clears the session and redirects to `/`
- [ ] After logout, visiting `/profile` does not show the previous user's data (session is gone)
- [ ] The demo user (`demo@spendly.com` / `demo123`) can log in successfully
