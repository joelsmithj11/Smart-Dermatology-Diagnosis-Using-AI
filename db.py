import sqlite3
import os

DB_PATH = os.path.join("database", "dermatology.db")

def get_connection():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password_hash TEXT,
        role TEXT,
        is_verified INTEGER DEFAULT 1,
        patient_name TEXT,
        gender TEXT,
        location TEXT,
        state TEXT,
        country TEXT,
        profile_completed INTEGER DEFAULT 0
    )
    """)

    # Attempt to rename mobile to email (migration)
    try:
        cur.execute("ALTER TABLE users RENAME COLUMN mobile TO email")
    except Exception:
        pass # Column likely already named email or mobile doesn't exist

    cur.execute("""
    CREATE TABLE IF NOT EXISTS location (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        latitude REAL,
        longitude REAL,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS otp_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        otp_code TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        login_time TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        disease TEXT,
        confidence REAL,
        timestamp TEXT,
        original_img TEXT,
        gradcam_img TEXT
    )
    """)

    conn.commit()
    conn.close()
