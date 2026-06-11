# Spec: Registration

## Overview
This step wires up the registration form so new users can create an account.
The GET route already exists and renders the form; this step adds the POST
handler that validates input, hashes the password, inserts the user into the
`users` table, and redirects to the login page with a success flash message.
It also adds the two DB helpers (`get_user_by_email`, `create_user`) that the
route delegates to.

## Depends on
- Step 01 — Database Setup (users table must exist)

## Routes
- `POST /register` — validate form, hash password, insert user, redirect to login — public

## Database changes
No database changes. The `users` table (id, name, email, password_hash,
created_at) was created in Step 01 and already supports all fields needed.

## Templates
- **Modify:** `templates/register.html`
  - Add `method="POST"` and `action="{{ url_for('register') }}"` to the `<form>` tag
  - Render flash messages for errors (duplicate email, missing fields) and success
  - Re-populate `name` and `email` fields from `request.form` on validation failure
  - Do not re-populate the password field

## Files to change
- `app.py` — update `register()` to handle GET and POST; add flash + redirect logic
- `database/db.py` — add `get_user_by_email(email)` and `create_user(name, email, password_hash)`
- `templates/register.html` — wire form POST, flash messages, sticky fields

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` ships with Flask and is already
available.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` via `get_db()` only
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `get_db()` already sets `PRAGMA foreign_keys = ON` — do not add it again in helpers
- Duplicate email must return HTTP 200 with an error message in the form, not a 500
- After successful registration redirect to `url_for('login')` with a flashed success message
- Use `app.secret_key` for flash — ensure it is set in `app.py` if not already
- `create_user` must NOT return the inserted row's password hash to the caller

## Definition of done
- [ ] Visiting `/register` renders the form (GET still works)
- [ ] Submitting the form with valid name, email, password creates a new row in `users`
- [ ] Submitting with an already-registered email shows an inline error on the form
- [ ] Submitting with any blank field shows a validation error without crashing
- [ ] Successful registration redirects to `/login` and shows a success flash message
- [ ] Password stored in DB is a hash, not plaintext (verify with a DB browser or `sqlite3` CLI)
- [ ] Name and email fields are re-populated after a failed submission; password field is empty
