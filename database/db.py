import sqlite3
from werkzeug.security import generate_password_hash


def get_db():
    conn = sqlite3.connect("spendly.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()

    row = conn.execute(
        "SELECT id FROM users WHERE email = ?",
        ("demo@spendly.com",)
    ).fetchone()

    if row is None:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", generate_password_hash("demo123"))
        )
        conn.commit()

    user_id = conn.execute(
        "SELECT id FROM users WHERE email = ?",
        ("demo@spendly.com",)
    ).fetchone()["id"]

    existing = conn.execute(
        "SELECT COUNT(*) FROM expenses WHERE user_id = ?",
        (user_id,)
    ).fetchone()[0]

    if existing == 0:
        expenses = [
            (user_id, 450.00,  "Food",          "2026-06-01", "Grocery run at DMart"),
            (user_id,  85.00,  "Transport",     "2026-06-02", "Uber to office"),
            (user_id, 1200.00, "Bills",          "2026-06-03", "Electricity bill"),
            (user_id, 300.00,  "Health",         "2026-06-04", "Pharmacy — vitamins"),
            (user_id, 550.00,  "Entertainment",  "2026-06-05", "Netflix + movie tickets"),
            (user_id, 2100.00, "Shopping",       "2026-06-06", "New sneakers"),
            (user_id, 180.00,  "Food",           "2026-06-07", "Dinner at Biryani Blues"),
            (user_id,  60.00,  "Other",          "2026-06-08", "Parking charges"),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description)"
            " VALUES (?, ?, ?, ?, ?)",
            expenses
        )
        conn.commit()

    conn.close()


def get_user_by_email(email):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user


def create_user(name, email, password_hash):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id
