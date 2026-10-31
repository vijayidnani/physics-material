"""Run this ONCE to create the database file (portal.db) and the first admin.

    python init_db.py
"""
import getpass
import os
import sqlite3

from werkzeug.security import generate_password_hash

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portal.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,          -- the login ID
    password_hash TEXT NOT NULL,                 -- never store plain passwords
    full_name     TEXT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN ('student','teacher','admin'))
);

CREATE TABLE IF NOT EXISTS results (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exam       TEXT NOT NULL,                    -- e.g. "Mid-term 2026"
    subject    TEXT NOT NULL,
    marks      REAL NOT NULL,
    max_marks  REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_results_student ON results(student_id);
"""


def main():
    db = sqlite3.connect(DB)
    db.executescript(SCHEMA)

    if db.execute("SELECT 1 FROM users WHERE role='admin'").fetchone():
        print("An admin already exists. Tables are ready. Nothing else to do.")
        return

    print("Create the first admin account.")
    username = input("Admin login ID (e.g. admin): ").strip() or "admin"
    name = input("Admin full name: ").strip() or "Administrator"
    while True:
        pw = getpass.getpass("Admin password (min 8 characters): ")
        if len(pw) >= 8 and pw == getpass.getpass("Type it again: "):
            break
        print("Too short or did not match. Try again.")
    db.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?,?,?,'admin')",
               (username, generate_password_hash(pw), name))
    db.commit()
    print(f"Done. Admin '{username}' created in {DB}")


if __name__ == "__main__":
    main()
