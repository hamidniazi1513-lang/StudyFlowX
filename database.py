import sqlite3


conn = sqlite3.connect(
    "student_assistant.db",
    check_same_thread=False
)

cursor = conn.cursor()


# ===== Notes Table =====

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    note TEXT
)
""")


# ===== Users Table =====

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    chat_id INTEGER PRIMARY KEY
)
""")


# ===== Schedule Table =====

cursor.execute("""
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    day TEXT,
    subject TEXT,
    time TEXT
)
""")


conn.commit()