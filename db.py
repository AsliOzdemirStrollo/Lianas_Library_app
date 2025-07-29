import sqlite3

def get_connection():
    conn = sqlite3.connect('Lianas_Library_app.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


