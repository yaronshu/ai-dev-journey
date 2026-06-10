import sqlite3
import os

# Put bugs.db in the project folder (the parent of app/) so its location does
# NOT depend on which directory you launch uvicorn from.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'bugs.db')


def get_connection() -> sqlite3.Connection:
    # check_same_thread=False: FastAPI may create the connection (in the get_db
    # dependency) on a different thread than the async endpoint that uses it.
    # Safe here because every request gets its own short-lived connection.
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row   # rows behave like dicts: row['title']
    return conn


def init_db() -> None:
    # Create the defects table once, on startup, if it doesn't already exist.
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS defects (
            id                 TEXT PRIMARY KEY,
            title              TEXT NOT NULL,
            description        TEXT NOT NULL,
            severity           TEXT NOT NULL,
            reporter           TEXT NOT NULL,
            status             TEXT NOT NULL DEFAULT 'open',
            created_at         TEXT NOT NULL,
            category           TEXT,
            suggested_severity TEXT,
            suggested_assignee TEXT,
            explanation        TEXT,
            confidence         REAL
        )
    ''')
    conn.commit()
    conn.close()


def get_db():
    # FastAPI dependency: hand each request its own connection, always close it.
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
